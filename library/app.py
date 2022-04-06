from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def get_database_url():
    DATA_BASE_URL = os.environ['DB_URL']
    return DATA_BASE_URL

def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    app.config['SECRET_KEY']='Th1s1ss3cr3t'
    app.config['SQLALCHEMY_DATABASE_URI']=get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    with app.app_context():
        from . import models
        from .views import (users_bp) # Import routes
        db.create_all()  # Create sql tables for our data models

        app.register_blueprint(users_bp)
        
        return app
