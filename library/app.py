from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    app.config['SECRET_KEY']='Th1s1ss3cr3t'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    with app.app_context():
        from . import models
        from .views import (users_bp) # Import routes
        db.create_all()  # Create sql tables for our data models

        app.register_blueprint(users_bp)
        
        return app
