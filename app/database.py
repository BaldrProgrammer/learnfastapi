from typing import Annotated
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped
from app.config import get_db_url


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
