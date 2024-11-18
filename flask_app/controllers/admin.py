import pickle
from flask import Blueprint, abort, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.sql import text


from flask_app.extensions import bcrypt, db
from flask_app.forms.admin_forms import AddUserForm, EditUserForm
from flask_app.forms.site_config import SiteConfigForm
from flask_app.models.roles_permissions import Role
from flask_app.models.site_config import SiteConfig
from flask_app.models.user import User

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.has_permission('sys-admin'):
        return "Access Denied", 403

    # Total users
    total_users = User.query.count()

    # Pass the data to the template
    stats = {
        'total_users': total_users,
    }
    return render_template('sys_admin/dashboard.html', **stats)

@bp.route("/manage_users")
@login_required
def manage_users():
    if not current_user.has_permission('sys-admin'):
        return "Access Denied", 403

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    query = User.query

    if search:
        query = query.filter(
            (User.username.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%"))
        )

    pagination = query.paginate(page=page, per_page=10, error_out=False)
    users = pagination.items

    return render_template("sys_admin/manage_users.html", users=users, pagination=pagination)

@bp.route('/view_logs')
@login_required
def view_logs():
    if not current_user.has_permission('sys-admin'):
        return "Access Denied", 403
    
    # Replace this with logic to fetch and display logs
    return render_template('sys_admin/view_logs.html')

@bp.route('/site_config', methods=['GET', 'POST'])
def site_config():
    if not current_user.has_permission('sys-admin'):
        return "Access Denied", 403
    
    config = SiteConfig.query.first() or SiteConfig()
    form = SiteConfigForm(obj=config)

    if form.validate_on_submit():
        # Save form data to the database
        form.populate_obj(config)
        if 'logo' in request.files and request.files['logo']:
            logo = request.files['logo']
            config.logo_path = f"uploads/{logo.filename}"  # Save file logic required
        if 'favicon' in request.files and request.files['favicon']:
            favicon = request.files['favicon']
            config.favicon_path = f"uploads/{favicon.filename}"  # Save file logic required

        db.session.add(config)
        db.session.commit()
        flash("Site configuration updated successfully!", "success")
        return redirect(url_for('admin.site_config'))

    # Pass the form object to the template
    return render_template('sys_admin/site_config.html', form=form, config=config)


# CRUD - USERS
# Create
@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    # Check if the current user has the required permission
    if not current_user.has_permission('sys-admin'):
        return "Access Denied", 403

    # Initialize the form
    form = AddUserForm()
    form.roles.choices = [(role.id, role.name) for role in Role.query.all()]  # Populate roles dynamically

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        selected_roles = form.roles.data  # Get selected roles from the form

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create the new user
        new_user = User(username=username, email=email, password_hash=hashed_password)

        # Assign roles to the user
        for role_id in selected_roles:
            role = Role.query.get(role_id)
            if role:
                new_user.roles.append(role)

        # Save to the database
        db.session.add(new_user)
        db.session.commit()

        flash(f"User '{username}' added successfully!", 'success')
        return redirect(url_for('admin.manage_users'))

    return render_template('sys_admin/add_user.html', form=form)


    return render_template('sys_admin/add_user.html', form=form)
# READ

# UPDATE
@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.has_permission('sys-admin'):
        return "Access Denied", 403

    user = User.query.get_or_404(user_id)

    # Initialize the form
    form = EditUserForm(obj=user)
    form.roles.choices = [(role.id, role.name) for role in Role.query.all()]  # Populate roles dynamically

    if form.validate_on_submit():
        # Update user fields
        user.username = form.username.data
        user.email = form.email.data

        # Update roles
        selected_roles = Role.query.filter(Role.id.in_(form.roles.data)).all()
        user.roles = selected_roles  # Assign the selected roles

        # Save changes to the database
        db.session.commit()
        flash(f"User '{user.username}' updated successfully!", 'success')
        return redirect(url_for('admin.manage_users'))

    # Prepopulate selected roles
    form.roles.data = [role.id for role in user.roles]

    return render_template('sys_admin/edit_user.html', form=form, user=user)


@bp.route('/toggle_user_status/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if not current_user.has_permission('sys-admin'):
        return "Access Denied", 403

    user = User.query.get_or_404(user_id)
    user.disabled = not user.disabled  # Toggle the user's status
    db.session.commit()

    action = "enabled" if not user.disabled else "disabled"
    flash(f"User '{user.username}' has been {action}.", 'success')
    return redirect(url_for('admin.manage_users'))


# DELETE
@bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.has_permission('sys-admin'):
        return "Access Denied", 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} deleted successfully.", "success")
    return redirect(url_for("admin.manage_users"))

