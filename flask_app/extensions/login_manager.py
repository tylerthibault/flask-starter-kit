from flask_login import LoginManager

login_manager = LoginManager()

# Default login route
login_manager.login_view = "auth.login"  # Update to match your route
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# Define a user loader (example)
@login_manager.user_loader
def load_user(user_id):
    from flask_app.models.user import User
    return User.query.get(int(user_id))
