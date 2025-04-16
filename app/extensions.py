from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS


db = SQLAlchemy()
bcrypt = Bcrypt()
marsh = Marshmallow()
jwt = JWTManager()
cors = CORS()