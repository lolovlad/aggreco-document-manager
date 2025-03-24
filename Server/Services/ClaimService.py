from ..Repository.ClaimRepository import ClaimRepository
from ..database import db, Claim, StateClaim, Equipment
from ..Forms import ClaimForm

from datetime import datetime
from uuid import uuid4
from os import remove
from pathlib import Path
from secrets import choice
from string import ascii_letters, digits


class ClaimServices:
    def __init__(self):
        self.__repository: ClaimRepository = ClaimRepository(db.session)

    def get_list_claim(self, state_claim: str = "all") -> list[Claim]:
        list_claim = self.__repository.get_list_claim(state_claim)
        return list_claim

    def get_list_claim_by_user(self, id_user: int) -> list[Claim]:
        list_claim = self.__repository.get_list_claim_by_user(id_user)
        return list_claim

    def add_claim(self, file: str, form: dict, id_user: int, equipment: Equipment):
        start_state = self.__repository.get_state_claim_by_name("draft")

        claim = Claim(
            uuid=str(uuid4()),
            id_state_claim=start_state.id,
            id_user=id_user,
            main_document=file,
            id_equipment=equipment.id
        )
        self.__repository.add(claim)

    def __delete_file(self, file_name: str):
        try:
            remove(Path(file_name))
        except OSError:
            pass

    def __get_name_file(self, extend: str) -> str:
        res = ''.join(choice(ascii_letters + digits) for x in range(15))
        return f"{res}.{extend}"

    def update_claim(self, uuid_claim: str, form: ClaimForm):
        claim = self.__repository.get_by_uuid(uuid_claim)
        if form.file.data:
            self.__delete_file(claim.main_document)
            name_main_file = self.__get_name_file(claim.main_document.split(".")[-1])
            form.file.data.save(Path("File", name_main_file))
            claim.main_document = str(Path("File", name_main_file))
        claim.comment = form.description.data
        self.__repository.update(claim)

    def get_by_uuid(self, uuid_claim: str):
        return self.__repository.get_by_uuid(uuid_claim)

    def delete_claim(self, uuid_claim: str):
        claim = self.get_by_uuid(uuid_claim)
        try:
            remove(Path("Files", claim.main_document).absolute())
        except Exception:
            pass
        self.__repository.delete(uuid_claim)

    def send_claim(self, uuid_claim: str, state_claim: str):
        entity_state_claim = self.__repository.get_state_claim_by_name(state_claim)
        claim = self.__repository.get_by_uuid(uuid_claim)

        claim.id_state_claim = entity_state_claim.id
        self.__repository.update(claim)

    def get_list_claim_in_equipments(self, uuid_equipment: str) -> list[Claim]:
        claims = self.__repository.get_claim_by_uuid_equipment(uuid_equipment)
        return claims
