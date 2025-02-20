from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from app.students.schemas import SStudent

class SCourse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    year: int = Field(..., description='Номер курса, т.е. год обучения')
    teacher_name: str = Field(..., min_length=1, max_length=50, description='Имя руководителя курса.')
    special_course_notes: Optional[str] = Field(None, max_length=300, description='Отличительные черты курса. Мах 300 символов')
    major_id: int = Field(..., ge=1, description='ID специальности курса.')

    students: List[SStudent]


class SCourseAdd(BaseModel):
    year: int = Field(..., description='Номер курса, т.е. год обучения')
    teacher_name: str = Field(..., min_length=1, max_length=50, description='Имя руководителя курса.')
    special_course_notes: Optional[str] = Field(None, max_length=300, description='Отличительные черты курса. Мах 300 символов')
    major_id: int = Field(..., ge=1, description='ID специальности курса.')
