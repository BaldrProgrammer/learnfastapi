from pydantic import Field, BaseModel, ConfigDict


class SMajor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    major_name: str = Field(..., description='Название факультета')
    major_description: str = Field(..., description='Описание факультета')
    count_students: int = Field(0, description='Количество студентов')


class SMajorAdd(BaseModel):
    major_name: str = Field(..., description='Название факультета')
    major_description: str = Field(..., description='Описание факультета')
    count_students: int = Field(0, description='Количество студентов')


class SMajorUpdDesc(BaseModel):
    major_name: str = Field(..., description='Название факультета')
    major_description: str = Field(None, description='Описание факультета')
