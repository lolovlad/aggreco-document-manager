from ..Models.User import GetUser
from ..Repository import UserRepository
from ..database import db


class UserService:
    def __init__(self):
        self.__user_repository: UserRepository = UserRepository(db.session)

    def get_list_users(self) -> list[GetUser]:
        return [GetUser.model_validate(i, from_attributes=True) for i in self.__user_repository.get_list_by_superuser(False)]
