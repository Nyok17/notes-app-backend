# config.py
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    _db_url = os.getenv("DATABASE_URL")
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _db_url or 'sqlite:///default.db'
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in the environment.")

    DEBUG = os.getenv('DEBUG', 'false').strip().lower() == 'true'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_EXP_HOURS", 1)))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
