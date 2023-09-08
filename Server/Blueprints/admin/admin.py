from flask import Blueprint, render_template

admin_router = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin_router.route("/")
def index():
    return render_template("admin_main.html")