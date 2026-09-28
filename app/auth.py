from flask import Blueprint, render_template, request, Response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user

import os
import uuid

from .extensions import db
from .models import User, File, FileShare
from .encryption import encrypt_file, decrypt_file


auth = Blueprint("auth", __name__)


ALLOWED_EXTENSIONS = {
    "txt",
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "docx"
}


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_username:
            return "Username already exists."

        if existing_email:
            return "Email already registered."

        password_hash = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        return "Registration successful!"

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return "Login successful!"

        return "Invalid username or password."

    return render_template("login.html")


@auth.route("/logout")
def logout():

    logout_user()

    return "Logged out successfully!"


@auth.route("/dashboard")
@login_required
def dashboard():

    files = File.query.filter_by(
        owner_id=current_user.id
    ).all()

    return render_template(
        "dashboard.html",
        files=files
    )


@auth.route("/files")
@login_required
def files():

    user_files = File.query.filter_by(
        owner_id=current_user.id
    ).all()

    return render_template(
        "files.html",
        files=user_files
    )

@auth.route("/shared-with-me")
@login_required
def shared_with_me():
    shared_files = FileShare.query.filter_by(
        shared_with_user_id=current_user.id
    ).all()

    files = [
        File.query.get(share.file_id)
        for share in shared_files
    ]

    return render_template("shared_with_me.html", files=files)

@auth.route("/upload", methods=["POST"])
@login_required
def upload_file():

    if "file" not in request.files:
        return "No file selected."

    uploaded_file = request.files["file"]

    MAX_FILE_SIZE = 10 * 1024 * 1024

    uploaded_file.stream.seek(0, 2)
    file_size = uploaded_file.stream.tell()
    uploaded_file.stream.seek(0)

    if file_size > MAX_FILE_SIZE:
        return "File is too large. Maximum size is 10 MB."

    if uploaded_file.filename == "":
        return "No file selected."

    original_filename = secure_filename(
        uploaded_file.filename
    )

    file_extension = original_filename.rsplit(
        ".",
        1
    )[-1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        return "File type not allowed."

    unique_filename = (
        str(uuid.uuid4())
        + "_"
        + original_filename
    )

    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads"
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_folder,
        unique_filename
    )

    file_data = uploaded_file.read()

    encrypted_data = encrypt_file(
        file_data
    )

    with open(file_path, "wb") as file:
        file.write(encrypted_data)

    new_file = File(
        original_filename=original_filename,
        stored_filename=unique_filename,
        owner_id=current_user.id
    )

    db.session.add(new_file)
    db.session.commit()

    return "File uploaded and encrypted successfully!"


@auth.route("/download/<int:file_id>")
@login_required
def download_file(file_id):

    file_record = File.query.get_or_404(
        file_id
    )

    if file_record.owner_id != current_user.id:

        shared_file = FileShare.query.filter_by(
            file_id=file_record.id,
            shared_with_user_id=current_user.id
        ).first()

        if not shared_file:
            return "You are not allowed to download this file.", 403

    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads"
    )

    file_path = os.path.join(
        upload_folder,
        file_record.stored_filename
    )

    if not os.path.exists(file_path):
        return "File not found.", 404

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = decrypt_file(
        encrypted_data
    )

    response = Response(
        decrypted_data,
        mimetype="application/octet-stream"
    )

    response.headers["Content-Disposition"] = (
        f'attachment; filename="{file_record.original_filename}"'
    )

    return response


@auth.route(
    "/delete/<int:file_id>",
    methods=["POST"]
)
@login_required
def delete_file(file_id):

    file_record = File.query.get_or_404(
        file_id
    )

    if file_record.owner_id != current_user.id:
        return "You are not allowed to delete this file.", 403

    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads"
    )

    file_path = os.path.join(
        upload_folder,
        file_record.stored_filename
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(file_record)
    db.session.commit()

    return "File deleted successfully!"


@auth.route(
    "/share/<int:file_id>",
    methods=["POST"]
)
@login_required
def share_file(file_id):

    file_record = File.query.get_or_404(
        file_id
    )

    if file_record.owner_id != current_user.id:
        return "You are not allowed to share this file.", 403

    username = request.form["username"]

    user_to_share = User.query.filter_by(
        username=username
    ).first()

    if not user_to_share:
        return "User not found."

    if user_to_share.id == current_user.id:
        return "You cannot share a file with yourself."

    existing_share = FileShare.query.filter_by(
        file_id=file_record.id,
        shared_with_user_id=user_to_share.id
    ).first()

    if existing_share:
        return "File is already shared with this user."

    file_share = FileShare(
        file_id=file_record.id,
        shared_with_user_id=user_to_share.id,
        permission="download"
    )

    db.session.add(file_share)
    db.session.commit()

    return "File shared successfully!"