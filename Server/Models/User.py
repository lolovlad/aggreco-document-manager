from pydantic import BaseModel


class RolesUsers(BaseModel):
    user_id: int
    role_id: int


class BaseRole(BaseModel):
    name: str
    description: str


class GetRole(BaseRole):
    id: int


class BaseUser(BaseModel):
    name: str
    surname: str
    patronymics: str
    email: str
    job_title: str
    painting: str


class GetUser(BaseUser):
    id: int
    roles: list[GetRole]


class PostUser(BaseUser):
    password: str
    id_role: int

