"""Trademark clearance search service — Phase A (structured mock results)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from app.services.similarity import RiskLevel, SimilarityResult, compute_similarity

# Static sample marks that mimic realistic USPTO records.
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
    registration_date: str | None
    similarity: SimilarityResult
    conflict_type: str = field(init=False)

    def __post_init__(self) -> None:
        ph = self.similarity.phonetic_score
        sem = self.similarity.semantic_score
        if ph > sem:
            self.conflict_type = "Phonetic"
        elif sem > ph:
            self.conflict_type = "Semantic"
        else:
            self.conflict_type = "Combined"


def run_clearance_search(
    name: str,
    classes: list[int] | None = None,
    jurisdiction: str | None = None,
    min_score: float = 0.2,
) -> list[dict]:
    """Search mock mark database and return conflicts above threshold, sorted by score."""
    results: list[SearchResult] = []
    for mark in _SAMPLE_MARKS:
        if jurisdiction and mark["jurisdiction"] != jurisdiction:
            continue
        if classes and not set(classes).intersection(set(mark["classes"])):
            continue
        sim = compute_similarity(name, mark["name"])
        if sim.combined_score >= min_score:
            results.append(
                SearchResult(
                    name=mark["name"],
                    owner=mark["owner"],
                    jurisdiction=mark["jurisdiction"],
                    status=mark["status"],
                    classes=mark["classes"],
                    application_number=mark["application_number"],
                    registration_date=mark["registration_date"],
                    similarity=sim,
                )
            )

    results.sort(key=lambda r: r.similarity.combined_score, reverse=True)
    return [
        {
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
        }
        for r in results
    ]
