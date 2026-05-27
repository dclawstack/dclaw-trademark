import pytest


@pytest.mark.asyncio
async def test_list_oppositions_empty(client):
    create_resp = await client.post("/api/v1/trademarks/", json={"name": "OpMark", "owner": "Corp"})
    tm_id = create_resp.json()["id"]
    resp = await client.get(f"/api/v1/trademarks/{tm_id}/oppositions")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_opposition(client):
    create_resp = await client.post("/api/v1/trademarks/", json={"name": "OpMark2", "owner": "Corp"})
    tm_id = create_resp.json()["id"]
    payload = {
        "case_type": "Opposition",
        "stage": "Filed",
        "opposing_party": "Rival Inc",
        "case_number": "OPP-2026-001",
    }
    resp = await client.post(f"/api/v1/trademarks/{tm_id}/oppositions", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["opposing_party"] == "Rival Inc"
    assert data["case_type"] == "Opposition"
    assert data["stage"] == "Filed"
    assert data["trademark_id"] == tm_id


@pytest.mark.asyncio
async def test_get_opposition(client):
    create_tm = await client.post("/api/v1/trademarks/", json={"name": "OpMark3", "owner": "Corp"})
    tm_id = create_tm.json()["id"]
    create_op = await client.post(
        f"/api/v1/trademarks/{tm_id}/oppositions",
        json={"case_type": "CeaseAndDesist", "stage": "Filed", "opposing_party": "Big Corp"},
    )
    case_id = create_op.json()["id"]
    resp = await client.get(f"/api/v1/oppositions/{case_id}")
    assert resp.status_code == 200
    assert resp.json()["case_type"] == "CeaseAndDesist"


@pytest.mark.asyncio
async def test_update_opposition(client):
    create_tm = await client.post("/api/v1/trademarks/", json={"name": "OpMark4", "owner": "Corp"})
    tm_id = create_tm.json()["id"]
    create_op = await client.post(
        f"/api/v1/trademarks/{tm_id}/oppositions",
        json={"case_type": "Opposition", "stage": "Filed"},
    )
    case_id = create_op.json()["id"]
    resp = await client.put(
        f"/api/v1/oppositions/{case_id}",
        json={"stage": "Resolved", "outcome": "Dismissed in favour of applicant"},
    )
    assert resp.status_code == 200
    assert resp.json()["stage"] == "Resolved"
    assert resp.json()["outcome"] == "Dismissed in favour of applicant"


@pytest.mark.asyncio
async def test_delete_opposition(client):
    create_tm = await client.post("/api/v1/trademarks/", json={"name": "OpMark5", "owner": "Corp"})
    tm_id = create_tm.json()["id"]
    create_op = await client.post(
        f"/api/v1/trademarks/{tm_id}/oppositions",
        json={"case_type": "Opposition", "stage": "Filed"},
    )
    case_id = create_op.json()["id"]
    resp = await client.delete(f"/api/v1/oppositions/{case_id}")
    assert resp.status_code == 204
    resp2 = await client.get(f"/api/v1/oppositions/{case_id}")
    assert resp2.status_code == 404


@pytest.mark.asyncio
async def test_opposition_not_found(client):
    resp = await client.get("/api/v1/oppositions/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_opposition_cascade_delete(client):
    create_tm = await client.post("/api/v1/trademarks/", json={"name": "OpMark6", "owner": "Corp"})
    tm_id = create_tm.json()["id"]
    await client.post(f"/api/v1/trademarks/{tm_id}/oppositions", json={"case_type": "Opposition", "stage": "Filed"})
    await client.delete(f"/api/v1/trademarks/{tm_id}")
    resp = await client.get(f"/api/v1/trademarks/{tm_id}/oppositions")
    assert resp.status_code == 404
