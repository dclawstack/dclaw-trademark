import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.utils import utc_now
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.deadline import DeadlineAlert
    from app.models.watchlist import WatchlistEntry


class Trademark(Base):
    __tablename__ = "trademarks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")
    jurisdiction: Mapped[str] = mapped_column(String(10), nullable=False, default="US")
    application_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    registration_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    filing_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    registration_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    expiry_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)

    classes: Mapped[List["TrademarkClass"]] = relationship(
        "TrademarkClass",
        lazy="selectin",
        cascade="all, delete-orphan",
        back_populates="trademark",
    )
    watchlist_entries: Mapped[List["WatchlistEntry"]] = relationship(
        "WatchlistEntry",
        lazy="selectin",
        cascade="all, delete-orphan",
        back_populates="trademark",
    )
    deadlines: Mapped[List["DeadlineAlert"]] = relationship(
        "DeadlineAlert",
        lazy="selectin",
        cascade="all, delete-orphan",
        back_populates="trademark",
    )


class TrademarkClass(Base):
    __tablename__ = "trademark_classes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    trademark_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("trademarks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nice_class_number: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utc_now)

    trademark: Mapped["Trademark"] = relationship(
        "Trademark", back_populates="classes", lazy="selectin"
    )
