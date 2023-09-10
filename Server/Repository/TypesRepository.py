from sqlalchemy.orm import Session
from ..database import Type
from ..Models.Type import BaseType


class TypesRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get_list_types(self) -> list[Type] | None:
        types = self.__session.query(Type).all()
        return types

    def add_type(self, type_entity: BaseType):
        pass