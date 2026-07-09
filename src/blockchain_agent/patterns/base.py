from __future__ import annotations

from abc import ABC, abstractmethod

from blockchain_agent.models import InvestigationGraph, PatternEvidence


class PatternPlugin(ABC):
    """Base interface for explainable deterministic investigation patterns."""

    name: str
    description: str

    @abstractmethod
    def detect(self, graph: InvestigationGraph, seed_set: set[str]) -> list[PatternEvidence]:
        """Return evidence found by this pattern plugin."""
