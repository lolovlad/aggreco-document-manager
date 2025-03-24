from pydantic import BaseModel


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
    id_role: int


class GetUser(BaseUser):
    id: int
    role: GetRole


class PostUser(BaseUser):
    password: str
    id_role: int

