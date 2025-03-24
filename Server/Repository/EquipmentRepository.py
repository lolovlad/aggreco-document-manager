from ..database import Equipment, TypeEquipment
from sqlalchemy.orm import Session


class EquipmentRepository:
    def __init__(self, session: Session):
        self.__session = session

    def get_list_type_equipment(self) -> list[TypeEquipment] | None:
        return self.__session.query(TypeEquipment).all()

    def get_list_equipments(self) -> list[Equipment] | None:
        return self.__session.query(Equipment).filter(Equipment.is_delite == False).all()

    def get(self, id_equipment: int) -> Equipment:
        return self.__session.get(Equipment, id_equipment)

    def get_by_uuid(self, uuid_equipments: str) -> Equipment:
        return self.__session.query(Equipment).filter(Equipment.uuid == uuid_equipments).first()

    def add(self, equipment: Equipment):
        try:
            self.__session.add(equipment)
            self.__session.commit()
        except:
            self.__session.rollback()

    def update(self, equipment: Equipment):
        try:
            self.__session.add(equipment)
            self.__session.commit()
        except:
            self.__session.rollback()

    def delete(self, uuid_equipment: str):
        entity = self.get_by_uuid(uuid_equipment)
        entity.is_delite = True
        self.update(entity)
