import pytest


@pytest.mark.asyncio
async def test_list_all_classes(client):
    resp = await client.get("/api/v1/classes")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 45
    first = data[0]
    assert first["class_number"] == 1
    assert "title" in first
    assert "description" in first
    assert "examples" in first


@pytest.mark.asyncio
async def test_get_single_class(client):
    resp = await client.get("/api/v1/classes/42")
    assert resp.status_code == 200
    data = resp.json()
    assert data["class_number"] == 42
    assert "software" in data["description"].lower() or "technology" in data["title"].lower()


@pytest.mark.asyncio
async def test_get_class_not_found(client):
    resp = await client.get("/api/v1/classes/99")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_classes_keyword_filter(client):
    resp = await client.get("/api/v1/classes?keyword=software")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    class_numbers = [item["class_number"] for item in data]
    assert 42 in class_numbers


@pytest.mark.asyncio
async def test_list_classes_no_match(client):
    resp = await client.get("/api/v1/classes?keyword=xyznonexistentterm12345")
    assert resp.status_code == 200
    assert resp.json() == []
