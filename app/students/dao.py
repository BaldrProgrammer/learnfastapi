from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from app.students.models import Student
from app.dao.base import BaseDAO
from app.database import async_session_maker

class StudentDAO(BaseDAO):
    model = Student

    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_session_maker() as session:
            query_student = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result_student = (await session.execute(query_student)).scalar_one_or_none()

            if not result_student:
                return None

            student_info = result_student.to_dict()
            student_info['major_id'] = result_student.major.major_name

            return student_info
