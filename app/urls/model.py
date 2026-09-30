from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ShortUrl(Base):
    __tablename__ = 'short_urls'

    __table_args__ = (
        UniqueConstraint('target_url', name='uq_short_urls_target_url'),
        CheckConstraint('number_of_creations >= 1', name='check_number_of_creations_minimum'),
        CheckConstraint('last_created_at >= created_at', name='check_last_created_at_valid')
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    short_code: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        index=True
    )

    target_url: Mapped[str] = mapped_column(Text)

    number_of_creations: Mapped[int] = mapped_column(
        BigInteger,
        default=1,
        server_default=text('1'),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    last_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
