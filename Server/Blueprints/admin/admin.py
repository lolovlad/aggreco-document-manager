from flask import Blueprint, render_template, request, redirect, session, url_for
from Server.Services.TemplatesServices import TemplatesService

admin_router = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

menu = [
    {'url': '.templates', 'title': "шаблоны документов"}
]

@admin_router.route("/")
def index():
    return render_template("admin_main.html", menu=menu, title="главная")


@admin_router.route("/templates", methods=["POST", "GET"])
def templates():
    template_service = TemplatesService()
    if request.method == "GET":
        types = [i.model_dump() for i in template_service.get_list_types()]
        plants = [i.model_dump() for i in template_service.get_list_plants()]
        return render_template("template_page.html", menu=menu, types=types, plants=plants)


@admin_router.route("/templates/add", methods=["POST"])
def add_templates():
    if request.method == 'POST':
        template_service = TemplatesService()
        file = request.files['file']
        if file:

            name_template = request.form["name"]
            type_template = int(request.form["type"])
            plant = int(request.form["plant"])

            template_service.add_template(name_template, type_template, plant, file)
            return redirect(url_for(".templates"))