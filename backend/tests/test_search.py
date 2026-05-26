import pytest


@pytest.mark.asyncio
async def test_clearance_search_returns_results(client):
    resp = await client.post("/api/v1/search", json={"name": "NovaMark"})
    assert resp.status_code == 200
    data = resp.json()
    assert "query" in data
    assert "total" in data
    assert "results" in data
    assert data["query"] == "NovaMark"
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_clearance_search_result_fields(client):
    resp = await client.post("/api/v1/search", json={"name": "NovaMark"})
    assert resp.status_code == 200
    results = resp.json()["results"]
    assert len(results) > 0
    first = results[0]
    for field in ("name", "owner", "jurisdiction", "status", "classes",
                  "similarity_score", "risk_level", "conflict_type"):
        assert field in first, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_clearance_search_sorted_by_score(client):
    resp = await client.post("/api/v1/search", json={"name": "NovaMark"})
    results = resp.json()["results"]
    scores = [r["similarity_score"] for r in results]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.asyncio
async def test_clearance_search_jurisdiction_filter(client):
    resp = await client.post("/api/v1/search", json={"name": "Nova", "jurisdiction": "US"})
    assert resp.status_code == 200
    results = resp.json()["results"]
    for r in results:
        assert r["jurisdiction"] == "US"


@pytest.mark.asyncio
async def test_clearance_search_high_score_for_identical(client):
    resp = await client.post("/api/v1/search", json={"name": "NovaMark", "min_score": 0.0})
    results = resp.json()["results"]
    top = results[0]
    assert top["name"] == "NovaMark"
    assert top["similarity_score"] >= 0.9
    assert top["risk_level"] == "Identical"


@pytest.mark.asyncio
async def test_clearance_search_no_results_for_unique_name(client):
    resp = await client.post(
        "/api/v1/search",
        json={"name": "ZzzzUniqueName9999", "min_score": 0.9},
    )
    assert resp.status_code == 200
    assert resp.json()["total"] == 0


@pytest.mark.asyncio
async def test_clearance_search_validation_error(client):
    resp = await client.post("/api/v1/search", json={"name": ""})
    assert resp.status_code == 422
