from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Server.database import db, User, Role, StateClaim
from flask_wtf.csrf import CSRFProtect

from Server.Models.UserSession import UserSession, GetUser

from Server.Services import LoginService
from Server.Blueprints.admin.admin import admin_router
from Server.Blueprints.user.user import user_router
from Server.Forms import LoginForm

from pathlib import Path

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


@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if current_user.is_authenticated:
        user_roles = current_user.user.role.name
        if "worker" == user_roles:
            return redirect(url_for("user.index"))
        else:
            return redirect(url_for("admin.index"))
    if form.validate_on_submit():
        login_service = LoginService()

        email = form.email.data
        password = form.password.data
        user = login_service.login_user(email, password)
        if user is None:
            return render_template("index.html", exception="неправильный логин или пароль", form=form)
        login_user(UserSession(user))
        role = user.role.name
        if "admin" == role or "super_admin" == role:
            return redirect(url_for("admin.index"))
        else:
            return redirect(url_for("user.index"))
    else:
        return render_template("index.html", exception="", form=form)


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
            state_claim = [
                StateClaim(
                    name="under_consideration",
                    description="На рассмотрении"
                ),
                StateClaim(
                    name="under_development",
                    description="На доработку"
                ),
                StateClaim(
                    name="accepted",
                    description="Принято"
                ),
                StateClaim(
                    name="draft",
                    description="Черновик"
                ),
            ]
            db.session.add_all(state_claim)
            db.session.commit()
            db.session.add_all(roles)
            admin_user = User(
                name="Владислав",
                surname="Скрипник",
                patronymics="Викторович",

                email="vladislav.skripnik@aggreko-eurasia.ru",
                job_title="программист",
                id_role=3
            )
            admin_user.password = "admin"

            db.session.add(admin_user)
            db.session.commit()
            return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

