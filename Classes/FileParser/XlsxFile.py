from openpyxl import Workbook, load_workbook
from .File import File
from pathlib import Path

from ..Models.Fileschame import FileSchemas, TableSchemas


class XlsxFile(File):
    def __init__(self, path_file: Path, map_data: FileSchemas):
        self.__path_file: Path = path_file
        self.__file: Workbook = load_workbook(filename=self.__path_file)
        self.__map_data: FileSchemas = map_data
        self.__active_sheet = None

    @property
    def map_data(self):
        return self.__map_data

    def render(self, schemas: dict):
        pass

    def is_table_schema(self, table, re: str):
        pass

    def get_all_parser_table_in_file(self) -> list[TableSchemas]:
        list_tables = []
        for protocols in self.__map_data.protocols:
            list_tables += protocols.tables
        return list_tables

    def get_list_cells(self, table):
        pass

    def get_sheet_by_name(self, name: str):
        return self.__file.get_sheet_by_name(name)

