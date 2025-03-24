from ..Models.User import GetUser
from ..Repository import UserRepository
from ..database import db, User
from ..Models.User import PostUser, GetRole
from ..Forms import UserForm

class UserService:
    def __init__(self):
        self.__user_repository: UserRepository = UserRepository(db.session)

    def get_list_users(self) -> list[GetUser]:
        return [GetUser.model_validate(i, from_attributes=True) for i in self.__user_repository.get_list_user()]

    def add_user(self, user: PostUser):
        self.__user_repository.add_user(user)

    def get_list_roles(self) -> list[GetRole] | None:
        return [GetRole.model_validate(i, from_attributes=True) for i in self.__user_repository.get_list_roles()]

    def delete_user(self, id_user: int):
        self.__user_repository.delete_user(id_user)

    def get_user(self, id_user: int) -> User:
        return self.__user_repository.get_user(id_user)

    def update_user(self, id_user: int, form: UserForm):
        user = self.__user_repository.get_user(id_user)

        role = self.__user_repository.get_role(form.id_role.data)

        if form.password.data:
            user.password = form.password.data

        user.name = form.name.data
        user.surname = form.surname.data
        user.patronymics = form.patronymics.data
        user.email = form.email.data
        user.job_title = form.job_title.data
        user.id_role = form.id_role.data

        self.__user_repository.update_user(user)