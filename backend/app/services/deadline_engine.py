"""Deadline alert engine — calculates upcoming trademark deadlines."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deadline import DeadlineAlert
from app.models.trademark import Trademark


async def get_upcoming_deadlines(db: AsyncSession, days: int = 30) -> list[dict]:
    """Return all DeadlineAlert records due within the next `days` days."""
    cutoff = datetime.utcnow().date() + timedelta(days=days)
    today = datetime.utcnow().date()

    stmt = (
        select(DeadlineAlert)
        .join(Trademark, DeadlineAlert.trademark_id == Trademark.id)
        .where(
            DeadlineAlert.status == "Pending",
            DeadlineAlert.due_date <= cutoff,
        )
        .order_by(DeadlineAlert.due_date)
    )
    result = await db.execute(stmt)
    alerts = result.scalars().all()

    output = []
    for alert in alerts:
        due = alert.due_date.date() if isinstance(alert.due_date, datetime) else alert.due_date
        days_remaining = (due - today).days
        output.append(
            {
                "id": str(alert.id),
                "trademark_id": str(alert.trademark_id),
                "trademark_name": alert.trademark.name if alert.trademark else None,
                "deadline_type": alert.deadline_type,
                "due_date": due.isoformat(),
                "days_remaining": days_remaining,
                "status": alert.status,
                "notes": alert.notes,
                "is_overdue": days_remaining < 0,
            }
        )
    return output
