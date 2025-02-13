from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
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
    async def update(cls, filter_by, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session='fetch')
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError('Для удаления данных нужно указать хотя-бы один параметр.')

        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model)
                if not delete_all:
                    query = query.filter_by(**filter_by)

                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def find_all(cls, isfilters: bool = True, **filters):
        async with async_session_maker() as session:
            query = select(cls.model)
            if isfilters:
                query = query.filter_by(**filters)
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
