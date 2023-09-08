from sqlalchemy.orm import Session
from ..database import User


class UserRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get_user_by_email(self, email: str) -> User | None:
        user = self.__session.query(User).filter(User.email == email).first()
        return user
