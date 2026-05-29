"""Demo seed / reset for the landing page.

Every trademark written here has a name beginning with the DEMO_PREFIX
("DEMO " ). `reset_demo()` deletes only trademarks whose name starts with
that prefix — and because every child row (classes, watchlist entries,
deadline alerts, opposition cases) cascades from the trademark, wiping the
demo trademarks removes the whole demo dataset and nothing else.

There is no auth/user model in this app, so the demo seeds data only and
returns no login credentials.

The dataset is intentionally small but exercises every shipped feature:
  • a portfolio of trademarks across several NICE classes & statuses
  • per-trademark NICE class entries
  • upcoming renewal / statement-of-use deadline alerts
  • a watchlist entry (a confusingly-similar conflicting mark)
  • an opposition case in an active stage
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import utc_now
from app.models.deadline import DeadlineAlert
from app.models.opposition import OppositionCase
from app.models.trademark import Trademark, TrademarkClass
from app.models.watchlist import WatchlistEntry

DEMO_PREFIX = "DEMO "


@dataclass
class DemoStatus:
    enabled: bool
    seeded: bool
    counts: dict[str, int]
    credentials: None = None


async def _demo_trademark_ids(db: AsyncSession) -> list:
    rows = (
        await db.execute(
            select(Trademark.id).where(Trademark.name.like(f"{DEMO_PREFIX}%"))
        )
    ).all()
    return [r[0] for r in rows]


async def gather_status(db: AsyncSession, *, enabled: bool) -> DemoStatus:
    tm_ids = await _demo_trademark_ids(db)
    if not tm_ids:
        return DemoStatus(enabled=enabled, seeded=False, counts={})

    counts = {
        "trademarks": len(tm_ids),
        "classes": (
            await db.execute(
                select(func.count(TrademarkClass.id)).where(
                    TrademarkClass.trademark_id.in_(tm_ids)
                )
            )
        ).scalar_one(),
        "deadlines": (
            await db.execute(
                select(func.count(DeadlineAlert.id)).where(
                    DeadlineAlert.trademark_id.in_(tm_ids)
                )
            )
        ).scalar_one(),
        "watchlist": (
            await db.execute(
                select(func.count(WatchlistEntry.id)).where(
                    WatchlistEntry.trademark_id.in_(tm_ids)
                )
            )
        ).scalar_one(),
        "oppositions": (
            await db.execute(
                select(func.count(OppositionCase.id)).where(
                    OppositionCase.trademark_id.in_(tm_ids)
                )
            )
        ).scalar_one(),
    }
    return DemoStatus(enabled=enabled, seeded=True, counts=counts)


async def seed_demo(db: AsyncSession) -> DemoStatus:
    """Idempotent: wipe any existing demo data, then seed a fresh portfolio."""
    await reset_demo(db)
    now = utc_now()

    # ── Portfolio of trademarks across NICE classes & statuses ──────────
    nova = Trademark(
        name="DEMO NovaMark",
        owner="DEMO Nova Labs Inc.",
        status="Registered",
        jurisdiction="US",
        application_number="DEMO-88123456",
        registration_number="DEMO-6543210",
        filing_date=now - timedelta(days=900),
        registration_date=now - timedelta(days=540),
        expiry_date=now + timedelta(days=45),  # renewal due soon
        description="Cloud data-sync platform brand.",
    )
    nova.classes = [
        TrademarkClass(nice_class_number=9, description="Computer software"),
        TrademarkClass(nice_class_number=42, description="SaaS and PaaS services"),
    ]
    nova.deadlines = [
        DeadlineAlert(
            deadline_type="Renewal",
            due_date=now + timedelta(days=45),
            status="Pending",
            notes="10-year registration renewal due.",
        ),
        DeadlineAlert(
            deadline_type="Declaration of Use (§8)",
            due_date=now + timedelta(days=120),
            status="Pending",
        ),
    ]
    nova.watchlist_entries = [
        WatchlistEntry(
            conflicting_mark_name="NovaMarq",
            similarity_score=0.91,
            conflict_type="Phonetic",
            status="Active",
            notes="Newly published application for related software services.",
        ),
    ]

    aurora = Trademark(
        name="DEMO Aurora",
        owner="DEMO Aurora Apparel Co.",
        status="Pending",
        jurisdiction="EU",
        application_number="DEMO-018765432",
        filing_date=now - timedelta(days=80),
        description="Outdoor apparel line.",
    )
    aurora.classes = [
        TrademarkClass(nice_class_number=25, description="Clothing, footwear"),
        TrademarkClass(nice_class_number=35, description="Retail services"),
    ]
    aurora.deadlines = [
        DeadlineAlert(
            deadline_type="Statement of Use",
            due_date=now + timedelta(days=20),
            status="Pending",
            notes="Opposition window closes — file SOU after.",
        ),
    ]
    aurora.oppositions = [
        OppositionCase(
            case_number="DEMO-OPP-91234",
            case_type="Opposition",
            stage="Opposed",
            opposing_party="Aurora Lighting GmbH",
            opposing_counsel="Müller & Partner",
            filing_date=now - timedelta(days=15),
            response_deadline=now + timedelta(days=10),
            hearing_date=now + timedelta(days=75),
            notes="Opposer claims confusion with Class 11 lighting mark.",
        ),
    ]

    helix = Trademark(
        name="DEMO Helix Foods",
        owner="DEMO Helix Foods LLC",
        status="Registered",
        jurisdiction="US",
        application_number="DEMO-87000111",
        registration_number="DEMO-5998877",
        filing_date=now - timedelta(days=2200),
        registration_date=now - timedelta(days=1800),
        expiry_date=now + timedelta(days=730),
        description="Organic snack foods brand.",
    )
    helix.classes = [
        TrademarkClass(nice_class_number=29, description="Processed foods"),
        TrademarkClass(nice_class_number=30, description="Snacks, confectionery"),
    ]

    quill = Trademark(
        name="DEMO Quill",
        owner="DEMO Quill Publishing",
        status="Refused",
        jurisdiction="UK",
        application_number="DEMO-UK00003456",
        filing_date=now - timedelta(days=300),
        description="Self-publishing platform — refused on descriptiveness.",
    )
    quill.classes = [
        TrademarkClass(nice_class_number=41, description="Publishing services"),
    ]

    db.add_all([nova, aurora, helix, quill])
    await db.commit()
    return await gather_status(db, enabled=True)


async def reset_demo(db: AsyncSession) -> DemoStatus:
    """Delete only demo trademarks; child rows cascade via FK ondelete."""
    tm_ids = await _demo_trademark_ids(db)
    if tm_ids:
        # Child tables have ON DELETE CASCADE on trademark_id, but issue
        # explicit deletes too so this works even without DB-level cascade.
        for model in (
            DeadlineAlert,
            OppositionCase,
            WatchlistEntry,
            TrademarkClass,
        ):
            await db.execute(
                delete(model).where(model.trademark_id.in_(tm_ids))
            )
        await db.execute(delete(Trademark).where(Trademark.id.in_(tm_ids)))
        await db.commit()
    return await gather_status(db, enabled=True)
