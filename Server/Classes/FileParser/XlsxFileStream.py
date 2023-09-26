from io import BytesIO
from .XlsxFile import XlsxFile
from openpyxl import load_workbook
from ..Models.Fileschame import *


class XlsxFileStream(XlsxFile):
    def __init__(self, file, map_data: FileSchemas):
        super().__init__(path_file=None, map_data=map_data)
        self._stream_file = file.stream

    def read_file(self):
        self._file = load_workbook(self._stream_file)