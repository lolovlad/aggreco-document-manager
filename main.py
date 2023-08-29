from pathlib import Path

from Classes.FileParser.ParserTempalteFile import ParserTemplateFile
from Classes.FileParser.ParserFormFile import ParserFormFile
from Classes.FileParser.JsonFile import JsonFile
from Classes.Models.Fileschame import FileSchemas


from docx import Document
from re import findall
from Classes.FileParser.FileParser import FileParser
from Classes.FileBuilder.BuilderXlsxFile import BuilderXlsxFile
from Classes.FileBuilder.BuilderDocxFile import BuilderDocxFile

from Classes.FileParser.DocxFile import DocxFile

from Classes.FileParser.XlsxFile import XlsxFile

path_file_json = Path("Files", "Docx", "Form1.json")
path_file_docx = Path("Files", "Docx", "Form1.docx")
path_file_xlsx = Path("Files", "Xlsx", "test.xlsx")

'''
parser = ParserTemplateFile(path_file_docx)
parser.parser()

builder_xlsx = BuilderXlsxFile(path_file_xlsx, parser.file_schema)

builder_xlsx.build()'''


json_map_data_path = Path("Files", "Xlsx", "test.json")
json_map_data_file = JsonFile(json_map_data_path)
json_map_data_file.read_file()

parser_exel = ParserFormFile(path_file_xlsx, FileSchemas.model_validate( json_map_data_file.scheme))
parser_exel.parser()

builder_docx = BuilderDocxFile(Path("Files", "Docx", "text_template.docx"), path_file_docx, parser_exel.map_data)
builder_docx.build()



