"""AI-assisted Nice class recommendation from goods/services description."""

from __future__ import annotations

import json
import re

import httpx

from app.core.config import settings
from app.services.nice_classes import NICE_CLASSES, search_classes_by_keyword


def _keyword_recommend(description: str) -> list[dict]:
    """Fast local keyword matching against Nice class corpus."""
    words = re.findall(r"\b\w{3,}\b", description.lower())
    scores: dict[int, float] = {}
    for word in words:
        for item in search_classes_by_keyword(word):
            num = item["class_number"]
            scores[num] = scores.get(num, 0.0) + 1.0

    if not scores:
        return []

    max_score = max(scores.values())
    results = []
    for num, score in sorted(scores.items(), key=lambda x: -x[1]):
        confidence = round(score / max_score, 2)
        if confidence < 0.1:
            continue
        data = NICE_CLASSES[num]
        results.append(
            {
                "class_number": num,
                "title": data["title"],
                "confidence": confidence,
                "reasoning": f"Matched keyword(s) in description against class {num} ({data['title']}).",
            }
        )
    return results[:5]


async def _llm_recommend(description: str) -> list[dict] | None:
    """Call OpenRouter (or Ollama fallback) for smarter class suggestions."""
    system_prompt = (
        "You are a trademark attorney specialising in Nice Classification. "
        "Given a goods/services description, return the top 3 most relevant Nice classes as JSON. "
        'Format: [{"class_number": <int>, "title": "<str>", "confidence": <0-1>, "reasoning": "<str>"}]'
    )
    user_msg = f"Goods/services description: {description}"

    # Try OpenRouter first
    if settings.openrouter_api_key:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
                    json={
                        "model": "mistralai/mistral-7b-instruct",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_msg},
                        ],
                        "temperature": 0.2,
                    },
                )
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception:
            pass

    # Fallback: Ollama
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                f"{settings.ollama_url}/api/generate",
                json={
                    "model": "mistral",
                    "prompt": f"{system_prompt}\n\n{user_msg}",
                    "stream": False,
                },
            )
        if resp.status_code == 200:
            raw = resp.json().get("response", "")
            match = re.search(r"\[.*\]", raw, re.DOTALL)
            if match:
                return json.loads(match.group())
    except Exception:
        pass

    return None


async def suggest_classes(description: str) -> list[dict]:
    """Return class suggestions: try LLM first, fall back to keyword matching."""
    llm_results = await _llm_recommend(description)
    if llm_results:
        return llm_results
    return _keyword_recommend(description)
