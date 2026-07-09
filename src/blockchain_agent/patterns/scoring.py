from __future__ import annotations

from collections import defaultdict

from blockchain_agent.models import CandidateResult, PatternEvidence


MAX_CONFIDENCE = 95


def score_candidates(evidence: list[PatternEvidence]) -> list[CandidateResult]:
    grouped: dict[str, list[PatternEvidence]] = defaultdict(list)
    for item in evidence:
        grouped[item.candidate_address].append(item)

    results: list[CandidateResult] = []
    for address, items in grouped.items():
        raw_score = sum(item.weight for item in items)
        diversity_bonus = len({item.pattern for item in items}) * 5
        confidence = min(MAX_CONFIDENCE, raw_score + diversity_bonus)
        results.append(CandidateResult(address=address, confidence=confidence, evidence=items))

    return sorted(results, key=lambda result: result.confidence, reverse=True)
