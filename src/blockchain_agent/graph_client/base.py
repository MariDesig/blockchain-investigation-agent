from __future__ import annotations

from abc import ABC, abstractmethod

from blockchain_agent.models import InvestigationGraph, Transaction


class GraphClient(ABC):
    """Interface for blockchain graph data providers.

    A future Bittax client should implement this interface using internal `graph/*` API methods.
    """

    @abstractmethod
    def get_transactions(self, address: str, network: str) -> list[Transaction]:
        """Return transactions related to one address."""

    @abstractmethod
    def expand(self, seed_addresses: list[str], network: str, depth: int) -> InvestigationGraph:
        """Return an expanded transaction graph for the provided seed addresses."""
