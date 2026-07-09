from blockchain_agent.agent import BlockchainInvestigationAgent
from blockchain_agent.graph_client.mock import MockGraphClient


def test_agent_returns_ranked_candidates() -> None:
    agent = BlockchainInvestigationAgent(graph_client=MockGraphClient())

    report = agent.investigate(
        seed_addresses=["0xSERVICE_A", "0xSERVICE_B"],
        network="ethereum",
        depth=2,
    )

    assert report.network == "ethereum"
    assert report.seed_addresses == ["0xSERVICE_A", "0xSERVICE_B"]
    assert report.candidates
    assert report.candidates[0].confidence >= report.candidates[-1].confidence


def test_agent_rejects_empty_seed_list() -> None:
    agent = BlockchainInvestigationAgent(graph_client=MockGraphClient())

    try:
        agent.investigate(seed_addresses=[], network="ethereum", depth=2)
    except ValueError as error:
        assert "seed address" in str(error)
    else:
        raise AssertionError("Expected ValueError")
