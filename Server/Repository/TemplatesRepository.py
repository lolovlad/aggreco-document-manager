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