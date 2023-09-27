from ..Models.User import GetUser
from ..Repository import UserRepository
from ..database import db
from ..Models.User import PostUser, GetRole


class UserService:
    def __init__(self):
        self.__user_repository: UserRepository = UserRepository(db.session)

    def get_list_users(self) -> list[GetUser]:
        return [GetUser.model_validate(i, from_attributes=True) for i in self.__user_repository.get_list_user()]

    def add_user(self, form: dict):
        user = PostUser(
            name=form["name"],
            surname=form["surname"],
            patronymics=form["patronymics"],
            email=form["email"],
            job_title=form["job_title"],
            painting="",
            password=form["password"],
            id_role=int(form["id_role"])
        )
        self.__user_repository.add_user(user)

    def get_list_roles(self) -> list[GetRole] | None:
        return [GetRole.model_validate(i, from_attributes=True) for i in self.__user_repository.get_list_roles()]

    def delete_user(self, id_user: int):
        self.__user_repository.delete_user(id_user)