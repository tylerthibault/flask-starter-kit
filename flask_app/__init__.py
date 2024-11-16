from flask import Flask
from flask_migrate import Migrate
from flask_app.config.config import Config
from flask_app.extensions import db, migrate, login_manager, mail, csrf
from flask_app.controllers import auth

from flask_app.controllers.auth import bp as auth_bp
from flask_app.controllers.home import bp as home_bp

migrate = Migrate()

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)  # Optional
    csrf.init_app(app)  # Optional

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    return app
