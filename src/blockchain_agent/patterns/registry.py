from __future__ import annotations

from blockchain_agent.models import InvestigationGraph, PatternEvidence
from blockchain_agent.patterns.base import PatternPlugin


class PatternRegistry:
    """Registry for deterministic pattern plugins.

    The registry keeps pattern discovery extensible: new rules can be added as
    independent plugins without changing the investigation agent.
    """

    def __init__(self, plugins: list[PatternPlugin] | None = None) -> None:
        self._plugins: list[PatternPlugin] = []
        for plugin in plugins or []:
            self.register(plugin)

    @property
    def plugins(self) -> list[PatternPlugin]:
        return list(self._plugins)

    def register(self, plugin: PatternPlugin) -> None:
        existing_names = {item.name for item in self._plugins}
        if plugin.name in existing_names:
            raise ValueError(f"Pattern plugin already registered: {plugin.name}")
        self._plugins.append(plugin)

    def detect_all(self, graph: InvestigationGraph) -> list[PatternEvidence]:
        seed_set = set(graph.seed_addresses)
        evidence: list[PatternEvidence] = []
        for plugin in self._plugins:
            evidence.extend(plugin.detect(graph, seed_set))
        return evidence
