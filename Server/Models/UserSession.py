from .User import GetUser


class UserSession:
    def __init__(self, user: GetUser):
        self.__user: GetUser = user

    @property
    def user(self):
        return self.__user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.id)