from __future__ import annotations

from blockchain_agent.graph_client.base import GraphClient
from blockchain_agent.models import InvestigationReport
from blockchain_agent.patterns.detector import PatternDetector
from blockchain_agent.patterns.scoring import score_candidates


class BlockchainInvestigationAgent:
    """Coordinates graph expansion, pattern detection, scoring, and reporting."""

    def __init__(self, graph_client: GraphClient, detector: PatternDetector | None = None) -> None:
        self.graph_client = graph_client
        self.detector = detector or PatternDetector()

    def investigate(self, seed_addresses: list[str], network: str, depth: int) -> InvestigationReport:
        if not seed_addresses:
            raise ValueError("At least one seed address is required")
        if depth < 1:
            raise ValueError("Depth must be at least 1")

        graph = self.graph_client.expand(seed_addresses=seed_addresses, network=network, depth=depth)
        evidence = self.detector.detect(graph)
        candidates = score_candidates(evidence)

        seed_set = set(seed_addresses)
        filtered_candidates = [candidate for candidate in candidates if candidate.address not in seed_set]

        return InvestigationReport(
            network=network,
            seed_addresses=seed_addresses,
            candidates=filtered_candidates,
        )
