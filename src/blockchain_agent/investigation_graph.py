from __future__ import annotations

from collections import deque

import networkx as nx

from blockchain_agent.models import InvestigationGraph, Transaction


class GraphAnalyzer:
    """Graph algorithms used by investigation and explanation layers."""

    def __init__(self, graph: InvestigationGraph) -> None:
        self.source_graph = graph
        self.graph = nx.MultiDiGraph()
        self._build()

    def _build(self) -> None:
        for address in self.source_graph.addresses:
            self.graph.add_node(address)
        for tx in self.source_graph.transactions:
            self.graph.add_edge(
                tx.source,
                tx.target,
                key=tx.tx_hash,
                tx_hash=tx.tx_hash,
                amount=tx.amount,
                timestamp=tx.timestamp,
                network=tx.network,
            )

    def shortest_seed_path(self, candidate_address: str) -> list[str] | None:
        """Return the shortest address path from any seed to candidate, if one exists."""
        best_path: list[str] | None = None
        for seed in self.source_graph.seed_addresses:
            try:
                path = nx.shortest_path(self.graph, seed, candidate_address)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
            if best_path is None or len(path) < len(best_path):
                best_path = path
        return best_path

    def neighborhood(self, address: str, max_depth: int = 1) -> set[str]:
        """Return addresses reachable from the given address within max_depth hops."""
        if address not in self.graph:
            return set()

        visited = {address}
        queue: deque[tuple[str, int]] = deque([(address, 0)])
        while queue:
            current, depth = queue.popleft()
            if depth >= max_depth:
                continue
            neighbors = set(self.graph.successors(current)) | set(self.graph.predecessors(current))
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        visited.remove(address)
        return visited

    def centrality(self) -> dict[str, float]:
        """Return degree centrality for all addresses in a simple directed projection."""
        simple_graph = nx.DiGraph(self.graph)
        return nx.degree_centrality(simple_graph)

    def transactions_between(self, source: str, target: str) -> list[Transaction]:
        return [
            tx
            for tx in self.source_graph.transactions
            if tx.source == source and tx.target == target
        ]
