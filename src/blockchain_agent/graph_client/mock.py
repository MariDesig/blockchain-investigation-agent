from __future__ import annotations

from blockchain_agent.graph_client.base import GraphClient
from blockchain_agent.models import InvestigationGraph, Transaction


MOCK_TRANSACTIONS = [
    Transaction("tx001", "ethereum", "0xSERVICE_A", "0xHUB_1", 12.4, "2026-07-08T10:00:00Z"),
    Transaction("tx002", "ethereum", "0xSERVICE_B", "0xHUB_1", 9.1, "2026-07-08T10:02:00Z"),
    Transaction("tx003", "ethereum", "0xHUB_1", "0xCANDIDATE_1", 21.3, "2026-07-08T10:05:00Z"),
    Transaction("tx004", "ethereum", "0xCANDIDATE_1", "0xOUT_1", 5.0, "2026-07-08T10:07:00Z"),
    Transaction("tx005", "ethereum", "0xCANDIDATE_1", "0xOUT_2", 5.0, "2026-07-08T10:08:00Z"),
    Transaction("tx006", "ethereum", "0xCANDIDATE_1", "0xOUT_3", 5.0, "2026-07-08T10:09:00Z"),
    Transaction("tx007", "ethereum", "0xUSER_1", "0xSERVICE_A", 1.2, "2026-07-08T10:10:00Z"),
    Transaction("tx008", "ethereum", "0xUSER_2", "0xSERVICE_A", 2.4, "2026-07-08T10:11:00Z"),
    Transaction("tx009", "ethereum", "0xUSER_3", "0xSERVICE_A", 3.1, "2026-07-08T10:12:00Z"),
    Transaction("tx010", "ethereum", "0xCANDIDATE_2", "0xHUB_1", 8.8, "2026-07-08T10:13:00Z"),
    Transaction("tx011", "ethereum", "0xCANDIDATE_2", "0xHUB_2", 8.7, "2026-07-08T10:14:00Z"),
    Transaction("tx012", "ethereum", "0xHUB_2", "0xSERVICE_B", 8.6, "2026-07-08T10:16:00Z"),
]


class MockGraphClient(GraphClient):
    """Small deterministic graph used until real graph/* API documentation is available."""

    def get_transactions(self, address: str, network: str) -> list[Transaction]:
        return [
            tx
            for tx in MOCK_TRANSACTIONS
            if tx.network == network and (tx.source == address or tx.target == address)
        ]

    def expand(self, seed_addresses: list[str], network: str, depth: int) -> InvestigationGraph:
        if depth < 1:
            return InvestigationGraph(seed_addresses=seed_addresses, transactions=[])

        discovered = set(seed_addresses)
        transactions: list[Transaction] = []

        for _ in range(depth):
            frontier = set(discovered)
            for tx in MOCK_TRANSACTIONS:
                if tx.network != network:
                    continue
                if tx.source in frontier or tx.target in frontier:
                    if tx not in transactions:
                        transactions.append(tx)
                    discovered.add(tx.source)
                    discovered.add(tx.target)

        return InvestigationGraph(seed_addresses=seed_addresses, transactions=transactions)
