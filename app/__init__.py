from flask import Flask
from app.config import Config
from app.extensions import db, marsh, bcrypt, jwt, cors
import os



def create_app(config_class=Config):
    """A function to and configure flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") or "sqlite:///default.db"

    #Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    marsh.init_app(app)
    cors.init_app(app)



    from .auth import init_auth_module
    from .notes import init_notes_module

    init_auth_module(app)
    init_notes_module(app)

    return app