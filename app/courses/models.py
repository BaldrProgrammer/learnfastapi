from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.database import Base, int_pk, str_uniq, str_null_true

class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int_pk]
    year: Mapped[int]
    teacher_name: Mapped[str_uniq]
    special_course_notes: Mapped[str_null_true]
    major_id: Mapped[int] = mapped_column(ForeignKey('majors.id'), nullable=False)

    major: Mapped['Major'] = relationship('Major', back_populates='course')
    students: Mapped[List['Student']] = relationship('Student', back_populates='course')
