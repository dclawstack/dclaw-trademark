"""Billing endpoints — Stripe Checkout + webhook skeleton."""
import hashlib
import hmac
import json
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.subscription import Subscription

router = APIRouter()

PLANS = {
    "starter": {"price_usd": 4900, "search_credits": 50, "label": "Starter $49/mo"},
    "pro": {"price_usd": 9900, "search_credits": 500, "label": "Pro $99/seat/mo"},
    "enterprise": {"price_usd": 29900, "search_credits": -1, "label": "Enterprise $299/mo"},
}


class CheckoutRequest(BaseModel):
    email: str
    plan: str
    success_url: str
    cancel_url: str


@router.get("/plans")
async def list_plans():
    return [{"plan": k, **v} for k, v in PLANS.items()]


@router.post("/checkout")
async def create_checkout(payload: CheckoutRequest, db: AsyncSession = Depends(get_db)):
    if payload.plan not in PLANS:
        raise HTTPException(status_code=400, detail=f"Unknown plan: {payload.plan}")
    if not settings.stripe_secret_key:
        # Return mock session when Stripe is not configured
        return {
            "session_id": "mock_session_" + hashlib.md5(payload.email.encode()).hexdigest()[:8],
            "checkout_url": payload.success_url,
            "plan": payload.plan,
            "note": "Stripe not configured — this is a mock checkout response",
        }
    # Real Stripe integration (requires stripe package + API key)
    try:
        import stripe  # type: ignore
        stripe.api_key = settings.stripe_secret_key
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": PLANS[payload.plan]["label"]},
                        "unit_amount": PLANS[payload.plan]["price_usd"],
                        "recurring": {"interval": "month"},
                    },
                    "quantity": 1,
                }
            ],
            mode="subscription",
            customer_email=payload.email,
            success_url=payload.success_url,
            cancel_url=payload.cancel_url,
            metadata={"plan": payload.plan},
        )
        return {"session_id": session.id, "checkout_url": session.url}
    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="Stripe library not installed. Add 'stripe' to requirements.txt.",
        )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    stripe_signature: Optional[str] = Header(default=None, alias="stripe-signature"),
):
    body = await request.body()
    if settings.stripe_webhook_secret and stripe_signature:
        try:
            import stripe  # type: ignore
            event = stripe.Webhook.construct_event(
                body, stripe_signature, settings.stripe_webhook_secret
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid webhook signature")
    else:
        try:
            event = json.loads(body)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON body")

    event_type = event.get("type", "")
    data = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        email = data.get("customer_email", "")
        sub_id = data.get("subscription")
        # Derive plan from Stripe metadata; fall back to "pro" if unset
        plan = data.get("metadata", {}).get("plan") or "pro"
        if plan not in PLANS:
            plan = "pro"
        result = await db.execute(
            select(Subscription).where(Subscription.customer_email == email)
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.stripe_subscription_id = sub_id
            sub.plan = plan
            sub.status = "active"
        else:
            db.add(Subscription(
                customer_email=email,
                stripe_subscription_id=sub_id,
                plan=plan,
                status="active",
                search_credits=PLANS[plan]["search_credits"],
            ))
        await db.commit()

    elif event_type in ("customer.subscription.deleted", "customer.subscription.updated"):
        sub_id = data.get("id")
        status = "canceled" if event_type.endswith("deleted") else data.get("status", "active")
        result = await db.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = status
            await db.commit()

    return {"received": True}


@router.get("/subscription/{email}")
async def get_subscription(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Subscription).where(Subscription.customer_email == email)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        return {"plan": "free", "status": "active", "search_credits": 5}
    return {
        "plan": sub.plan,
        "status": sub.status,
        "search_credits": sub.search_credits,
        "current_period_end": sub.current_period_end,
    }
