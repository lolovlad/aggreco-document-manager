from sqlalchemy.orm import Session
from ..database import User


class UserRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get_user_by_email(self, email: str) -> User | None:
        user = self.__session.query(User).filter(User.email == email).first()
        return user

    def get_list_by_superuser(self, is_superuser: bool) -> list[User] | None:
        return self.__session.query(User).filter(User.is_superuser == is_superuser).all()

    def get_user(self, id_user: int) -> User | None:
        return self.__session.get(User, id_user)
