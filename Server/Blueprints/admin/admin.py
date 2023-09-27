from flask import Blueprint, render_template, request, redirect, session, url_for
from Server.Services.TemplatesServices import TemplatesService
from Server.Services.DeviceServices import DeviceServices
from Server.Services.UserService import UserService
from flask_login import current_user, login_required


admin_router = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin_router.before_request
def is_admin():
    if current_user.is_authenticated:
        user_roles = [i.name for i in current_user.user.roles]
        if "admin" not in user_roles and "super_admin" not in user_roles:
            return redirect("/")
    else:
        return redirect("/")


menu = [
    {'url': '.templates', 'title': "Шаблоны документов"},
    {'url': '.devices', 'title': "Список приборов"},
    {'url': '.users', 'title': "Пользователи"}
]


@admin_router.route("/")
@login_required
def index():
    return render_template("admin_main.html", menu=menu, title="главная")


@admin_router.route("/templates", methods=["POST", "GET"])
@login_required
def templates():
    template_service = TemplatesService()
    if request.method == "GET":
        templates_models = template_service.get_list_templates()
        if templates_models is None:
            templates_models = []
        return render_template("template_page.html", menu=menu, templates=templates_models)


@admin_router.route("/templates/add", methods=["POST", "GET"])
@login_required
def add_templates():
    template_service = TemplatesService()
    if request.method == 'GET':
        types = [i.model_dump() for i in template_service.get_list_types()]
        plants = [i.model_dump() for i in template_service.get_list_plants()]
        return render_template("form_template_page.html", menu=menu, types=types, plants=plants)

    if request.method == 'POST':
        file = request.files['file']
        if file:

            name_template = request.form["name"]
            type_template = int(request.form["type"])
            plant = int(request.form["plant"])

            template_service.add_template(name_template, type_template, plant, file)
            return redirect(url_for(".templates"))


@admin_router.route("/templates/delete/<int:id_temp>", methods=["GET"])
@login_required
def delete_template(id_temp):
    template_service = TemplatesService()
    if request.method == 'GET':
        template_service.delete_template(id_temp)
        redirect(url_for(".templates"))


@admin_router.route("/devices", methods=["GET"])
@login_required
def devices():
    device_service = DeviceServices()
    return render_template("devices_page.html", menu=menu, devices=device_service.get_list_device())


@admin_router.route("/devices/add", methods=["GET", "POST"])
@login_required
def add_devices():
    device_service = DeviceServices()
    if request.method == "GET":
        return render_template("form_devices_page.html",
                               menu=menu,
                               type_dev=device_service.get_list_type_device(),
                               url=".add_devices",
                               is_add=True)
    if request.method == "POST":
        device_service.add_device(
            request.form["name"],
            request.form["number"],
            request.form["date_verification"],
            request.form["date_next_verification"],
            request.form["certificate_number"],
            int(request.form["type"])
        )
        return redirect(url_for('.devices'))


@admin_router.route("/devices/update/<id_device>", methods=["GET", "POST"])
@login_required
def update_devices(id_device):
    if request.method == "GET":
        return render_template("form_devices_page.html",
                               menu=menu,
                               id_dev=id_device,
                               type_dev=[],
                               url=".update_devices",
                               is_add=False)
    if request.method == "POST":
        return redirect(url_for('.devices'))


@admin_router.route("/form_type_device", methods=["GET", "POST"])
@login_required
def from_type_devices():
    device_service = DeviceServices()
    if request.method == "GET":
        return render_template("form_type_devices_page.html", menu=menu)
    if request.method == "POST":
        device_service.add_type_device(request.form["name"])
        return redirect(url_for('.devices'))


@admin_router.route("/users",  methods=["GET"])
@login_required
def users():
    user_service = UserService()
    if request.method == "GET":
        return render_template("user_page.html", menu=menu, users=user_service.get_list_users())


@admin_router.route("/add_user",  methods=["POST", "GET"])
@login_required
def add_user():
    user_service = UserService()
    if request.method == "GET":
        roles = user_service.get_list_roles()
        return render_template("form_user_page.html", menu=menu, is_add=True, user={"id": 1}, roles=roles)
    elif request.method == "POST":
        user_service.add_user(request.form)
        return redirect(url_for(".users"))


@admin_router.route("/delete_user/<int:id_user>",  methods=["GET"])
@login_required
def delete_user(id_user):
    user_service = UserService()
    if request.method == "GET":
        user_service.delete_user(id_user)
        return redirect(url_for(".users"))


@admin_router.route("/update_user/<int:id_user>",  methods=["PUT", "GET"])
@login_required
def update_user(id_user):
    if request.method == "GET":
        return render_template("form_user_page.html", menu=menu, user={"id": 1}, is_add=False)