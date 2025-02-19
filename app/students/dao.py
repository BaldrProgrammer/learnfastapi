from sqlalchemy import update, delete, event
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from app.students.models import Student, Major
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.students.schemas import SStudent


import asyncio


@event.listens_for(Student, 'after_insert')
def receive_after_insert(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        update(Major)
        .where(Major.id == major_id)
        .values(count_students=Major.count_students + 1)
    )


@event.listens_for(Student, 'after_delete')
def receive_after_delete(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        update(Major)
        .where(Major.id == major_id)
        .values(count_students=Major.count_students - 1)
    )


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

    @classmethod
    async def add_students(cls, student_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_student = Student(**student_data)
                session.add(new_student)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_student.to_dict()['id']

    @classmethod
    async def update_students(cls, student_id: int, values: dict):
        async with async_session_maker() as session:
            async with session.begin():
                current_info = (await cls.find_all(True, id=student_id))[0].to_dict()
                values = current_info | values
                query = (
                    update(cls.model)
                    .filter_by(id=student_id)
                    .values(**values)
                    .execution_options(synchronize_session='fetch')
                )
                await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return values

    @classmethod
    async def del_students(cls, student_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model).filter_by(id=student_id)
                await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return student_id
