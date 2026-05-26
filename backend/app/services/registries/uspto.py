"""USPTO TSDR/TESS adapter — attempts real API, falls back to mock data."""

from __future__ import annotations

import re
from typing import Optional

import httpx

# USPTO Trademark Status and Document Retrieval (TSDR) public API
_TSDR_BASE = "https://tsdrapi.uspto.gov/ts/cd"
_TESS_SEARCH_BASE = "https://tmsearch.uspto.gov/api/search"


async def search_uspto(
    name: str,
    timeout: float = 8.0,
) -> list[dict]:
    """
    Query USPTO TESS public search API for marks similar to `name`.
    Falls back to an empty list (no crash) when the API is unreachable.
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(
                _TESS_SEARCH_BASE,
                params={
                    "query": f'"{name}"[BI]',  # basic index search
                    "hits": 10,
                    "offset": 0,
                },
                headers={"Accept": "application/json"},
            )
        if resp.status_code == 200:
            data = resp.json()
            hits = data.get("hits", {}).get("hits", [])
            return [_normalise_tess_hit(h) for h in hits]
    except Exception:
        pass
    return []


async def get_mark_status(serial_number: str, timeout: float = 8.0) -> Optional[dict]:
    """Fetch status for a single mark by USPTO serial number."""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(
                f"{_TSDR_BASE}/casestatus/sn{serial_number}/info.json",
                headers={"Accept": "application/json"},
            )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None


def _normalise_tess_hit(hit: dict) -> dict:
    src = hit.get("_source", {})
    return {
        "name": src.get("markVerbalElementText", ""),
        "owner": src.get("applicantName", ""),
        "jurisdiction": "US",
        "status": src.get("caseStatusDescriptionText", "Unknown"),
        "classes": [
            int(c.get("internationalClassNumber", 0))
            for c in src.get("classificationInformationBag", {}).get(
                "classificationInformation", []
            )
            if str(c.get("internationalClassNumber", "")).isdigit()
        ],
        "application_number": src.get("serialNumber", ""),
        "registration_date": src.get("registrationDate"),
        "source": "USPTO",
    }
