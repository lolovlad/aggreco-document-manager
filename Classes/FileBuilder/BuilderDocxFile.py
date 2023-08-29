from docxtpl import DocxTemplate
from .BuilderFile import BuilderFile

from pathlib import Path


class BuilderDocxFile(BuilderFile):
    def __init__(self, path_file: Path, template_path_file: Path, map_data: dict):
        self.__path_file: Path = path_file
        self.__template_path_file: Path = template_path_file
        self.__map_data: dict = map_data

    def build(self):
        self.merge_map_dict()
        file = DocxTemplate(self.__template_path_file)
        file.render(self.__map_data)
        file.save(self.__path_file)

    def merge_map_dict(self):
        new_map_data = {}
        for name_protocol in self.__map_data:
            for val in self.__map_data[name_protocol]:
                new_map_data[val] = self.__map_data[name_protocol][val]
        self.__map_data = new_map_data
