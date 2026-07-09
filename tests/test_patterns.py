from blockchain_agent.graph_client.mock import MockGraphClient
from blockchain_agent.patterns.detector import PatternDetector


def test_detector_finds_candidates_on_mock_graph() -> None:
    graph = MockGraphClient().expand(
        seed_addresses=["0xSERVICE_A", "0xSERVICE_B"],
        network="ethereum",
        depth=2,
    )

    evidence = PatternDetector().detect(graph)
    candidate_addresses = {item.candidate_address for item in evidence}

    assert "0xHUB_1" in candidate_addresses
    assert "0xCANDIDATE_1" in candidate_addresses
    assert "0xCANDIDATE_2" in candidate_addresses


def test_detector_produces_explainable_evidence() -> None:
    graph = MockGraphClient().expand(
        seed_addresses=["0xSERVICE_A", "0xSERVICE_B"],
        network="ethereum",
        depth=2,
    )

    evidence = PatternDetector().detect(graph)

    assert evidence
    assert all(item.description for item in evidence)
    assert all(item.weight > 0 for item in evidence)
