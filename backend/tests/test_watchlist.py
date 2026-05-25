import pytest


async def create_trademark(client, name="TestMark"):
    resp = await client.post(
        "/api/v1/trademarks/",
        json={"name": name, "owner": "Test Owner"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_list_watchlist_empty(client):
    tm_id = await create_trademark(client)
    response = await client.get(f"/api/v1/trademarks/{tm_id}/watchlist")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_add_watchlist_entry(client):
    tm_id = await create_trademark(client, "BrandX")
    payload = {
        "conflicting_mark_name": "BrandXtra",
        "conflict_type": "Phonetic",
        "similarity_score": 0.82,
    }
    response = await client.post(f"/api/v1/trademarks/{tm_id}/watchlist", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["conflicting_mark_name"] == "BrandXtra"
    assert data["similarity_score"] == pytest.approx(0.82)
    assert data["trademark_id"] == tm_id


@pytest.mark.asyncio
async def test_update_watchlist_entry(client):
    tm_id = await create_trademark(client, "BrandY")
    create_resp = await client.post(
        f"/api/v1/trademarks/{tm_id}/watchlist",
        json={"conflicting_mark_name": "BrandYX", "conflict_type": "Semantic"},
    )
    entry_id = create_resp.json()["id"]

    response = await client.put(f"/api/v1/watchlist/{entry_id}", json={"status": "Dismissed"})
    assert response.status_code == 200
    assert response.json()["status"] == "Dismissed"


@pytest.mark.asyncio
async def test_delete_watchlist_entry(client):
    tm_id = await create_trademark(client, "BrandZ")
    create_resp = await client.post(
        f"/api/v1/trademarks/{tm_id}/watchlist",
        json={"conflicting_mark_name": "BrandZX"},
    )
    entry_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/watchlist/{entry_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_watchlist_404_on_invalid_trademark(client):
    response = await client.get(
        "/api/v1/trademarks/00000000-0000-0000-0000-000000000000/watchlist"
    )
    assert response.status_code == 404
