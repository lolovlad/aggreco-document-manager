import os

from ..Repository import TypesRepository, PlantRepository, TemplatesRepository, DeviceRepository, UserRepository
from ..database import db
from ..Models.Type import BaseType, GetType
from ..Models.Plant import GetPlant
from ..Models.Template import BaseTemplate, GetTemplate
from ..Models.User import GetUser
from ..Classes.FileParser.ParserTempalteFile import ParserTemplateFile
from ..Classes.FileBuilder.BuilderXlsxFile import BuilderXlsxFile
from ..Classes.FileBuilder.BuilderDocxFile import BuilderDocxFile
from ..Classes.FileParser.ParserFormFile import ParserFormFile
from ..Classes.FileParser.JsonFile import JsonFile
from ..Classes.Models.Fileschame import FileSchemas
from ..Classes.FileParser.XlsxFileStream import XlsxFileStream


from werkzeug.datastructures import FileStorage
from pathlib import Path
from secrets import choice
from string import ascii_letters, digits
from functools import partial
from os import remove
from datetime import datetime
from ..database import Equipment


class TemplatesService:
    def __init__(self):
        self.__types_repository: TypesRepository = TypesRepository(db.session)
        self.__plants_repository: PlantRepository = PlantRepository(db.session)
        self.__template_repository: TemplatesRepository = TemplatesRepository(db.session)
        self.__device_repository: DeviceRepository = DeviceRepository(db.session)
        self.__user_repository: UserRepository = UserRepository(db.session)

        self.__name_fild_user = "user"

    def __get_name_file(self, extend: str) -> str:
        res = ''.join(choice(ascii_letters + digits) for x in range(15))
        return f"{res}.{extend}"

    def __save_file(self, file: FileStorage, path: Path):
        file.save(path)

    def get_list_types(self) -> list[GetType]:
        types = self.__types_repository.get_list_types()
        if types:
            return [GetType.model_validate(i, from_attributes=True) for i in types]
        return []

    def get_list_plants(self) -> list[GetPlant]:
        plants = self.__plants_repository.get_list_plants()
        if plants:
            return [GetPlant.model_validate(i, from_attributes=True) for i in plants]
        return []

    def get_list_templates(self) -> list[GetTemplate]:
        templates = self.__template_repository.get_templates()
        if templates:
            return [GetTemplate.model_validate(i, from_attributes=True) for i in templates]
        return []

    def add_template(self, name_template: str, type_template: int, plant: int, file: FileStorage):
        name_file_docx = self.__get_name_file("docx")
        name_file_exel = self.__get_name_file("xlsx")

        path_file_docx = Path("Files", name_file_docx)
        path_file_json = Path("Files", name_file_exel.split(".")[0] + ".json")
        path_file_exel = Path("Files", name_file_exel)

        self.__save_file(file, path_file_docx)

        parser_template = ParserTemplateFile(path_file_docx)
        parser_template.parser()

        builder_file = BuilderXlsxFile(path_file_exel, parser_template.file_schema)
        builder_file.build()

        template_model = BaseTemplate(
            name=name_template,
            id_plant=plant,
            id_type=type_template,
            path_template_docx_file=str(path_file_docx),
            path_map_data_json_file=str(path_file_json),
            path_form_xlsx_file=str(path_file_exel)
        )

        self.__template_repository.add_template(template_model)

    def get_file_to_download(self, id_template: int, funct_senf_file):
        template = self.__template_repository.get_template(id_template)

        path_file_exel = Path(template.path_form_xlsx_file)

        return partial(funct_senf_file,
                       path_or_file=path_file_exel.absolute(),
                       download_name=f"{template.name}_{template.type.name}_{template.plant.name}{path_file_exel.suffix}",
                       as_attachment=True)

    def get_scheme_template(self, id_template: int) -> dict:
        template = self.__template_repository.get_template(id_template)
        scheme = JsonFile(Path(template.path_map_data_json_file))
        scheme.read_file()
        return scheme.scheme

    def add_device_to_scheme(self, scheme_template: dict) -> dict:
        for protocol in scheme_template["protocols"]:
            for equip in protocol["list_equipment"]:
                equip["num_device"] = [{"id": i.id, "num": i.number} for i in self.__device_repository.get_devices_by_type(equip["type_equip"])]
        return scheme_template

    def generate_document(self,
                          form: dict,
                          file: FileStorage,
                          id_template: int,
                          user: GetUser,
                          equipment: Equipment):
        path_exel_data = self.__save_file_form(file)

        entity_template = self.__template_repository.get_template(id_template)

        map_data = {}

        scheme = self.get_scheme_template(id_template)

        self.__add_equip(scheme, form, map_data)
        self.__add_date(map_data, form["date"])
        map_data["user"] = user.model_dump()

        map_data["equipment"] = {"name", equipment.code}
        file_scheme = FileSchemas.model_validate(scheme)

        parser_file_form = ParserFormFile(path_exel_data, file_scheme, XlsxFileStream(file, file_scheme))
        parser_file_form.parser()

        path_file_template = Path("Files", "", self.__get_name_file("docx"))

        builder = BuilderDocxFile(path_file_template,
                                  Path(entity_template.path_template_docx_file),
                                  parser_file_form.map_data)
        builder.build(map_data)

        remove(path_exel_data.absolute())

        return path_file_template, f"{entity_template.name}_{entity_template.type.name}_{entity_template.plant.name}{path_file_template.suffix}"

    def __add_equip(self, scheme: dict, form: dict, map_data: dict):
        equipments = self.__get_equipment(scheme)

        for i, protocol in enumerate(scheme["protocols"]):
            map_data[protocol["remark"]] = form[protocol["remark"]]

            for j, equip in enumerate(protocol["list_equipment"]):
                number = equip["number"]
                try:
                    device = self.__device_repository.get_device(form[equip["number"]])

                    map_data[number] = device.number
                    map_data[equip["certificate"]] = device.certificate_number
                    map_data[equip["data_start"]] = device.date_verification.strftime("%d.%m.%Y")
                    map_data[equip["data_end"]] = device.date_next_verification.strftime("%d.%m.%Y")
                except Exception:
                    map_data[number] = {
                        "certificate": "",
                        "data_start": "",
                        "data_end": ""
                    }

        return map_data

    def __get_equipment(self, scheme: dict) -> dict:
        new_quip = {}
        for i, protocol in enumerate(scheme["protocols"]):
            new_quip[i] = {}
            for j, equip in enumerate(protocol["list_equipment"]):
                new_quip[i][j] = equip["number"]
        return new_quip

    def __save_file_form(self, file: FileStorage) -> Path:
        name_file_exel = self.__get_name_file("xlsx")
        path_file_exel = Path("Files", name_file_exel)
        self.__save_file(file, path_file_exel)
        return path_file_exel

    def __add_date(self, map_data: dict, date: str):
        date = datetime.strptime(date, "%Y-%m-%d").date()
        map_data["date"] = {
            "d": date.day if date.day > 9 else f"0{date.day}",
            "y": date.year,
            "m": date.month if date.month > 9 else f"0{date.month}",
            "full": date.strftime("%d.%m.%Y")
        }

    def get_template(self, id_temp: int):
        return self.__template_repository.get_template(id_temp)

    def update_template(self, id_template: int, name_template: str, type_template: int, plant: int, file: FileStorage | None):
        template_entity = self.__template_repository.get_template(id_template)
        if file:
            self.__delete_file(template_entity.path_template_docx_file)
            self.__delete_file(template_entity.path_form_xlsx_file)
            self.__delete_file(template_entity.path_map_data_json_file)

            name_file_docx = self.__get_name_file("docx")
            name_file_exel = self.__get_name_file("xlsx")

            path_file_docx = Path("Files", name_file_docx)
            path_file_json = Path("Files", name_file_exel.split(".")[0] + ".json")
            path_file_exel = Path("Files", name_file_exel)

            self.__save_file(file, path_file_docx)

            parser_template = ParserTemplateFile(path_file_docx)
            parser_template.parser()

            builder_file = BuilderXlsxFile(path_file_exel, parser_template.file_schema)
            builder_file.build()

            template_entity.path_template_docx_file = str(path_file_docx)
            template_entity.path_map_data_json_file = str(path_file_json)
            template_entity.path_form_xlsx_file = str(path_file_exel)

        template_entity.name = name_template
        template_entity.id_plant = plant
        template_entity.id_type = type_template

        print(template_entity.name)
        self.__template_repository.update_template(template_entity)

    def __delete_file(self, file_name: str):
        try:
            os.remove(Path(file_name))
        except OSError:
            pass

    def delete_template(self, id_temp: int):
        template_entity = self.__template_repository.get_template(id_temp)
        self.__delete_file(template_entity.path_template_docx_file)
        self.__delete_file(template_entity.path_form_xlsx_file)
        self.__delete_file(template_entity.path_map_data_json_file)
        self.__template_repository.delete_template(id_temp)

    #map_data[i][device.type.name] = {
    #    "certificate": device.certificate_number,
    #    "data_start": device.date_verification.strftime("%d.%m.%Y"),
    #    "data_end": device.date_next_verification.strftime("%d.%m.%Y")
    #}
    #except Exception:
    #map_data[i][equip["type_equip"]] = {
    #    "certificate": "",
    #    "data_start": "",
    #    "data_end": ""
    #}