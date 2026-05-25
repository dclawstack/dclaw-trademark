import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.utils import utc_now
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.trademark import Trademark


class WatchlistEntry(Base):
    __tablename__ = "watchlist_entries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    trademark_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("trademarks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    conflicting_mark_name: Mapped[str] = mapped_column(String(255), nullable=False)
    similarity_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    conflict_type: Mapped[str] = mapped_column(String(50), nullable=False, default="Phonetic")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Active")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)

    trademark: Mapped["Trademark"] = relationship(
        "Trademark", back_populates="watchlist_entries", lazy="selectin"
    )
