from flask_login import UserMixin

from .extensions import db


class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


class File(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    stored_filename = db.Column(
        db.String(255),
        nullable=False
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


class FileShare(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    file_id = db.Column(
        db.Integer,
        db.ForeignKey("file.id"),
        nullable=False
    )

    shared_with_user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    permission = db.Column(
        db.String(20),
        nullable=False,
        default="download"
    )

    shared_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    __table_args__ = (
        db.UniqueConstraint(
            "file_id",
            "shared_with_user_id",
            name="unique_file_share"
        ),
    )