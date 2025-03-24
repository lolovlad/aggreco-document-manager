from flask import Blueprint, render_template, request, redirect, session, url_for, send_from_directory, send_file
from Server.Services.TemplatesServices import TemplatesService
from Server.Services.DeviceServices import DeviceServices
from Server.Services.UserService import UserService
from Server.Services.EquipmentService import EquipmentServices
from Server.Services.ClaimService import ClaimServices

from flask_login import current_user, login_required

from Server.Forms import TemplateForm, UserForm, TypeDeviceForm, DeviceForm, EquipmentForm, ClaimForm
from Server.Models.User import PostUser

from pathlib import Path

admin_router = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin_router.before_request
def is_admin():
    if current_user.is_authenticated:
        user_roles = current_user.user.role.name
        if "admin" != user_roles and "super_admin" != user_roles:
            return redirect("/")
    else:
        return redirect("/")


menu = [
    {'url': '.templates', 'title': "Шаблоны документов"},
    {'url': '.devices', 'title': "Список приборов"},
    {'url': '.users', 'title': "Пользователи"},
    {'url': '.equipments', 'title': "Оборудованние"},
    {'url': '.claim', 'title': "Отчеты"}
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


@admin_router.route('/templates/form/', methods=['GET', 'POST'])
@admin_router.route("/templates/form/<int:template_id>", methods=["POST", "GET"])
@login_required
def manage_template(template_id=None):
    template_service = TemplatesService()
    form = TemplateForm()
    form.types.choices = [(i.id, i.name) for i in template_service.get_list_types()]
    form.plant.choices = [(i.id, i.name) for i in template_service.get_list_plants()]

    template = None

    if request.method == 'GET':
        if template_id:
            template = template_service.get_template(template_id)
            if template:
                form.id.data = template.id
                form.name.data = template.name
                form.types.data = template.id_type
                form.plant.data = template.id_plant
        return render_template("form_template_page.html",
                               menu=menu,
                               form=form,
                               id_add=True,
                               template=template)

    if form.validate_on_submit():
        if template_id:
            file = form.file.data
            name_template = form.name.data
            type_template = form.types.data
            plant = form.plant.data
            template_service.update_template(template_id, name_template, type_template, plant, file)
        else:
            file = form.file.data
            name_template = form.name.data
            type_template = form.types.data
            plant = form.plant.data
            if file:
                template_service.add_template(name_template, type_template, plant, file)
        return redirect(url_for(".templates"))


@admin_router.route("/templates/delete/<int:id_temp>", methods=["GET"])
@login_required
def delete_template(id_temp):
    template_service = TemplatesService()
    if request.method == 'GET':
        template_service.delete_template(id_temp)
        return redirect(url_for(".templates"))


@admin_router.route("/devices", methods=["GET"])
@login_required
def devices():
    device_service = DeviceServices()
    return render_template("devices_page.html", menu=menu, devices=device_service.get_list_device())


@admin_router.route('/devices/edit/', methods=['GET', 'POST'])
@admin_router.route("/devices/edit/<int:devices_id>", methods=["POST", "GET"])
@login_required
def manage_device(devices_id=None):
    device_service = DeviceServices()
    form = DeviceForm()
    form.type.choices = [(i.id, i.name) for i in device_service.get_list_type_device()]

    device = None

    if request.method == "GET":
        if devices_id:
            device = device_service.get_device(devices_id)
            if device:
                form.id.data = device.id
                form.type.data = device.id_type
                form.number.data = device.number
                form.date_verification.data = device.date_verification
                form.date_next_verification.data = device.date_next_verification
                form.certificate_number.data = device.certificate_number
        return render_template("form_devices_page.html",
                               menu=menu,
                               form=form)
    if form.validate_on_submit():
        if devices_id:
            name = form.name.data
            number = form.number.data
            date_verification = form.date_verification.data
            date_next = form.date_next_verification.data
            certificate_number = form.certificate_number.data
            id_type = int(form.type.data)
            device_service.update_device(devices_id,
                                           name,
                                           number,
                                           date_verification,
                                           date_next,
                                           certificate_number,
                                           id_type
                                           )
        else:
            name = form.name.data
            number = form.number.data
            date_verification = form.date_verification.data
            date_next = form.date_next_verification.data
            certificate_number = form.certificate_number.data
            id_type = int(form.type.data)
            device_service.add_device(name,
                                      number,
                                      date_verification,
                                      date_next,
                                      certificate_number,
                                      id_type)
        return redirect(url_for('.devices'))


@admin_router.route("/devices/delete/<int:id_device>", methods=["GET"])
@login_required
def delete_device(id_device):
    device_service = DeviceServices()
    if request.method == 'GET':
        device_service.delete_device(id_device)
        return redirect(url_for(".device"))


@admin_router.route("/form_type_device", methods=["GET", "POST"])
@login_required
def from_type_devices():
    device_service = DeviceServices()
    form = TypeDeviceForm()
    if request.method == "GET":
        return render_template("form_type_devices_page.html", menu=menu, form=form)
    if form.validate_on_submit():
        device_service.add_type_device(form.type_device.data)
        return redirect(url_for('.devices'))


@admin_router.route("/users",  methods=["GET"])
@login_required
def users():
    user_service = UserService()
    if request.method == "GET":
        return render_template("user_page.html", menu=menu, users=user_service.get_list_users())


@admin_router.route('/user/edit/', methods=['GET', 'POST'])
@admin_router.route("/user/edit/<int:user_id>", methods=["POST", "GET"])
@login_required
def manage_user(user_id=None):
    user_service = UserService()
    form = UserForm()
    form.id_role.choices = [(i.id, i.name) for i in user_service.get_list_roles()]

    user = None

    if request.method == 'GET':
        if user_id:
            user = user_service.get_user(user_id)
            if user:
                form.id.data = user.id
                form.name.data = user.name
                form.surname.data = user.surname
                form.patronymics.data = user.patronymics
                form.id_role.data = user.id_role
                form.email.data = user.email
                form.job_title.data = user.job_title
        return render_template("form_user_page.html",
                               menu=menu,
                               form=form,
                               user=user)

    if form.validate_on_submit():
        if user_id:
            user_service.update_user(user_id, form)
        else:
            user = PostUser(
                name=form.name.data,
                surname=form.surname.data,
                patronymics=form.patronymics.data,
                email=form.email.data,
                job_title=form.job_title.data,
                painting="",
                password=form.password.data,
                id_role=int(form.id_role.data)
            )
            user_service.add_user(user)
        return redirect(url_for(".users"))


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


@admin_router.route("/equpments",  methods=["GET"])
@login_required
def equipments():
    service = EquipmentServices()
    if request.method == "GET":
        return render_template("equipment_page.html", menu=menu, equipments=service.get_list_equipment())


@admin_router.route("/equpments/<uuid_equipments>/claim",  methods=["GET"])
@login_required
def claim_in_equipments(uuid_equipments):
    service = ClaimServices()
    if request.method == "GET":
        claims = service.get_list_claim_in_equipments(uuid_equipments)
        return render_template("claim_admin_page.html", menu=menu, claims=claims)


@admin_router.route('/equipment/edit/', methods=['GET', 'POST'])
@admin_router.route("/equipment/edit/<equipment_uuid>", methods=["POST", "GET"])
@login_required
def manage_equipment(equipment_uuid=None):
    service = EquipmentServices()
    form = EquipmentForm()
    form.type.choices = [(i.id, f"{i.name} ({i.code})") for i in service.get_list_type_equipments()]

    equipment = None

    if request.method == 'GET':
        if equipment_uuid:
            equipment = service.get_by_uuid(equipment_uuid)
            if equipment:
                form.id.data = equipment.id
                form.code.data = equipment.code
                form.type.data = equipment.id_type
                form.description.data = equipment.description
        return render_template("form_equipment_page.html",
                               menu=menu,
                               form=form,
                               equipment=equipment)
    if form.validate_on_submit():
        if equipment_uuid:
            service.update_equipment(equipment_uuid, form)
        else:
            service.add_equipments(form)
        return redirect(url_for(".equipments"))


@admin_router.route("/equipment/delete/<equipment_uuid>",  methods=["GET"])
@login_required
def delete_equipment(equipment_uuid):
    service = EquipmentServices()
    if request.method == "GET":
        service.delete_equipment(equipment_uuid)
        return redirect(url_for(".equipments"))


@admin_router.route("/claim", methods=["POST", "GET"])
@login_required
def claim():
    service = ClaimServices()
    if request.method == "GET":
        claims = service.get_list_claim("under_consideration")
        return render_template("claim_admin_page.html", menu=menu, claims=claims)


@admin_router.route("/claim/delete/<uuid_claim>", methods=["POST", "GET"])
@login_required
def delete_claim(uuid_claim):
    service = ClaimServices()
    if request.method == "GET":
        service.delete_claim(uuid_claim)
        return redirect(url_for(".claim"))


@admin_router.route('/claim/edit/', methods=['GET', 'POST'])
@admin_router.route("/claim/edit/<uuid_claim>", methods=["POST", "GET"])
@login_required
def manage_claim(uuid_claim):
    service = ClaimServices()
    form = ClaimForm()
    if request.method == 'GET':
        claim = service.get_by_uuid(uuid_claim)
        if uuid_claim:
            form.description.data = claim.comment
        return render_template("claim_form_admin_page.html",
                               menu=menu,
                               form=form,
                               claim=claim)
    if form.validate_on_submit():
        if uuid_claim:
            service.update_claim(uuid_claim, form)
        return redirect(url_for(".claim"))


@admin_router.route("/claim/send/<uuid_claim>/<type_state>", methods=["POST", "GET"])
@login_required
def send_claim(uuid_claim, type_state):
    service = ClaimServices()
    if request.method == "GET":
        service.send_claim(uuid_claim, type_state)
        return redirect(url_for(".claim"))


@admin_router.route("/download_claim/<uuid_claim>", methods=["GET"])
@login_required
def download_claim(uuid_claim):
    claim_service = ClaimServices()
    claim = claim_service.get_by_uuid(uuid_claim)
    path_file = Path(claim.main_document)
    return send_file(
        path_or_file=path_file.absolute(),
        download_name=f"Отчет{path_file.suffix}",
        as_attachment=True
    )

