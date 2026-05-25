import pytest


@pytest.mark.asyncio
async def test_list_trademarks_empty(client):
    response = await client.get("/api/v1/trademarks/")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_trademark(client):
    payload = {
        "name": "NovaMark",
        "owner": "Acme Corp",
        "status": "Pending",
        "jurisdiction": "US",
        "classes": [{"nice_class_number": 42, "description": "Software as a service"}],
    }
    response = await client.post("/api/v1/trademarks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "NovaMark"
    assert data["owner"] == "Acme Corp"
    assert len(data["classes"]) == 1
    assert data["classes"][0]["nice_class_number"] == 42
    return data["id"]


@pytest.mark.asyncio
async def test_get_trademark(client):
    create_resp = await client.post(
        "/api/v1/trademarks/",
        json={"name": "SkyBrand", "owner": "Test Inc"},
    )
    assert create_resp.status_code == 201
    tm_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/trademarks/{tm_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "SkyBrand"


@pytest.mark.asyncio
async def test_get_trademark_not_found(client):
    response = await client.get("/api/v1/trademarks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_trademark(client):
    create_resp = await client.post(
        "/api/v1/trademarks/",
        json={"name": "OldName", "owner": "Corp A"},
    )
    tm_id = create_resp.json()["id"]

    response = await client.put(
        f"/api/v1/trademarks/{tm_id}",
        json={"name": "NewName", "status": "Registered"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "NewName"
    assert data["status"] == "Registered"


@pytest.mark.asyncio
async def test_delete_trademark(client):
    create_resp = await client.post(
        "/api/v1/trademarks/",
        json={"name": "ToDelete", "owner": "Corp B"},
    )
    tm_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/trademarks/{tm_id}")
    assert response.status_code == 204

    response = await client.get(f"/api/v1/trademarks/{tm_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_trademarks_after_create(client):
    for i in range(3):
        await client.post(
            "/api/v1/trademarks/",
            json={"name": f"Mark{i}", "owner": "Batch Corp"},
        )

    response = await client.get("/api/v1/trademarks/?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3
