import os

from dotenv import load_dotenv
from flask import Flask

from .extensions import db

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secure_files.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .models import User

    @app.route("/")
    def home():
        return "Secure File Sharing System"

    return app