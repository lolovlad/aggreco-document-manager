from ..database import TypeDevice, Device
from sqlalchemy.orm import Session
from ..Models.Device import BaseDevice, BaseTypeDevice


class DeviceRepository:
    def __init__(self, session: Session):
        self.__session = session

    def get_list_type_device(self) -> list[TypeDevice] | None:
        return self.__session.query(TypeDevice).all()

    def get_list_device(self) -> list[Device] | None:
        return self.__session.query(Device).all()

    def get_device(self, id_device: int) -> Device | None:
        return self.__session.get(Device, id_device)

    def get_device_by_nuber(self, num: str) -> Device | None:
        return self.__session.query(Device).filter(Device.number == num).first()

    def add_device(self, device: BaseDevice):
        device_entity = Device()
        device_dict = device.model_dump()
        for key in device_dict:
            setattr(device_entity, key, device_dict[key])

        try:
            self.__session.add(device_entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def add_type_device(self, type_device: BaseTypeDevice):
        device_type_entity = TypeDevice()
        device_type_dict = type_device.model_dump()
        for key in device_type_dict:
            setattr(device_type_entity, key, device_type_dict[key])

        try:
            self.__session.add(device_type_entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def get_devices_by_type(self, type_device: str) -> list[Device] | None:
        try:
            id_type: TypeDevice = self.__session.query(TypeDevice).filter(TypeDevice.name == type_device).first()
            return self.__session.query(Device).filter(Device.id_type == id_type.id).all()
        except AttributeError:
            return []

    def delete_device(self, id_device: int):
        device = self.get_device(id_device)
        try:
            self.__session.delete(device)
            self.__session.commit()
        except:
            self.__session.rollback()

    def update(self, device: Device):
        try:
            self.__session.add(device)
            self.__session.commit()
        except:
            self.__session.rollback()