from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def get_database_url():
    DB_NAME = os.environ.get('DB_NAME')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_USER = os.environ.get('DB_USER')

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    return DATABASE_URL

def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    app.config['SECRET_KEY']='Th1s1ss3cr3t'
    app.config['SQLALCHEMY_DATABASE_URI']=get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    with app.app_context():
        from . import models
        from .views import (users_bp, authors_bp) # Import routes
        db.create_all()  # Create sql tables for our data models
        
        app.register_blueprint(users_bp)
        app.register_blueprint(authors_bp)
        
        return app
