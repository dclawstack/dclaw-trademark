"""Trademark clearance search — Phase A fixture corpus + Phase B USPTO live adapter."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.similarity import SimilarityResult, compute_similarity

# ── Fixture corpus (Phase A) ──────────────────────────────────────────────────
# Kept as a realistic baseline; supplemented by live USPTO results in Phase B.
_SAMPLE_MARKS: list[dict] = [
    {"name": "NovaMark", "owner": "NovaMark LLC", "jurisdiction": "US", "status": "Registered", "classes": [9, 42], "application_number": "US79000001", "registration_date": "2019-03-15"},
    {"name": "NovaMarket", "owner": "NovaMarket Inc", "jurisdiction": "US", "status": "Registered", "classes": [35], "application_number": "US79000002", "registration_date": "2020-07-22"},
    {"name": "Nova Mark Pro", "owner": "Nova Solutions", "jurisdiction": "EU", "status": "Registered", "classes": [42], "application_number": "EU018000001", "registration_date": "2021-01-10"},
    {"name": "SkyBrand", "owner": "SkyBrand GmbH", "jurisdiction": "US", "status": "Registered", "classes": [25, 35], "application_number": "US79000010", "registration_date": "2018-05-01"},
    {"name": "SkiBrands", "owner": "Mountain LLC", "jurisdiction": "US", "status": "Pending", "classes": [28], "application_number": "US79000011", "registration_date": None},
    {"name": "BlueMark", "owner": "BlueMark Corp", "jurisdiction": "US", "status": "Registered", "classes": [9], "application_number": "US79000020", "registration_date": "2017-11-30"},
    {"name": "BlueMarker", "owner": "Stationery Co", "jurisdiction": "EU", "status": "Registered", "classes": [16], "application_number": "EU018000020", "registration_date": "2022-02-14"},
    {"name": "TechBrand", "owner": "TechBrand Inc", "jurisdiction": "US", "status": "Registered", "classes": [9, 42], "application_number": "US79000030", "registration_date": "2016-08-19"},
    {"name": "Tech Brand Solutions", "owner": "TBS Ltd", "jurisdiction": "WO", "status": "Registered", "classes": [42], "application_number": "WO2016000001", "registration_date": "2016-12-01"},
    {"name": "AlphaMark", "owner": "Alpha Corp", "jurisdiction": "US", "status": "Registered", "classes": [9, 35, 42], "application_number": "US79000040", "registration_date": "2015-03-28"},
]


@dataclass
class SearchResult:
    name: str
    owner: str
    jurisdiction: str
    status: str
    classes: list[int]
    application_number: str
    registration_date: Optional[str]
    similarity: SimilarityResult
    source: str = "fixture"
    conflict_type: str = field(init=False)

    def __post_init__(self) -> None:
        ph = self.similarity.phonetic_score
        sem = self.similarity.semantic_score
        self.conflict_type = "Phonetic" if ph > sem else ("Semantic" if sem > ph else "Combined")


def _score_mark(name: str, mark: dict) -> Optional[SearchResult]:
    sim = compute_similarity(name, mark["name"])
    return SearchResult(
        name=mark["name"],
        owner=mark.get("owner", ""),
        jurisdiction=mark.get("jurisdiction", "US"),
        status=mark.get("status", "Unknown"),
        classes=mark.get("classes", []),
        application_number=mark.get("application_number", ""),
        registration_date=mark.get("registration_date"),
        similarity=sim,
        source=mark.get("source", "fixture"),
    )


def _to_dict(r: SearchResult) -> dict:
    return {
        "name": r.name,
        "owner": r.owner,
        "jurisdiction": r.jurisdiction,
        "status": r.status,
        "classes": r.classes,
        "application_number": r.application_number,
        "registration_date": r.registration_date,
        "phonetic_score": r.similarity.phonetic_score,
        "semantic_score": r.similarity.semantic_score,
        "similarity_score": r.similarity.combined_score,
        "risk_level": r.similarity.risk_level.value,
        "conflict_type": r.conflict_type,
        "source": r.source,
    }


async def run_clearance_search(
    name: str,
    classes: Optional[list[int]] = None,
    jurisdiction: Optional[str] = None,
    min_score: float = 0.2,
    db: Optional[AsyncSession] = None,
) -> list[dict]:
    """
    Run clearance search against live USPTO (Phase B) + fixture corpus (Phase A).
    Logs the query to search_queries if a DB session is provided.
    """
    # Phase B: attempt live USPTO search for US jurisdiction
    live_marks: list[dict] = []
    if not jurisdiction or jurisdiction == "US":
        try:
            from app.services.registries.uspto import search_uspto
            live_marks = await search_uspto(name)
        except Exception:
            pass

    # Merge live results with fixture corpus (deduplicate by application_number)
    seen: set[str] = set()
    candidate_marks: list[dict] = []
    for m in live_marks:
        key = m.get("application_number", m["name"])
        if key not in seen:
            seen.add(key)
            candidate_marks.append(m)
    for m in _SAMPLE_MARKS:
        key = m.get("application_number", m["name"])
        if key not in seen:
            seen.add(key)
            candidate_marks.append(m)

    # Score and filter
    results: list[SearchResult] = []
    for mark in candidate_marks:
        if jurisdiction and mark.get("jurisdiction") != jurisdiction:
            continue
        if classes and not set(classes).intersection(set(mark.get("classes", []))):
            continue
        r = _score_mark(name, mark)
        if r.similarity.combined_score >= min_score:
            results.append(r)

    results.sort(key=lambda r: r.similarity.combined_score, reverse=True)
    output = [_to_dict(r) for r in results]

    # Audit log
    if db is not None:
        try:
            from app.models.search_query import SearchQuery
            db.add(SearchQuery(
                query_name=name,
                jurisdiction=jurisdiction,
                classes_json=json.dumps(classes) if classes else None,
                result_count=len(output),
                top_score=output[0]["similarity_score"] if output else None,
            ))
            await db.commit()
        except Exception:
            pass

    return output
