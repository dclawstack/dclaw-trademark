"""AI Application Drafting — generate USPTO TEAS-compatible application stubs."""

from __future__ import annotations

import json
import re
from typing import Optional

import httpx

from app.core.config import settings
from app.services.class_recommender import suggest_classes

_DRAFT_SYSTEM = """You are an expert USPTO trademark application drafter.
Given a mark name, owner, and goods/services description, generate:
1. A polished goods/services description suitable for USPTO TEAS filing
2. Specimen guidance (what sample to submit)
3. Identified Nice classification classes

Return JSON: {"goods_services": "<text>", "specimen_guidance": "<text>", "classes": [<int>], "disclaimers": ["<text>"], "teas_json": {}}"""


async def _llm_draft(
    name: str, owner: str, description: str
) -> Optional[dict]:
    user_msg = f"Mark: {name}\nOwner: {owner}\nDescription: {description}"

    if settings.openrouter_api_key:
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
                    json={
                        "model": "mistralai/mistral-7b-instruct",
                        "messages": [
                            {"role": "system", "content": _DRAFT_SYSTEM},
                            {"role": "user", "content": user_msg},
                        ],
                        "temperature": 0.3,
                    },
                )
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"]
                match = re.search(r"\{.*\}", content, re.DOTALL)
                if match:
                    return json.loads(match.group())
        except Exception:
            pass

    if settings.ollama_url.startswith(("http://", "https://")):
        try:
            async with httpx.AsyncClient(timeout=25) as client:
                resp = await client.post(
                    f"{settings.ollama_url}/api/generate",
                    json={
                        "model": "mistral",
                        "prompt": f"{_DRAFT_SYSTEM}\n\n{user_msg}",
                        "stream": False,
                    },
                )
            if resp.status_code == 200:
                raw = resp.json().get("response", "")
                match = re.search(r"\{.*\}", raw, re.DOTALL)
                if match:
                    return json.loads(match.group())
        except Exception:
            pass

    return None


def _static_draft(name: str, owner: str, description: str, classes: list[dict]) -> dict:
    class_nums = [c["class_number"] for c in classes[:3]]
    goods = (
        f"{description.capitalize()} provided by {owner}, "
        "namely, [specify exact goods/services here]."
    )
    specimen = (
        "For a trademark covering goods: submit a photograph of the mark as it appears on the goods or packaging. "
        "For services: submit a screenshot or printout of the mark as it appears on your website or in advertising."
    )
    disclaimers = []
    if any(w in name.upper() for w in ["MARK", "BRAND", "TECH", "SMART", "NET", "SOFT"]):
        disclaimers.append(f"No claim is made to the exclusive right to use '{name.upper()}' apart from the mark as shown.")

    return {
        "goods_services": goods,
        "specimen_guidance": specimen,
        "classes": class_nums,
        "disclaimers": disclaimers,
        "teas_json": {
            "markName": name,
            "owner": owner,
            "ownerType": "INDIVIDUAL",
            "goodsAndServices": goods,
            "internationalClasses": class_nums,
            "basisFilingCode": "1a",
            "note": "Review and complete before filing. This is an AI-generated draft.",
        },
    }


async def draft_application(
    name: str, owner: str, goods_services_description: str
) -> dict:
    class_suggestions = await suggest_classes(goods_services_description)
    llm_result = await _llm_draft(name, owner, goods_services_description)
    if llm_result and "goods_services" in llm_result:
        llm_result.setdefault("classes", [c["class_number"] for c in class_suggestions[:3]])
        return llm_result
    return _static_draft(name, owner, goods_services_description, class_suggestions)
