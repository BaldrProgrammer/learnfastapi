from pydantic import Field, BaseModel, ConfigDict
from typing import List
from app.courses.schemas import SCourse


class SMajor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    major_name: str = Field(..., description='Название факультета')
    major_description: str = Field(..., description='Описание факультета')

    course: List[SCourse]


class SMajorAdd(BaseModel):
    major_name: str = Field(..., description='Название факультета')
    major_description: str = Field(..., description='Описание факультета')


class SMajorUpdDesc(BaseModel):
    major_name: str = Field(..., description='Название факультета')
    major_description: str = Field(None, description='Описание факультета')
