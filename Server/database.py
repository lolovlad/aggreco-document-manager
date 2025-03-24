import datetime
from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = "roles"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    patronymics = Column(String(32), nullable=False)

    email = Column(String(128), nullable=False)
    password_hash = Column(String, nullable=False)

    job_title = Column(String, nullable=False)
    painting = Column(String, nullable=True, default="none")
    id_role = Column(ForeignKey("roles.id"))
    role = relationship('Role')

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
    date_verification = Column(Date, nullable=True, default=None)
    date_next_verification = Column(Date, nullable=True, default=None)
    certificate_number = Column(String, nullable=True, default="-")

    type = relationship("TypeDevice")


class TypeEquipment(db.Model):
    __tablename__ = "type_equipment"
    id = Column(Integer, autoincrement=True, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(128), nullable=True)


class Equipment(db.Model):
    __tablename__ = "equipment"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String, unique=True)
    code = Column(String, nullable=False, unique=True)
    id_type = Column(ForeignKey("type_equipment.id"))
    type = relationship("TypeEquipment", lazy="joined")
    description = Column(Text, nullable=True)

    is_delite = Column(Boolean, default=False, nullable=True, server_default="False")


class StateClaim(db.Model):
    __tablename__ = "state_claim"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    description = Column(String(128), nullable=True)


class Claim(db.Model):
    __tablename__ = "claim"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String, unique=True)

    datetime = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now)

    id_state_claim = Column(ForeignKey("state_claim.id"))
    state_claim = relationship(StateClaim, lazy="joined")

    id_user = Column(ForeignKey("users.id"))
    user = relationship(User, lazy="joined")

    main_document = Column(String, nullable=True)

    comment = Column(Text, nullable=True, default="Нет")

    id_equipment = Column(ForeignKey("equipment.id"))
    equipment = relationship(Equipment, lazy="joined")