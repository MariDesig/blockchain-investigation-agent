from __future__ import annotations

from blockchain_agent.graph_client.base import GraphClient
from blockchain_agent.models import InvestigationGraph, Transaction


class BittaxGraphClient(GraphClient):
    """Placeholder for future internal graph/* API integration.

    This client should be implemented after Swagger methods, request parameters,
    response schemas, authentication, and pagination rules are confirmed.
    """

    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    def get_transactions(self, address: str, network: str) -> list[Transaction]:
        raise NotImplementedError("Implement after graph/* Swagger schema is available")

    def expand(self, seed_addresses: list[str], network: str, depth: int) -> InvestigationGraph:
        raise NotImplementedError("Implement after graph/* Swagger schema is available")
