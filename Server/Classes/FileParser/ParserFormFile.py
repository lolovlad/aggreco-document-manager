from .XlsxFile import XlsxFile
from pathlib import Path
from ..Models.Fileschame import *


class ParserFormFile:
    def __init__(self, path_file: Path, file_schema: FileSchemas, file: XlsxFile):
        self.__path_file: Path = path_file
        self.__file: XlsxFile = file
        self.__file_schema: FileSchemas = file_schema
        self.__map_data: dict = {}

    @property
    def map_data(self) -> dict:
        return self.__map_data

    def parser(self):
        self.__file.read_file()
        for target_protocol in self.__file_schema.protocols:
            keys_value = {}

            self.__file.target_sheet_by_name(target_protocol.name)

            for table in target_protocol.tables:
                for cell in table.cells:
                    print(cell, self.__file.get_cell(cell.global_x, cell.global_y).value)
                    if keys_value.get(cell.text) is None:
                        keys_value[cell.text] = self.__file.get_cell(cell.global_x, cell.global_y).value
            self.__map_data[target_protocol.name] = keys_value
