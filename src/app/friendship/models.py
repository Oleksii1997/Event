from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship, Mapped
from uuid import uuid4, UUID
from typing import Optional

from src.config.models import Base, created_at


class FriendshipRequestModel(Base):
    """Модель заявок на підписку"""

    __tablename__ = "friendship_request_table"
    __table_args__ = (
        UniqueConstraint("sender_id", "receiver_id", name="uq_sender_receiver"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    sender_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_table.id"), nullable=False, index=True
    )
    receiver_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_table.id"), nullable=False, index=True
    )
    created_at: Mapped[Optional[created_at]]


class FriendshipModel(Base):
    """Модель друзів|підписників.
    user_id - мій id;
    friend_id - id на кого я підписаний"""

    __tablename__ = "friendship_table"
    __table_args__ = (UniqueConstraint("user_id", "friend_id", name="uq_user_friend"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_table.id"), nullable=False, index=True
    )
    friend_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_table.id"), nullable=False, index=True
    )
    created_at: Mapped[Optional[created_at]]
