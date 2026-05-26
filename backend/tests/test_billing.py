import pytest


@pytest.mark.asyncio
async def test_list_plans(client):
    resp = await client.get("/api/v1/billing/plans")
    assert resp.status_code == 200
    plans = resp.json()
    assert len(plans) == 3
    plan_names = {p["plan"] for p in plans}
    assert plan_names == {"starter", "pro", "enterprise"}


@pytest.mark.asyncio
async def test_list_plans_fields(client):
    resp = await client.get("/api/v1/billing/plans")
    for plan in resp.json():
        assert "plan" in plan
        assert "price_usd" in plan
        assert "search_credits" in plan
        assert "label" in plan


@pytest.mark.asyncio
async def test_checkout_mock_no_stripe(client):
    resp = await client.post(
        "/api/v1/billing/checkout",
        json={
            "email": "test@example.com",
            "plan": "pro",
            "success_url": "http://localhost:3066/billing/success",
            "cancel_url": "http://localhost:3066/billing",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "session_id" in data
    assert "checkout_url" in data


@pytest.mark.asyncio
async def test_checkout_invalid_plan(client):
    resp = await client.post(
        "/api/v1/billing/checkout",
        json={
            "email": "test@example.com",
            "plan": "nonexistent",
            "success_url": "http://localhost/success",
            "cancel_url": "http://localhost/cancel",
        },
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_get_subscription_no_record(client):
    resp = await client.get("/api/v1/billing/subscription/unknown@example.com")
    assert resp.status_code == 200
    data = resp.json()
    assert data["plan"] == "free"
    assert data["status"] == "active"
