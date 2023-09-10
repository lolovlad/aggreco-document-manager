from pydantic import BaseModel


class BaseType(BaseModel):
    name: str


class GetType(BaseType):
    id: int
