from pydantic import BaseModel


class BasePlant(BaseModel):
    name: str


class GetPlant(BasePlant):
    id: int
