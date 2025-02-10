from pydantic import Field, BaseModel

class SMajorAdd(BaseModel):
    major_name: str = Field(..., description='Название факультета')
    major_description: str = Field(..., description='Описание факультета')
    count_students: int = Field(0, description='Количество студентов')
