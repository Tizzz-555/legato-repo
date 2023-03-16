import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import SECRET_KEY

# Create a new SQLAlchemy object stored into db variable
db = SQLAlchemy()
UPLOAD_FOLDER = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'static/uploads')


def create_app():
    '''Returns a new Flask application instance'''

    app = Flask(__name__)
    # Set secret key configuration var, imported from config file
    app.config['SECRET_KEY'] = SECRET_KEY
    # Set database configuration var
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(os.getcwd(), 'database.db')}"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    # Initialize db object with the app instance
    db.init_app(app)

    # Import blueprints
    from .views import views
    from .auth import auth

    # Register views to handle requests, set prefix to / (no prefix)
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Create a login manager instance
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # User loader function for LoginManager
    @login_manager.user_loader
    def load_user(id):
        '''Load a User instance from the database given a user ID.'''

        return User.query.get(int(id))

    # Create all necessary database tables
    with app.app_context():
        from .models import User
        db.create_all()

    return app
