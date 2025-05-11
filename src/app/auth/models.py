from sqlalchemy import text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from typing import Annotated, Optional
import datetime

from src.config.models import Base


created_at = Annotated[
    datetime.datetime, mapped_column(DateTime(timezone=True), server_default=func.now())
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    ),
]


class VerificationModel(Base):
    """Модель верифікації користувача через e-mail під час реєстрації"""

    __tablename__ = "verification_table"
    link: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_table.id", ondelete="CASCADE")
    )
    created_at: Mapped[created_at]

    # user: Mapped["UserModel"] = relationship(back_populates="verification", lazy="selectin", uselist=False)
