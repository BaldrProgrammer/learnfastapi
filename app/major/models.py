from sqlalchemy.orm import Mapped, relationship
from typing import List
from app.database import Base, str_uniq, int_pk, str_null_true


# создаем модель таблицы факультетов (majors)
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
