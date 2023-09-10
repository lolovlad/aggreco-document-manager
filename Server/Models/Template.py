from pydantic import BaseModel
from .Type import GetType
from .Plant import GetPlant


class BaseTemplate(BaseModel):
    name: str
    id_plant: int
    id_type: int

    path_template_docx_file: str
    path_map_data_json_file: str
    path_form_xlsx_file: str


class GetTemplate(BaseTemplate):
    id: int

    type: GetType
    plant: GetPlant