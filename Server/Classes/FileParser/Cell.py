from re import findall
from ..Models.Fileschame import CellSchemas, Size


class Cell:
    def __init__(self, left: int, top: int, right: int, bottom: int, text: str):
        self.__x: int = left + 1
        self.__y: int = top + 1
        self.__width: int = right - left
        self.__height: int = bottom - top
        self.__text: str = text
        self.__re: str = r'{{\w+}}'

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def text(self):
        return self.__text

    def is_merge_cell(self) -> bool:
        return self.__width > 1 or self.__height > 1

    def is_data_cell(self) -> bool:
        return len(findall(self.__re, self.__text)) > 0

    def get_schemas(self) -> CellSchemas:
        return CellSchemas(
            x=self.x,
            y=self.y,
            is_merge=self.is_merge_cell(),
            is_data=self.is_data_cell(),
            text=self.text,
            size=Size(
                width=self.width,
                height=self.height
            )
        )

    def __repr__(self):
        return f"{self.__text} coord: x-{self.__x} y-{self.__y}"