from sqlalchemy.orm import Session
from ..database import Plant
from ..Models.Plant import BasePlant


class PlantRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get_list_plants(self) -> list[Plant] | None:
        plants = self.__session.query(Plant).all()
        return plants

    def add_plant(self, plant_entity: BasePlant):
        pass