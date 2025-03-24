from ..Repository.DeviceRepository import DeviceRepository
from ..Models.Device import *
from ..database import db, Device

from datetime import datetime


class DeviceServices:
    def __init__(self):
        self.__device_repository: DeviceRepository = DeviceRepository(db.session)

    def get_list_device(self) -> list[GetDevice]:
        list_device = self.__device_repository.get_list_device()
        return [GetDevice.model_validate(entity, from_attributes=True) for entity in list_device]

    def get_list_type_device(self) -> list[GetTypeDevice]:
        list_type_device = self.__device_repository.get_list_type_device()
        return [GetTypeDevice.model_validate(entity, from_attributes=True) for entity in list_type_device]

    def add_device(self, name: str,
                   number: str,
                   date_verification: str,
                   date_next: str,
                   certificate_number: str,
                   id_type: int):

        device = BaseDevice(
            number=number,
            name=name,
            id_type=id_type,
            date_verification=datetime.strptime(str(date_verification), "%Y-%m-%d").date(),
            date_next_verification=datetime.strptime(str(date_next), "%Y-%m-%d").date(),
            certificate_number=certificate_number
        )
        self.__device_repository.add_device(device)

    def add_type_device(self, name: str):
        type_device = BaseTypeDevice(name=name)
        self.__device_repository.add_type_device(type_device)

    def get_device(self, id_device: int) -> Device:
        return self.__device_repository.get_device(id_device)

    def delete_device(self, id_device: int):
        self.__device_repository.delete_device(id_device)

    def update_device(self,
                      id_device: int,
                      name: str,
                      number: str,
                      date_verification: str,
                      date_next: str,
                      certificate_number: str,
                      id_type: int):
        device = self.__device_repository.get_device(id_device)
        device.name = name
        device.number = number
        device.date_verification = datetime.strptime(date_verification, "%Y-%m-%d").date()
        device.date_next_verification = datetime.strptime(date_next, "%Y-%m-%d").date()
        device.certificate_number = certificate_number
        device.id_type = id_type
        self.__device_repository.update(device)
