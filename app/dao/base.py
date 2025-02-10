from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_obj = cls.model(**values)
                session.add(new_obj)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_obj

    @classmethod
    async def find_all(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            response = await session.execute(query)
            return response.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, student_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=student_id)
            response = await session.execute(query)
            return response.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_filter(cls, **filters):
        async with async_session_maker as session:
            query = select(cls.model).filter_by(**filters)
            response = await session.execute(query)
            return response.scalar_one_or_none()
