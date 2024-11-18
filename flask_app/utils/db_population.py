from flask_app.extensions import bcrypt, db
from flask_app.models.roles_permissions import Permission, Role
from flask_app.models.user import User


def populate_roles_and_permissions():
    """Populate roles and their associated permissions."""
    user = ["user-view", "user-edit"]
    admin = ["admin-view", "admin-edit"] + user
    sys_admin = ["sys-admin"] + admin

    roles_permissions = {
        "user": user,
        "admin": admin,
        "sys-admin": sys_admin,
    }

    # Populate roles
    for role_name in roles_permissions.keys():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)

    db.session.commit()

    # Populate permissions and assign to roles
    for role_name, permissions in roles_permissions.items():
        role = Role.query.filter_by(name=role_name).first()
        for permission_name in permissions:
            permission = Permission.query.filter_by(name=permission_name).first()
            if not permission:
                permission = Permission(name=permission_name)
                db.session.add(permission)
            if permission not in role.permissions:
                role.permissions.append(permission)
    db.session.commit()


def populate_sys_admin_user():
    """Populate a user with the sys-admin role."""
    # Define sys-admin user credentials
    sys_admin_username = "sysadmin"
    sys_admin_email = "sysadmin@email.com"
    sys_admin_password = "Pass123!!"  # Change this in production!

    # Check if the user already exists
    user = User.query.filter_by(email=sys_admin_email).first()
    if not user:
        # Create the user
        user = User(
            username=sys_admin_username,
            email=sys_admin_email,
            password_hash=bcrypt.generate_password_hash(sys_admin_password)
        )
        db.session.add(user)
        db.session.commit()

    # Check if the sys-admin role exists
    sys_admin_role = Role.query.filter_by(name="sys-admin").first()
    if not sys_admin_role:
        raise ValueError("The 'sys-admin' role does not exist. Please populate roles first.")

    # Assign the sys-admin role to the user if not already assigned
    if sys_admin_role not in user.roles:
        user.roles.append(sys_admin_role)
        db.session.commit()
        print(f"User '{sys_admin_username}' has been assigned the 'sys-admin' role.")

    else:
        print(f"User '{sys_admin_username}' already has the 'sys-admin' role.")