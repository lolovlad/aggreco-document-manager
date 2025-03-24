from ..Repository.EquipmentRepository import EquipmentRepository
from ..database import db, Equipment, TypeEquipment
from ..Forms import EquipmentForm

from datetime import datetime
from uuid import uuid4


class EquipmentServices:
    def __init__(self):
        self.__repository: EquipmentRepository = EquipmentRepository(db.session)

    def get_list_equipment(self) -> list[Equipment]:
        list_equip = self.__repository.get_list_equipments()
        return list_equip

    def get_list_type_equipments(self) -> list[TypeEquipment]:
        list_type_equip = self.__repository.get_list_type_equipment()
        return list_type_equip

    def add_equipments(self, form: EquipmentForm):
        entity = Equipment(
            code=form.code.data,
            id_type=int(form.type.data),
            description=form.description.data,
            uuid=str(uuid4())
        )
        self.__repository.add(entity)

    def update_equipment(self, uuid_equipment: str, form: EquipmentForm):
        entity = self.__repository.get_by_uuid(uuid_equipment)
        entity.code = form.code.data
        entity.id_type = int(form.type.data)
        entity.description = form.description.data

        self.__repository.update(entity)

    def get_by_uuid(self, uuid_equipment: str):
        return self.__repository.get_by_uuid(uuid_equipment)

    def delete_equipment(self,  uuid_equipment: str):
        self.__repository.delete(uuid_equipment)
