from flask import Flask, render_template, request, redirect, session, url_for
from flask_migrate import Migrate
from Server.database import db

from Server.Services import LoginService
from Server.Exeptions import PasswordValidException, UserExistException
from Server.Blueprints.admin.admin import admin_router

app = Flask(__name__)
app.config['SECRET_KEY'] = '2wae3tgv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = '/Files'

app.register_blueprint(admin_router, url_prefix="/admin")

db.init_app(app)


migrate = Migrate(app, db)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", exception="")


@app.route("/login", methods=["POST"])
def login_user():
    if request.method == "POST":
        login_service = LoginService()

        email = request.form["email"]
        password = request.form["password"]
        user = login_service.login_user(email, password)
        if user is None:
            return render_template("index.html", exception="неправильный логин или пароль")
        session["user"] = user.model_dump()
        if user.is_superuser:
            return redirect(url_for("admin.index"))


@app.route("/create_user", methods=["GET"])
def create_user():
    if request.method == "GET":
        from Server.database import db, User

        user = User(
            name="admin",
            surname="admin",
            patronymics="admin",

            email="lll-ooo-200@mail.ru",
            job_title="admin",
            is_superuser=True
        )

        user.password = "admin"
        db.session.add(user)
        db.session.commit()

        redirect("index")


if __name__ == "__main__":
    app.run(debug=True)

