from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    surname: str
    patronymics: str

    email: str

    job_title: str
    painting: str

    is_superuser: bool
