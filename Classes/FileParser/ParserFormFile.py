from .XlsxFile import XlsxFile
from pathlib import Path
from ..Models.Fileschame import *


class ParserFormFile:
    def __init__(self, path_file: Path, file_schema: FileSchemas):
        self.__path_file: Path = path_file
        self.__file: XlsxFile = XlsxFile(path_file, file_schema)
        self.__file_schema: FileSchemas = file_schema
        self.__map_data: dict = {}

    @property
    def file_schema(self) -> FileSchemas:
        return self.__file.map_data

    def parser(self):
        for target_protocol in self.__file_schema.protocols:
            keys_value = {}
            target_sheet = self.__file.get_sheet_by_name(target_protocol.name)

            for table in target_protocol.tables:
                for cell in table.cells:
                    keys_value[cell] =
                    coord = self.__map_data[protocol_name][value_name]
                    self.__map_data[protocol_name][value_name] = target_sheet.cell(row=coord[1], column=coord[0]).value

            self.__map_data[target_protocol.name] = keys_value