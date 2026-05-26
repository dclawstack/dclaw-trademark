"""Phonetic + semantic similarity scoring for trademark conflict detection."""

import re
from dataclasses import dataclass
from enum import Enum

import jellyfish


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    IDENTICAL = "Identical"


@dataclass
class SimilarityResult:
    phonetic_score: float
    semantic_score: float
    combined_score: float
    risk_level: RiskLevel
    phonetic_match: str  # Double Metaphone of query
    candidate_phonetic: str  # Double Metaphone of candidate


def _metaphone(name: str) -> str:
    return jellyfish.metaphone(name.upper())


def _normalize(name: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", name.lower())).strip()


def phonetic_score(name_a: str, name_b: str) -> float:
    """Jaro-Winkler similarity between the Double Metaphone codes of two mark names."""
    meta_a = _metaphone(name_a)
    meta_b = _metaphone(name_b)
    if not meta_a or not meta_b:
        return 0.0
    return float(jellyfish.jaro_winkler_similarity(meta_a, meta_b))


def _token_set(name: str) -> set[str]:
    return set(_normalize(name).split())


def semantic_score(name_a: str, name_b: str) -> float:
    """Token-overlap + character Jaro-Winkler similarity between two mark names."""
    tokens_a = _token_set(name_a)
    tokens_b = _token_set(name_b)
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    jaccard = len(intersection) / len(union)
    char_sim = float(jellyfish.jaro_winkler_similarity(_normalize(name_a), _normalize(name_b)))
    return (jaccard + char_sim) / 2.0


def compute_similarity(query: str, candidate: str) -> SimilarityResult:
    """Compute combined similarity score with risk bucket assignment."""
    ph = phonetic_score(query, candidate)
    sem = semantic_score(query, candidate)
    # Weighted average: phonetic similarity is slightly more important for trademarks
    combined = round(0.55 * ph + 0.45 * sem, 4)

    if combined >= 0.9:
        risk = RiskLevel.IDENTICAL
    elif combined >= 0.6:
        risk = RiskLevel.HIGH
    elif combined >= 0.3:
        risk = RiskLevel.MEDIUM
    else:
        risk = RiskLevel.LOW

    return SimilarityResult(
        phonetic_score=round(ph, 4),
        semantic_score=round(sem, 4),
        combined_score=combined,
        risk_level=risk,
        phonetic_match=_metaphone(query),
        candidate_phonetic=_metaphone(candidate),
    )
