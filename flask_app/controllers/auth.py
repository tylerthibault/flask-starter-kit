from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from flask_app.controllers import user
from flask_app.models.user import User
from flask_app.forms.auth_forms import LoginForm, RegisterForm
from flask_app.utils.auth_utils import authenticate_user

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember_me.data
        
        # Authenticate user
        user = authenticate_user(email, password)
        if user:
            login_user(user, remember=remember)
            flash("Logged in successfully!", "success")
            return redirect(url_for("home.index"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("auth/login.html", form=form)


from flask_app.extensions import db, bcrypt
from flask_app.models.user import User

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

