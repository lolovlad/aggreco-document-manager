from sqlalchemy.orm import Session
from ..Models.Template import BaseTemplate
from ..database import Templates


class TemplatesRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def add_template(self, template: BaseTemplate):
        dict_model = template.model_dump()
        template = Templates()
        for key in dict_model:
            setattr(template, key, dict_model[key])
        try:

            self.__session.add(template)
            self.__session.commit()
        except Exception:
            self.__session.rollback()

    def get_templates(self) -> list[Templates] | None:
        return self.__session.query(Templates).all()

    def get_template(self, id_template: int) -> Templates | None:
        return self.__session.get(Templates, id_template)

    def delete_template(self, id_temp: int):
        template = self.get_template(id_temp)
        try:
            self.__session.delete(template)
            self.__session.commit()
        except:
            self.__session.rollback()



