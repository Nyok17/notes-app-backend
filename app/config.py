import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'FALSE').lower()== "true"
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    