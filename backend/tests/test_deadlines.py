import pytest
from datetime import datetime, timedelta


async def create_trademark(client, name="DeadlineMark"):
    resp = await client.post(
        "/api/v1/trademarks/",
        json={"name": name, "owner": "Deadline Corp"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def future_date(days: int) -> str:
    return (datetime.utcnow() + timedelta(days=days)).isoformat()


@pytest.mark.asyncio
async def test_list_deadlines_empty(client):
    tm_id = await create_trademark(client)
    response = await client.get(f"/api/v1/trademarks/{tm_id}/deadlines")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_deadline(client):
    tm_id = await create_trademark(client, "RenewalMark")
    payload = {
        "deadline_type": "RENEWAL",
        "due_date": future_date(30),
        "status": "Pending",
        "notes": "10-year US renewal",
    }
    response = await client.post(f"/api/v1/trademarks/{tm_id}/deadlines", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["deadline_type"] == "RENEWAL"
    assert data["status"] == "Pending"
    assert data["trademark_id"] == tm_id


@pytest.mark.asyncio
async def test_update_deadline_status(client):
    tm_id = await create_trademark(client, "ResponseMark")
    create_resp = await client.post(
        f"/api/v1/trademarks/{tm_id}/deadlines",
        json={"deadline_type": "RESPONSE", "due_date": future_date(14)},
    )
    dl_id = create_resp.json()["id"]

    response = await client.put(f"/api/v1/deadlines/{dl_id}", json={"status": "Completed"})
    assert response.status_code == 200
    assert response.json()["status"] == "Completed"


@pytest.mark.asyncio
async def test_delete_deadline(client):
    tm_id = await create_trademark(client, "ExpiredMark")
    create_resp = await client.post(
        f"/api/v1/trademarks/{tm_id}/deadlines",
        json={"deadline_type": "MAINTENANCE", "due_date": future_date(60)},
    )
    dl_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/deadlines/{dl_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_upcoming_deadlines(client):
    tm_id = await create_trademark(client, "UpcomingMark")
    await client.post(
        f"/api/v1/trademarks/{tm_id}/deadlines",
        json={"deadline_type": "RENEWAL", "due_date": future_date(10)},
    )
    await client.post(
        f"/api/v1/trademarks/{tm_id}/deadlines",
        json={"deadline_type": "RESPONSE", "due_date": future_date(400)},
    )

    response = await client.get("/api/v1/deadlines/upcoming?days=30")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["deadline_type"] == "RENEWAL"


@pytest.mark.asyncio
async def test_deadlines_404_on_invalid_trademark(client):
    response = await client.get(
        "/api/v1/trademarks/00000000-0000-0000-0000-000000000000/deadlines"
    )
    assert response.status_code == 404
