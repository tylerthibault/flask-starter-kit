from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from flask_app.extensions import db
from flask_app.forms.admin_forms import EditUserForm
from flask_app.forms.site_config import SiteConfigForm
from flask_app.models.site_config import SiteConfig
from flask_app.models.user import User

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.sys_admin:
        abort(403)  # Forbidden if not a sys admin

    # Example data for the dashboard
    stats = {
        'active_users': 42,
        'total_users': 100,
        'pending_issues': 5
    }
    return render_template('sys_admin/dashboard.html', **stats)

@bp.route("/manage_users")
@login_required
def manage_users():
    if not current_user.sys_admin:
        abort(403)  # Restrict access to sys admins only

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
    if not current_user.sys_admin:
        abort(403)  # Restrict access to sys admins only
    # Replace this with logic to fetch and display logs
    return render_template('sys_admin/view_logs.html')

@bp.route('/site_config', methods=['GET', 'POST'])
def site_config():
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
    if not current_user.sys_admin:
        abort(403)  # Restrict access to sys admins only

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        sys_admin = request.form.get('sys_admin') == 'on'

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin.add_user'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password, sys_admin=sys_admin)
        db.session.add(new_user)
        db.session.commit()
        flash(f"User '{username}' added successfully!", 'success')
        return redirect(url_for('admin.manage_users'))

    return render_template('sys_admin/add_user.html')

# READ

# UPDATE
@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.sys_admin:
        abort(403)  # Restrict access to sys admins only

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.sys_admin = form.sys_admin.data

        db.session.commit()
        flash(f"User '{user.username}' updated successfully!", 'success')
        return redirect(url_for('admin.manage_users'))

    return render_template('sys_admin/edit_user.html', form=form, user=user)

@bp.route('/toggle_user_status/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if not current_user.sys_admin:
        abort(403)  # Restrict access to sys admins only

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
    if not current_user.sys_admin:
        abort(403)  # Restrict access to sys admins only

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} deleted successfully.", "success")
    return redirect(url_for("admin.manage_users"))

