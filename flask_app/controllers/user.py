from flask import Blueprint, render_template

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/profile")
def profile():
    return render_template("user/profile.html")
