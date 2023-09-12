import datetime

from pydantic import BaseModel


class BaseTypeDevice(BaseModel):
    name: str


class GetTypeDevice(BaseTypeDevice):
    id: int


class BaseDevice(BaseModel):
    name: str
    id_type: int
    number: str
    date_verification: datetime.date
    date_next_verification: datetime.date
    certificate_number: str


class GetDevice(BaseDevice):
    id: int
    type: GetTypeDevice
