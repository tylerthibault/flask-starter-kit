from flask_app.extensions import db
from flask_login import UserMixin
from flask_app.models.associations import users_roles
from flask_app.models.roles_permissions import Permission, Role


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    disabled = db.Column(db.Boolean, default=False)  # Account status
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Relationship to roles
    roles = db.relationship('Role', secondary='users_roles', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def is_active(self):
        """Check if the user is active (not disabled)."""
        return not self.disabled

    def has_permission(self, permission_name):
        """
        Check if the user has a specific permission.
        """
        # Collect all permissions from all roles assigned to the user
        user_permissions = set(permission.name for role in self.roles for permission in role.permissions)

        # Check if the requested permission exists
        return permission_name in user_permissions

    def get_roles(self):
        """
        Returns the user's roles as a list of role names.
        """
        return [role.name for role in self.roles]