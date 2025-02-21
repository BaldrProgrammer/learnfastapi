from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.dao.base import BaseDAO
from app.models import Major
from app.models import Course
from app.database import async_session_maker

class MajorDAO(BaseDAO):
    model = Major

    @classmethod
    async def find_all(cls, isfilters: bool = False, **filters):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.course).selectinload(Course.students))
            )
            if isfilters:
                query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()
