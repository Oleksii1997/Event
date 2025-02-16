import datetime
from src.config.models import Base
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from typing import Annotated, Optional


created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('UTC', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('UTC', now())"),
                                                        onupdate=datetime.datetime.now(datetime.UTC))]

class VerificationModel(Base):
    """Модель верифікації користувача через e-mail під час реєстрації"""

    __tablename__ = "verification"
    link: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]

    user: Mapped["UserModel"] = relationship(back_populates="verification", lazy="selectin", uselist=False)