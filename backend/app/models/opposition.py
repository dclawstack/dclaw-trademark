import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.utils import utc_now
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.trademark import Trademark


class OppositionCase(Base):
    __tablename__ = "opposition_cases"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    trademark_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("trademarks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    case_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    case_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="Opposition"
    )  # Opposition | Cancellation | CeaseAndDesist | Litigation
    stage: Mapped[str] = mapped_column(
        String(50), nullable=False, default="Filed"
    )  # Filed | Published | OppositionWindow | Opposed | Resolved | Abandoned
    opposing_party: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    opposing_counsel: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    filing_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    response_deadline: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    hearing_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    outcome: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)

    trademark: Mapped["Trademark"] = relationship(
        "Trademark", back_populates="oppositions", lazy="selectin"
    )
