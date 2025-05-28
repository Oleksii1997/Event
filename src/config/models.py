import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime
from sqlalchemy.sql import func

"""creating a new object type for some database fields"""
str_16 = Annotated[str, 16]
str_32 = Annotated[str, 32]
str_48 = Annotated[str, 48]
str_64 = Annotated[str, 64]
str_128 = Annotated[str, 128]
str_256 = Annotated[str, 256]
str_1024 = Annotated[str, 1024]
bytes_256 = Annotated[bytes, 256]
created_at = Annotated[
    datetime.datetime, mapped_column(DateTime(timezone=True), server_default=func.now())
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    ),
]


class Base(AsyncAttrs, DeclarativeBase):

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {','.join(cols)}>"
