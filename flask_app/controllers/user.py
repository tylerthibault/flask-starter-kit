from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html")

@bp.route("/settings")
@login_required
def settings():
    return render_template("user/settings.html")