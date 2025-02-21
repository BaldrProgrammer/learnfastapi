from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.models import Course
from app.database import async_session_maker

import asyncio


class CourseDAO(BaseDAO):
    model = Course

    @classmethod
    async def find_all(cls, isfilters: bool = False, **filters):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(selectinload(Course.major), selectinload(Course.students))
            )
            if isfilters:
                query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, student_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=student_id).options(selectinload(Course.major),
                                                                       selectinload(Course.students))
            response = await session.execute(query)
            return response.scalar_one_or_none()

    @classmethod
    async def update_course(cls, course_id: int, values: dict):
        async with async_session_maker() as session:
            current_info = (await cls.find_one_or_none_by_id(course_id)).to_dict()
            remain_values = {}
            for k in values:
                if values[k]:
                    remain_values[k] = values[k]

            new_info = current_info | remain_values
            query = (
                update(cls.model)
                .filter_by(id=course_id)
                .values(**new_info)
                .execution_options(synchronize_session='fetch')
            )
            await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_info
