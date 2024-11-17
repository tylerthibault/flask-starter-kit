from flask_app.extensions import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationship to permissions
    permissions = db.relationship(
        'Permission',
        secondary='roles_permissions',
        backref=db.backref('roles', lazy='dynamic')
    )

    def __repr__(self):
        return f"<Role {self.name}>"

# Permission model
class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Permission {self.name}>"

# Association table for roles and permissions
roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True),
    extend_existing=True  # Allow redefinition if this table already exists
)
