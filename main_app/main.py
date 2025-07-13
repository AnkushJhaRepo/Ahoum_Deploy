from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from main_app.config import Config
from main_app.models import db, migrate
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def index():
        return "Server running"

    return app
