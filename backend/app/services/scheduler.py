"""Background scheduler — periodic watch monitoring and deadline scanning."""

from __future__ import annotations

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_factory

logger = logging.getLogger(__name__)

_scheduler: AsyncIOScheduler | None = None


async def _run_watch_scan() -> None:
    """Score all active watchlist entries against their parent trademark name."""
    try:
        from app.models.watchlist import WatchlistEntry
        from app.models.trademark import Trademark
        from app.services.similarity import compute_similarity

        async with async_session_factory() as db:
            result = await db.execute(
                select(WatchlistEntry)
                .join(Trademark, WatchlistEntry.trademark_id == Trademark.id)
                .where(WatchlistEntry.status == "Active")
            )
            entries = result.scalars().all()
            updated = 0
            for entry in entries:
                if entry.trademark and entry.conflicting_mark_name:
                    sim = compute_similarity(
                        entry.trademark.name, entry.conflicting_mark_name
                    )
                    if entry.similarity_score != sim.combined_score:
                        entry.similarity_score = sim.combined_score
                        updated += 1
            if updated:
                await db.commit()
            logger.info("Watch scan complete: %d entries updated", updated)
    except Exception as exc:
        logger.warning("Watch scan error: %s", exc)


async def _run_deadline_overdue_check() -> None:
    """Mark any Pending deadlines whose due_date is in the past as Overdue."""
    try:
        from app.core.utils import utc_now
        from app.models.deadline import DeadlineAlert

        async with async_session_factory() as db:
            now = utc_now()
            result = await db.execute(
                select(DeadlineAlert).where(
                    DeadlineAlert.status == "Pending",
                    DeadlineAlert.due_date < now,
                )
            )
            overdue = result.scalars().all()
            for alert in overdue:
                alert.status = "Overdue"
            if overdue:
                await db.commit()
            logger.info("Deadline check: %d items marked Overdue", len(overdue))
    except Exception as exc:
        logger.warning("Deadline overdue check error: %s", exc)


def start_scheduler() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    _scheduler = AsyncIOScheduler()
    # Watch scan every 24 hours
    _scheduler.add_job(
        _run_watch_scan,
        trigger=IntervalTrigger(hours=24),
        id="watch_scan",
        replace_existing=True,
    )
    # Deadline overdue check every 6 hours
    _scheduler.add_job(
        _run_deadline_overdue_check,
        trigger=IntervalTrigger(hours=6),
        id="deadline_check",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("Background scheduler started")
    return _scheduler


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        logger.info("Background scheduler stopped")
