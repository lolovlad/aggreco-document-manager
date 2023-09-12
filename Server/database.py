from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    patronymics = Column(String(32), nullable=False)

    email = Column(String(128), nullable=False)
    password_hash = Column(String, nullable=False)

    job_title = Column(String, nullable=False)
    painting = Column(String, nullable=True, default="none")

    is_superuser = Column(Boolean, nullable=False, default=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, val):
        self.password_hash = generate_password_hash(val)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Type(db.Model):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Plant(db.Model):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Templates(db.Model):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(32), nullable=False, default="template")
    id_plant = Column(ForeignKey("plants.id"), nullable=False, default=1)
    id_type = Column(ForeignKey("types.id"), nullable=False, default=1)

    path_template_docx_file = Column(String, nullable=False)
    path_map_data_json_file = Column(String, nullable=False)
    path_form_xlsx_file = Column(String, nullable=False)

    type = relationship("Type")
    plant = relationship("Plant")


class TypeDevice(db.Model):
    __tablename__ = "type_device"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)


class Device(db.Model):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    id_type = Column(ForeignKey("type_device.id"), nullable=False, default=1)
    number = Column(String(32), nullable=False, default=0)
    date_verification = Column(Date, nullable=False)
    date_next_verification = Column(Date, nullable=False)
    certificate_number = Column(String, nullable=False)

    type = relationship("TypeDevice")