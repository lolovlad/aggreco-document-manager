from ..Repository import TypesRepository, PlantRepository, TemplatesRepository
from ..database import db
from ..Models.Type import BaseType, GetType
from ..Models.Plant import GetPlant
from ..Models.Template import BaseTemplate
from ..Classes.FileParser.ParserTempalteFile import ParserTemplateFile
from ..Classes.FileBuilder.BuilderXlsxFile import BuilderXlsxFile


from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from pathlib import Path
from secrets import choice

from string import ascii_letters, digits


class TemplatesService:
    def __init__(self):
        self.__types_repository: TypesRepository = TypesRepository(db.session)
        self.__plants_repository: PlantRepository = PlantRepository(db.session)
        self.__template_repository: TemplatesRepository = TemplatesRepository(db.session)

    def __get_name_file(self, extend: str) -> str:
        res = ''.join(choice(ascii_letters + digits) for x in range(15))
        return f"{res}.{extend}"

    def __save_file(self, file: FileStorage, path: Path):
        file.save(path)

    def get_list_types(self) -> list[GetType]:
        types = self.__types_repository.get_list_types()
        if types:
            return [GetType.model_validate(i, from_attributes=True) for i in types]

    def get_list_plants(self) -> list[GetPlant]:
        plants = self.__plants_repository.get_list_plants()
        if plants:
            return [GetPlant.model_validate(i, from_attributes=True) for i in plants]

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