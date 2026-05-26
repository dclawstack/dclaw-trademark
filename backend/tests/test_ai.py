import pytest


@pytest.mark.asyncio
async def test_suggest_classes_returns_suggestions(client):
    resp = await client.post(
        "/api/v1/ai/suggest-classes",
        json={"goods_services_description": "mobile app development and cloud software services"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "description" in data
    assert "suggestions" in data
    assert len(data["suggestions"]) > 0


@pytest.mark.asyncio
async def test_suggest_classes_result_fields(client):
    resp = await client.post(
        "/api/v1/ai/suggest-classes",
        json={"goods_services_description": "online retail clothing store"},
    )
    suggestions = resp.json()["suggestions"]
    for s in suggestions:
        assert "class_number" in s
        assert "confidence" in s
        assert 1 <= s["class_number"] <= 45
        assert 0.0 <= s["confidence"] <= 1.0


@pytest.mark.asyncio
async def test_suggest_classes_class_42_for_software(client):
    resp = await client.post(
        "/api/v1/ai/suggest-classes",
        json={"goods_services_description": "SaaS platform for software development tools"},
    )
    suggestions = resp.json()["suggestions"]
    class_numbers = [s["class_number"] for s in suggestions]
    assert 42 in class_numbers


@pytest.mark.asyncio
async def test_suggest_classes_validation_error(client):
    resp = await client.post("/api/v1/ai/suggest-classes", json={"goods_services_description": "ab"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_copilot_chat_returns_reply(client):
    resp = await client.post(
        "/api/v1/ai/copilot/chat",
        json={"message": "How do I search for trademark conflicts?"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data
    assert "suggested_actions" in data
    assert len(data["reply"]) > 0


@pytest.mark.asyncio
async def test_copilot_chat_suggests_actions(client):
    resp = await client.post(
        "/api/v1/ai/copilot/chat",
        json={"message": "What are the renewal deadlines for US trademarks?"},
    )
    data = resp.json()
    assert isinstance(data["suggested_actions"], list)
    for action in data["suggested_actions"]:
        assert "label" in action
        assert "action" in action


@pytest.mark.asyncio
async def test_copilot_chat_validation_error(client):
    resp = await client.post("/api/v1/ai/copilot/chat", json={"message": ""})
    assert resp.status_code == 422
