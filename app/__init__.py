import os

from dotenv import load_dotenv
from flask import Flask

from .extensions import db, login_manager, csrf


load_dotenv()


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secure_files.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager.init_app(app)

    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    login_manager.login_message = None

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth

    app.register_blueprint(auth)

    @app.route("/")
    def home():

        from flask import render_template

        return render_template("home.html")

    return app