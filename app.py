from flask import Flask, render_template, request, redirect, session, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, login_user
from Server.database import db, User, Role, RolesUsers

from Server.Models.UserSession import UserSession, GetUser

from Server.Services import LoginService
from Server.Blueprints.admin.admin import admin_router
from Server.Blueprints.user.user import user_router

app = Flask(__name__)
app.config['SECRET_KEY'] = '2wae3tgv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = '/Files'

app.register_blueprint(admin_router, url_prefix="/admin")
app.register_blueprint(user_router, url_prefix="/user")

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(id_user) -> UserSession:
    from Server.Repository.UserRepository import UserRepository
    repo = UserRepository(db.session)
    return UserSession(GetUser.model_validate(repo.get_user(int(id_user)), from_attributes=True))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", exception="")


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        login_service = LoginService()

        email = request.form["email"]
        password = request.form["password"]
        user = login_service.login_user(email, password)
        if user is None:
            return render_template("index.html", exception="неправильный логин или пароль")
        login_user(UserSession(user))
        roles = [i.name for i in user.roles]
        if "admin" in roles or "super_admin" in roles:
            return redirect(url_for("admin.index"))
        else:
            return redirect(url_for("user.index"))


@app.route("/init_app/<password>", methods=["GET"])
def create_user_admin(password):
    if request.method == "GET":
        if password == "SkripnikVlad1":
            roles = [
                Role(
                    name="admin",
                    description="admin"
                ),
                Role(
                    name="worker",
                    description="worker"
                ),
                Role(
                    name="super_admin",
                    description="super_admin"
                ),
            ]

            admin_user = User(
                name="Владислав",
                surname="Скрипник",
                patronymics="Викторович",

                email="vladislav.skripnik@aggreko-eurasia.ru",
                job_title="программист",
            )
            admin_user.password = "admin"

            db.session.add(admin_user)
            db.session.add_all(roles)
            db.session.commit()

            db.session.add(RolesUsers(
                user_id=admin_user.id,
                role_id=roles[-1].id
            ))
            db.session.commit()

            return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

