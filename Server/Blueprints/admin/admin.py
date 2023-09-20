from flask import Blueprint, render_template, request, redirect, session, url_for
from Server.Services.TemplatesServices import TemplatesService
from Server.Services.DeviceServices import DeviceServices

admin_router = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

menu = [
    {'url': '.templates', 'title': "шаблоны документов"},
    {'url': '.devices', 'title': "список приборов"}
]


@admin_router.route("/")
def index():
    return render_template("admin_main.html", menu=menu, title="главная")


@admin_router.route("/templates", methods=["POST", "GET"])
def templates():
    template_service = TemplatesService()
    if request.method == "GET":
        templates_models = template_service.get_list_templates()
        return render_template("template_page.html", menu=menu, templates=templates_models)


@admin_router.route("/templates/add", methods=["POST", "GET"])
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


@admin_router.route("/devices", methods=["GET"])
def devices():
    device_service = DeviceServices()
    return render_template("devices_page.html", menu=menu, devices=device_service.get_list_device())


@admin_router.route("/devices/add", methods=["GET", "POST"])
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
def from_type_devices():
    device_service = DeviceServices()
    if request.method == "GET":
        return render_template("form_type_devices_page.html", menu=menu)
    if request.method == "POST":
        device_service.add_type_device(request.form["name"])
        return redirect(url_for('.devices'))