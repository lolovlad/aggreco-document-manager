from .DocxFile import DocxFile
from pathlib import Path
from ..Models.Fileschame import *
from .Table import Table
import json


class ParserTemplateFile:
    def __init__(self, path_file: Path, re_end_table: str = "НаименованиеИОиИС"):
        self.__path_file: Path = path_file
        self.__file: DocxFile = DocxFile(path_file)
        self.__map_data: dict = {}
        self.__skip_top_table: int = 1
        self.__skip_bottom_table: int = 3
        self.__re_end_table: str = re_end_table
        self.__file_schema = FileSchemas()

    @property
    def file_schema(self):
        return self.__file_schema

    @property
    def map_data(self):
        return self.__map_data

    def parser(self):
        id_protocol = 1
        tables = self.__file.get_all_parser_table_in_file(r'{{\w+}}')
        tables_in_protocol = []

        index_table = 1 + self.__skip_top_table

        while index_table < len(tables):
            table = tables[index_table]
            if self.__is_end_protocol(table[0][0]):
                table_equipment = table
                table_workers = tables[index_table + 2]

                key_remark = self.__get_key_remark_field(tables[index_table + 1])

                protocol = self.__create_protocol(f"{id_protocol}",
                                                  tables_in_protocol,
                                                  table_equipment,
                                                  table_workers,
                                                  key_remark)

                id_protocol += 1
                tables_in_protocol.clear()
                index_table += (self.__skip_bottom_table + self.__skip_top_table)
                self.__file_schema.protocols.append(protocol)
            else:
                tables_in_protocol.append(table)
                index_table += 1

    def __get_key_remark_field(self, table: Table):
        return table[1][1].text[2:-2]


    def __is_end_protocol(self, cell):
        search_str = "".join(cell.text.split())
        return len(cell.text) > 0 and search_str == self.__re_end_table

    def __get_list_equipment(self, table: Table) -> list[Equipment]:
        start_row = 2
        list_equipment = []
        for row in range(start_row, table.row_count):
            list_equipment.append(Equipment(
                name=table[row][0].text,
                type_equip=table[row][1].text,
                error=table[row][2].text,
                number=table[row][3].text,
                certificate=table[row][4].text,
                data_start=table[row][5].text,
                data_end=table[row][6].text,
            ))
        return list_equipment

    def __create_protocol(self, name, tables, table_equipment, table_workers, remark: str) -> Protocol:
        list_equipment = self.__get_list_equipment(table_equipment)
        protocol = Protocol(
            name=name,
            tables=[tb.get_schemas() for tb in tables],
            list_equipment=list_equipment,
            remark=remark
        )
        protocol.list_workers = self.__get_list_workers(table_workers)
        return protocol

    def __get_list_workers(self, table: Table):
        list_workers = []
        for row in range(table.row_count):
            if table[row][0].is_data_cell():
                list_workers.append(Workers())
        if len(list_workers) == 0:
            raise Exception("this table is not workers")
        else:
            return list_workers