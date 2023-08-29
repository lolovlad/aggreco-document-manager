from .XlsxFile import XlsxFile
from pathlib import Path
from ..Models.Fileschame import *


class ParserFormFile:
    def __init__(self, path_file: Path, file_schema: FileSchemas, map_data: dict):
        self.__path_file: Path = path_file
        self.__file: XlsxFile = XlsxFile(path_file, file_schema)
        self.__map_data: dict = map_data

    @property
    def file_schema(self) -> FileSchemas:
        return self.__file.map_data

    @property
    def map_data(self):
        return self.__map_data

    def parser(self):
        for protocol_name in self.__map_data:
            target_sheet = self.__file.get_sheet_by_name(protocol_name)
            for value_name in self.__map_data[protocol_name]:
                coord = self.__map_data[protocol_name][value_name]
                self.__map_data[protocol_name][value_name] = target_sheet.cell(row=coord[1], column=coord[0]).value