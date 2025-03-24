from flask import Blueprint, render_template, request, redirect, session, url_for, send_file
from Server.Services.TemplatesServices import TemplatesService
from Server.Services.UserService import UserService
from Server.Services.EquipmentService import EquipmentServices
from Server.Services.ClaimService import ClaimServices
from flask_login import current_user, login_required
from Server.Forms import ClaimForm

from pathlib import Path

user_router = Blueprint("user", __name__, template_folder="templates", static_folder="static")


@user_router.before_request
def is_user():
    if current_user.is_authenticated:
        user_roles = current_user.user.role.name
        if "worker" != user_roles:
            return redirect("/")
    else:
        return redirect("/")


menu = [
    {'url': '.templates', 'title': "шаблоны документов"},
    {'url': '.claim', 'title': "Заявки"},
    {'url': '.equipment', 'title': "Оборудованние"}
]


@user_router.route("/")
@login_required
def index():
    return render_template("user_main.html", menu=menu, title="главная")


@user_router.route("/templates", methods=["POST", "GET"])
@login_required
def templates():
    template_service = TemplatesService()
    if request.method == "GET":
        templates = [i.model_dump() for i in template_service.get_list_templates()]
        return render_template("download_template_page.html", menu=menu, templates=templates)


@user_router.route("/download_templates/<id_template>", methods=["GET"])
@login_required
def download_templates(id_template):
    template_service = TemplatesService()
    send_file_partial = template_service.get_file_to_download(int(id_template), send_file)
    return send_file_partial()


@user_router.route("/download_claim/<uuid_claim>", methods=["GET"])
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


@user_router.route("/claim/add/<int:id_template>", methods=["GET", "POST"])
@login_required
def create_claim(id_template):
    template_service = TemplatesService()
    equipment_service = EquipmentServices()
    claim_service = ClaimServices()
    if request.method == "GET":
        scheme = template_service.get_scheme_template(int(id_template))
        scheme = template_service.add_device_to_scheme(scheme)

        equipments = equipment_service.get_list_equipment()
        return render_template("form_document_page.html",
                               menu=menu,
                               form_scheme=scheme,
                               id_template=id_template,
                               equipments=equipments
                               )
    elif request.method == "POST":
        file = request.files['file']
        id_user = current_user.user.id
        equipment = equipment_service.get_by_uuid(request.form["select_equipment"])
        if file:
            abs_template, name = template_service.generate_document(
                request.form,
                file,
                int(id_template),
                current_user.user,
                equipment
            )
            claim_service.add_claim(f"{str(abs_template)}", request.form, id_user, equipment)
            return redirect(url_for(".claim"))


@user_router.route("/templates/add", methods=["POST"])
@login_required
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


@user_router.route("/claim", methods=["POST", "GET"])
@login_required
def claim():
    service = ClaimServices()
    if request.method == "GET":
        claims = service.get_list_claim_by_user(current_user.user.id)
        return render_template("claim_user_page.html", menu=menu, claims=claims)


@user_router.route("/claim/delete/<uuid_claim>", methods=["POST", "GET"])
@login_required
def delete_claim(uuid_claim):
    service = ClaimServices()
    if request.method == "GET":
        service.delete_claim(uuid_claim)
        claims = service.get_list_claim_by_user(current_user.user.id)
        return render_template("claim_user_page.html", menu=menu, claims=claims)


@user_router.route("/equipment", methods=["POST", "GET"])
@login_required
def equipment():
    service = EquipmentServices()
    if request.method == "GET":
        return render_template("equipment_user_page.html", menu=menu, equipments=service.get_list_equipment())


@user_router.route("/equipments/<uuid_equipments>/claim",  methods=["GET"])
@login_required
def claim_in_equipments(uuid_equipments):
    service = ClaimServices()
    if request.method == "GET":
        claims = service.get_list_claim_in_equipments(uuid_equipments)
        return render_template("claim_user_page.html", menu=menu, claims=claims)


@user_router.route('/claim/edit/', methods=['GET', 'POST'])
@user_router.route("/claim/edit/<uuid_claim>", methods=["POST", "GET"])
@login_required
def manage_claim(uuid_claim):
    service = ClaimServices()
    form = ClaimForm()
    if request.method == 'GET':
        claim = service.get_by_uuid(uuid_claim)
        if uuid_claim:
            form.description.data = claim.comment
        return render_template("claim_form_page.html",
                               menu=menu,
                               form=form,
                               claim=claim)
    if form.validate_on_submit():
        if uuid_claim:
            service.update_claim(uuid_claim, form)
        return redirect(url_for(".claim"))


@user_router.route("/claim/send/<uuid_claim>", methods=["POST", "GET"])
@login_required
def send_claim(uuid_claim):
    service = ClaimServices()
    if request.method == "GET":
        service.send_claim(uuid_claim, "under_consideration")
        return redirect(url_for(".claim"))




