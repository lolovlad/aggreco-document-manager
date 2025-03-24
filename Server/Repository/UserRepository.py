from sqlalchemy.orm import Session
from ..database import User, Role
from ..Models.User import PostUser


class UserRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get_user_by_email(self, email: str) -> User | None:
        user = self.__session.query(User).filter(User.email == email).first()
        return user

    def get_list_user(self) -> list[User] | None:
        return self.__session.query(User).all()

    def get_user(self, id_user: int) -> User | None:
        return self.__session.get(User, id_user)

    def get_list_roles(self) -> list[Role] | None:
        return self.__session.query(Role).all()

    def add_user(self, user: PostUser):
        user_entity = User(
            name=user.name,
            surname=user.surname,
            patronymics=user.patronymics,
            email=user.email,
            job_title=user.job_title,
            id_role=user.id_role
        )
        user_entity.password = user.password
        try:
            self.__session.add(user_entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def delete_user(self, id_user: int):
        try:
            user = self.get_user(id_user)
            self.__session.delete(user)
            self.__session.commit()
        except:
            self.__session.rollback()

    def get_role(self, id_role) -> Role | None:
        return self.__session.get(Role, id_role)

    def update_user(self, user: User):
        try:
            self.__session.add(user)
            self.__session.commit()
        except:
            self.__session.rollback()