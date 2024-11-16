from flask_app.models.user import User
from flask_app.extensions.bcrypt import bcrypt

def authenticate_user(email, password):
    """
    Authenticate a user by email and password.
    :param email: User's email address
    :param password: Plain text password
    :return: User object if authenticated, None otherwise
    """
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return user
    return None
