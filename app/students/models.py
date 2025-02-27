from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date


# создаем модель таблицы студентов
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
