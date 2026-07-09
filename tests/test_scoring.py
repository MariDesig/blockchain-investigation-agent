from blockchain_agent.models import PatternEvidence
from blockchain_agent.patterns.scoring import score_candidates


def test_score_candidates_groups_evidence_by_address() -> None:
    evidence = [
        PatternEvidence(
            pattern="common_counterparty",
            candidate_address="0xCANDIDATE",
            description="shared counterparty",
            weight=18,
        ),
        PatternEvidence(
            pattern="fan_out",
            candidate_address="0xCANDIDATE",
            description="fan out",
            weight=10,
        ),
    ]

    results = score_candidates(evidence)

    assert len(results) == 1
    assert results[0].address == "0xCANDIDATE"
    assert results[0].confidence == 38
    assert len(results[0].evidence) == 2


def test_score_candidates_caps_confidence() -> None:
    evidence = [
        PatternEvidence(
            pattern="common_counterparty",
            candidate_address="0xCANDIDATE",
            description="high weight",
            weight=100,
        )
    ]

    results = score_candidates(evidence)

    assert results[0].confidence == 95
