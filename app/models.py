from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import date
from app.database import Base, int_pk, str_uniq, str_null_true


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]
    address: Mapped[str] = mapped_column(Text, nullable=False)
    enrollment_year: Mapped[int]
    special_notes: Mapped[str_null_true]
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), nullable=False)

    course: Mapped['Course'] = relationship('Course', back_populates='students')

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r}, "
                f"last_name={self.last_name!r})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "email": self.email,
            "address": self.address,
            "enrollment_year": self.enrollment_year,
            "special_notes": self.special_notes,
            "course_id": self.course_id
        }


class Major(Base):
    __tablename__ = 'majors'

    id: Mapped[int_pk]
    major_name: Mapped[str_uniq]
    major_description: Mapped[str_null_true]

    # Определяем отношения: один факультет может иметь много студентов
    course: Mapped[List['Course']] = relationship('Course', back_populates='major')

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, major_name={self.major_name!r})"

    def __repr__(self):
        return str(self)


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int_pk]
    year: Mapped[int]
    teacher_name: Mapped[str_uniq]
    special_course_notes: Mapped[str_null_true]
    major_id: Mapped[int] = mapped_column(ForeignKey('majors.id'), nullable=False)

    major: Mapped['Major'] = relationship('Major', back_populates='course')
    students: Mapped[List['Student']] = relationship('Student', back_populates='course')

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, year={self.year!r}, major_id={self.major_id})"

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'year': self.year,
            'teacher_name': self.teacher_name,
            'special_course_notes': self.special_course_notes,
            'major_id': self.major_id
        }
