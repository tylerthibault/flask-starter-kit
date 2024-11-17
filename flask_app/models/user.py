from flask_app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    sys_admin = db.Column(db.Boolean, default=False)
    disabled = db.Column(db.Boolean, default=False)  # New field
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def is_active(self):
        """Check if the user is active (not disabled)."""
        return not self.disabled