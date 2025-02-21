import asyncio

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from app.models import Student
from app.dao.base import BaseDAO
from app.database import async_session_maker


class StudentDAO(BaseDAO):
    model = Student

    @classmethod
    async def find_all(cls, isfilters: bool = False, **filters):
        async with async_session_maker() as session:
            query = select(cls.model)
            if isfilters:
                query = query.filter_by(**filters)
            response = await session.execute(query)
            return response.scalars().all()

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
    async def change_course(cls, student_id: int, course_id: int):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .filter_by(id=student_id)
                .values(course_id=course_id)
            )
            await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return course_id

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


# asyncio.run(StudentDAO.change_course(2, 1))
