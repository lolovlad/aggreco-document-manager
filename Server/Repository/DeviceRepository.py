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