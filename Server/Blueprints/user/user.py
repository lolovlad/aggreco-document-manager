from flask import Blueprint, render_template, request, redirect, session, url_for, send_file
from Server.Services.TemplatesServices import TemplatesService
from Server.Services.UserService import UserService

user_router = Blueprint("user", __name__, template_folder="templates", static_folder="static")

menu = [
    {'url': '.templates', 'title': "шаблоны документов"}
]


@user_router.route("/")
def index():
    return render_template("user_main.html", menu=menu, title="главная")


@user_router.route("/templates", methods=["POST", "GET"])
def templates():
    template_service = TemplatesService()
    if request.method == "GET":
        templates = [i.model_dump() for i in template_service.get_list_templates()]
        return render_template("download_template_page.html", menu=menu, templates=templates)


@user_router.route("/download_templates/<id_template>", methods=["GET"])
def download_templates(id_template):
    template_service = TemplatesService()
    send_file_partial = template_service.get_file_to_download(int(id_template), send_file)
    return send_file_partial()


@user_router.route("/form_create_document/form/<id_template>", methods=["GET", "POST"])
def create_document(id_template):
    template_service = TemplatesService()
    user_service = UserService()
    if request.method == "GET":
        scheme = template_service.get_scheme_template(int(id_template))
        scheme = template_service.add_device_to_scheme(scheme)
        users = user_service.get_list_users()
        return render_template("form_document_page.html",
                               menu=menu,
                               form_scheme=scheme,
                               id_template=id_template,
                               users=users)
    elif request.method == "POST":
        file = request.files['file']
        if file:
            file_template = template_service.generate_document(request.form, file, int(id_template), send_file)
            return file_template()


@user_router.route("/templates/add", methods=["POST"])
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