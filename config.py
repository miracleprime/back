# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'yy'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False