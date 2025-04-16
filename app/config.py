import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    """Base configuration"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'FALSE').lower()== "true"
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    