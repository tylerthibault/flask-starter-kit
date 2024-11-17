from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from flask_app.controllers import user
from flask_app.models.user import User
from flask_app.forms.auth_forms import LoginForm, RegisterForm
from flask_app.utils.auth_utils import authenticate_user
from flask_app.extensions import db, bcrypt

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home.index'))
        else:
            flash("Invalid email or password.", "danger")
    
    return render_template('auth/login.html', form=form)




@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))  # Redirect to the login page