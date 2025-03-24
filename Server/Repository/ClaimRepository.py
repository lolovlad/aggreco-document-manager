from ..database import Claim, StateClaim, Equipment
from sqlalchemy.orm import Session


class ClaimRepository:
    def __init__(self, session: Session):
        self.__session = session

    def get_list_claim(self, state_claim: str = "all") -> list[Claim] | None:
        if state_claim == "all":
            return self.__session.query(Claim).all()
        else:
            return self.__session.query(Claim).join(StateClaim).filter(StateClaim.name == state_claim).all()

    def get_state_claim_by_name(self, name: str) -> StateClaim:
        return self.__session.query(StateClaim).filter(StateClaim.name == name).first()

    def get_list_claim_by_user(self, id_user: int) -> list[Claim]:
        return self.__session.query(Claim).filter(Claim.id_user == id_user).all()

    def get(self, id_claim: int) -> Claim:
        return self.__session.get(Claim, id_claim)

    def get_by_uuid(self, uuid_claim: str) -> Claim:
        return self.__session.query(Claim).filter(Claim.uuid == uuid_claim).first()

    def get_claim_by_uuid_equipment(self, uuid_equipment: str) -> list[Claim]:
        return self.__session.query(Claim).join(Equipment).filter(Equipment.uuid == uuid_equipment).all()

    def add(self, entity: Claim):
        try:
            self.__session.add(entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def update(self, entity: Claim):
        try:
            self.__session.add(entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def delete(self, uuid_equipment: str):
        entity = self.get_by_uuid(uuid_equipment)
        try:
            self.__session.delete(entity)
            self.__session.commit()
        except:
            self.__session.rollback()
