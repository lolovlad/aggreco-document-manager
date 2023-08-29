from .BuilderFile import BuilderFile

from ..FileParser.XlsxFile import XlsxFile
from ..FileParser.JsonFile import JsonFile

from ..Models.Fileschame import *

from copy import deepcopy
from pathlib import Path
from re import findall


class BuilderXlsxFile(BuilderFile):
    def __init__(self, path_file: Path, file_schemas: FileSchemas):
        self.__file: XlsxFile = XlsxFile(path_file, file_schemas)
        self.__file_schemas: FileSchemas = file_schemas
        self.__json_data_schema: dict = {}
        self.__path_file: Path = path_file

    def build(self):
        for id_protocol, target_protocol in enumerate(self.__file_schemas.protocols):
            self.__file.create_sheet(target_protocol)

            bias = 0
            last_y_cell = 0

            self.__json_data_schema[target_protocol.name] = {}

            for id_table, table in enumerate(target_protocol.tables):
                for id_cell, cell in enumerate(table.cells):

                    x = cell.x
                    y = cell.y + bias + last_y_cell

                    if cell.is_merge:
                        self.__create_merge_cell(x, y, cell.size, cell.text)
                        self.delete_cell(id_protocol, id_table, id_cell)
                    elif cell.is_data:
                        self.__create_data_cell(x, y, cell.text)

                        cell.global_x = x
                        cell.global_y = y

                    else:
                        self.delete_cell(id_protocol, id_table, id_cell)
                        self.__file.create_cell(x, y, cell.text)

                last_y_cell = y - 2
                bias += 10
        self.save_file()

    def delete_cell(self, id_protocol: int, id_table: int, id_cell: int):
        self.__file_schemas.protocols[id_protocol].tables[id_table].cells[id_cell] = None

    def __get_json_data_schema(self, sheet, key):
        return self.__json_data_schema[sheet][key]

    def __is_cell_ref(self, text: str):
        coord = self.__json_data_schema[self.__file.get_title_sheet()].get(text)
        return coord is not None

    def __create_data_cell(self, x: int, y: int, text: str):
        text = self.__get_text_in_cell(text)
        if self.__is_cell_ref(text):
            coord_ref_cell = self.__get_json_data_schema(self.__file.get_title_sheet(), text)
            text = self.__create_ref_to_cell(coord_ref_cell[0], coord_ref_cell[1])
        else:
            self.__add_to_schema(x, y, text)
            self.__file.add_fill_cell(x, y)
            text = ""
        self.__file.create_cell(x, y, text)

    def __create_merge_cell(self, x: int, y: int, size: Size, text: str):
        try:
            self.__file.create_cell(x, y, text)

            end_x = x + size.width - 1
            end_y = y + size.height - 1

            self.__file.merge_cells(x, y, end_x, end_y)
        except AttributeError:
            pass

    def __add_to_schema(self, x: int, y: int, text: str):
        title_sheet = self.__file.get_title_sheet()
        self.__json_data_schema[title_sheet][self.__get_text_in_cell(text)] = (x, y)

    def __create_ref_to_cell(self, x: int, y: int) -> str:
        coord_cell = self.__file.get_coord_cell(x, y)
        return f"={coord_cell}"

    def __get_text_in_cell(self, text) -> str:
        text_list = findall(r"\w+", text)
        return text_list[0]

    def save_file(self):
        self.__file.save()
        json_file = JsonFile(self.__path_file, self.__file_schemas.model_dump())
        json_file.save_file()
