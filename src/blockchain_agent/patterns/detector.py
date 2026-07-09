from __future__ import annotations

from blockchain_agent.models import InvestigationGraph, PatternEvidence
from blockchain_agent.patterns.plugins import default_pattern_plugins
from blockchain_agent.patterns.registry import PatternRegistry


class PatternDetector:
    """Backward-compatible facade over the plugin registry.

    Existing code and tests can keep using PatternDetector, while the production
    architecture is now driven by independently registered pattern plugins.
    """

    def __init__(self, registry: PatternRegistry | None = None) -> None:
        self.registry = registry or PatternRegistry(default_pattern_plugins())

    def detect(self, graph: InvestigationGraph) -> list[PatternEvidence]:
        return self.registry.detect_all(graph)
