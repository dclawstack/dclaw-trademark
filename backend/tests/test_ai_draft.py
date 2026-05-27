import pytest


@pytest.mark.asyncio
async def test_draft_application_returns_structure(client):
    resp = await client.post(
        "/api/v1/ai/draft-application",
        json={
            "name": "NovaMark",
            "owner": "Acme Corp",
            "goods_services_description": "Online software as a service for project management tools",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "goods_services" in data
    assert "specimen_guidance" in data
    assert "classes" in data
    assert "disclaimers" in data
    assert "teas_json" in data
    assert isinstance(data["classes"], list)
    assert len(data["classes"]) > 0


@pytest.mark.asyncio
async def test_draft_application_classes_are_valid(client):
    resp = await client.post(
        "/api/v1/ai/draft-application",
        json={
            "name": "FashionBrand",
            "owner": "Style Co",
            "goods_services_description": "Clothing, footwear and fashion accessories for retail",
        },
    )
    data = resp.json()
    for cls in data["classes"]:
        assert 1 <= cls <= 45


@pytest.mark.asyncio
async def test_draft_application_teas_json_has_mark(client):
    resp = await client.post(
        "/api/v1/ai/draft-application",
        json={
            "name": "TestMark",
            "owner": "TestOwner",
            "goods_services_description": "Cloud computing services and software development tools",
        },
    )
    teas = resp.json()["teas_json"]
    assert teas.get("markName") == "TestMark"
    assert teas.get("owner") == "TestOwner"


@pytest.mark.asyncio
async def test_draft_application_validation_error(client):
    resp = await client.post(
        "/api/v1/ai/draft-application",
        json={"name": "X", "owner": "Y", "goods_services_description": "too short"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_logo_search_stub(client):
    resp = await client.post("/api/v1/ai/search/logo")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "not_implemented"
    assert "planned_version" in data
