"""AI Trademark Copilot — LLM-powered Q&A grounded in trademark law."""

from __future__ import annotations

import json
import re
from typing import Optional
from uuid import UUID

import httpx

from app.core.config import settings

_SYSTEM_PROMPT = """You are an AI trademark attorney assistant for DClaw Trademark.
You help users with trademark law questions, clearance searches, portfolio management,
and USPTO filing guidance. Be concise, accurate, and always recommend consulting a
licensed attorney for formal legal advice.

When answering, suggest concrete next actions the user can take in the app.
Return a JSON object: {"reply": "<your answer>", "suggested_actions": [{"label": "<action label>", "action": "<route or command>"}]}
Limit suggested_actions to 3 items max."""


async def _call_llm(message: str, context: str = "") -> dict:
    user_content = f"{context}\n\nUser question: {message}" if context else message

    # Try OpenRouter
    if settings.openrouter_api_key:
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
                    json={
                        "model": "mistralai/mistral-7b-instruct",
                        "messages": [
                            {"role": "system", "content": _SYSTEM_PROMPT},
                            {"role": "user", "content": user_content},
                        ],
                        "temperature": 0.4,
                    },
                )
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"]
                match = re.search(r"\{.*\}", content, re.DOTALL)
                if match:
                    return json.loads(match.group())
        except Exception:
            pass

    # Fallback: Ollama — validate URL scheme to prevent SSRF
    if not settings.ollama_url.startswith(("http://", "https://")):
        return None
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{settings.ollama_url}/api/generate",
                json={
                    "model": "mistral",
                    "prompt": f"{_SYSTEM_PROMPT}\n\n{user_content}",
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


def _static_fallback(message: str) -> dict:
    """Return a helpful static response when no LLM is available."""
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["search", "conflict", "similar", "clear"]):
        reply = (
            "To check if your trademark is available, use the Clearance Search. "
            "Enter your proposed mark name, select relevant Nice classes, and review the conflict report."
        )
        actions = [{"label": "Run Clearance Search", "action": "/search"}]
    elif any(w in msg_lower for w in ["class", "nice", "goods", "service"]):
        reply = (
            "Nice Classification divides goods and services into 45 classes. "
            "Classes 1-34 cover goods; classes 35-45 cover services. "
            "Use the AI Class Recommender to find the right classes for your description."
        )
        actions = [{"label": "Browse Nice Classes", "action": "/classes"}, {"label": "Suggest Classes", "action": "/ai/suggest-classes"}]
    elif any(w in msg_lower for w in ["renew", "deadline", "expir", "due"]):
        reply = (
            "US trademarks must be renewed between years 5-6 (Section 8 declaration) "
            "and then every 10 years. Check your upcoming deadlines in the Deadlines section."
        )
        actions = [{"label": "View Upcoming Deadlines", "action": "/deadlines/upcoming"}]
    elif any(w in msg_lower for w in ["portfolio", "add", "creat", "register"]):
        reply = (
            "You can add a trademark to your portfolio by clicking 'New Trademark' on the Portfolio page. "
            "Fill in the mark name, owner, status, jurisdiction, and Nice classes."
        )
        actions = [{"label": "Add Trademark", "action": "/portfolio/new"}]
    else:
        reply = (
            "I'm your AI trademark assistant. I can help you with clearance searches, "
            "Nice class selection, deadline tracking, and portfolio management. "
            "What would you like to know?"
        )
        actions = [
            {"label": "View Portfolio", "action": "/portfolio"},
            {"label": "Search Trademarks", "action": "/search"},
        ]
    return {"reply": reply, "suggested_actions": actions}


async def chat(message: str, trademark_context: Optional[str] = None) -> dict:
    result = await _call_llm(message, context=trademark_context or "")
    if result and "reply" in result:
        return result
    return _static_fallback(message)
