from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations

from blockchain_agent.models import InvestigationGraph, PatternEvidence, Transaction


class PatternDetector:
    """Deterministic pattern detector for early blockchain investigations.

    The detector intentionally uses explainable rules instead of hidden heuristics.
    This makes MVP results easier for analysts to review and correct.
    """

    def detect(self, graph: InvestigationGraph) -> list[PatternEvidence]:
        seed_set = set(graph.seed_addresses)
        evidence: list[PatternEvidence] = []
        evidence.extend(self._detect_common_counterparties(graph, seed_set))
        evidence.extend(self._detect_shared_intermediates(graph, seed_set))
        evidence.extend(self._detect_fan_out(graph, seed_set))
        evidence.extend(self._detect_fan_in(graph, seed_set))
        evidence.extend(self._detect_chain_transfers(graph, seed_set))
        evidence.extend(self._detect_consolidation(graph, seed_set))
        return evidence

    def _detect_common_counterparties(
        self, graph: InvestigationGraph, seed_set: set[str]
    ) -> list[PatternEvidence]:
        counterparties_by_seed: dict[str, set[str]] = defaultdict(set)
        txs_by_pair: dict[tuple[str, str], list[str]] = defaultdict(list)

        for tx in graph.transactions:
            if tx.source in seed_set and tx.target not in seed_set:
                counterparties_by_seed[tx.source].add(tx.target)
                txs_by_pair[(tx.source, tx.target)].append(tx.tx_hash)
            if tx.target in seed_set and tx.source not in seed_set:
                counterparties_by_seed[tx.target].add(tx.source)
                txs_by_pair[(tx.target, tx.source)].append(tx.tx_hash)

        evidence: list[PatternEvidence] = []
        for seed_a, seed_b in combinations(counterparties_by_seed.keys(), 2):
            shared = counterparties_by_seed[seed_a] & counterparties_by_seed[seed_b]
            for candidate in shared:
                tx_hashes = txs_by_pair[(seed_a, candidate)] + txs_by_pair[(seed_b, candidate)]
                evidence.append(
                    PatternEvidence(
                        pattern="common_counterparty",
                        candidate_address=candidate,
                        description=(
                            f"Address {candidate} is a direct counterparty of multiple seed "
                            f"addresses: {seed_a}, {seed_b}."
                        ),
                        related_transactions=tx_hashes,
                        weight=18,
                    )
                )
        return evidence

    def _detect_shared_intermediates(
        self, graph: InvestigationGraph, seed_set: set[str]
    ) -> list[PatternEvidence]:
        outgoing: dict[str, list[Transaction]] = defaultdict(list)
        incoming: dict[str, list[Transaction]] = defaultdict(list)
        for tx in graph.transactions:
            outgoing[tx.source].append(tx)
            incoming[tx.target].append(tx)

        evidence: list[PatternEvidence] = []
        for intermediate in graph.addresses - seed_set:
            seed_touch = [tx for tx in incoming[intermediate] + outgoing[intermediate] if tx.source in seed_set or tx.target in seed_set]
            if not seed_touch:
                continue
            for tx in outgoing[intermediate]:
                if tx.target not in seed_set:
                    evidence.append(
                        PatternEvidence(
                            pattern="shared_intermediate_wallet",
                            candidate_address=tx.target,
                            description=(
                                f"Address {tx.target} is reachable through intermediate wallet "
                                f"{intermediate}, which interacts with known seed addresses."
                            ),
                            related_transactions=[item.tx_hash for item in seed_touch] + [tx.tx_hash],
                            weight=14,
                        )
                    )
        return evidence

    def _detect_fan_out(self, graph: InvestigationGraph, seed_set: set[str]) -> list[PatternEvidence]:
        outgoing: dict[str, list[Transaction]] = defaultdict(list)
        for tx in graph.transactions:
            outgoing[tx.source].append(tx)

        evidence: list[PatternEvidence] = []
        for source, txs in outgoing.items():
            unique_targets = {tx.target for tx in txs}
            if len(unique_targets) >= 3:
                for candidate in unique_targets - seed_set:
                    evidence.append(
                        PatternEvidence(
                            pattern="fan_out",
                            candidate_address=candidate,
                            description=(
                                f"Address {candidate} receives funds from {source}, which distributes "
                                f"funds to {len(unique_targets)} different targets."
                            ),
                            related_transactions=[tx.tx_hash for tx in txs],
                            weight=10,
                        )
                    )
        return evidence

    def _detect_fan_in(self, graph: InvestigationGraph, seed_set: set[str]) -> list[PatternEvidence]:
        incoming: dict[str, list[Transaction]] = defaultdict(list)
        for tx in graph.transactions:
            incoming[tx.target].append(tx)

        evidence: list[PatternEvidence] = []
        for target, txs in incoming.items():
            unique_sources = {tx.source for tx in txs}
            if len(unique_sources) >= 3 and target not in seed_set:
                evidence.append(
                    PatternEvidence(
                        pattern="fan_in",
                        candidate_address=target,
                        description=(
                            f"Address {target} receives funds from {len(unique_sources)} different "
                            "sources, which can indicate deposit or aggregation behavior."
                        ),
                        related_transactions=[tx.tx_hash for tx in txs],
                        weight=12,
                    )
                )
        return evidence

    def _detect_chain_transfers(
        self, graph: InvestigationGraph, seed_set: set[str]
    ) -> list[PatternEvidence]:
        outgoing: dict[str, list[Transaction]] = defaultdict(list)
        for tx in graph.transactions:
            outgoing[tx.source].append(tx)

        evidence: list[PatternEvidence] = []
        for tx1 in graph.transactions:
            if tx1.source not in seed_set:
                continue
            for tx2 in outgoing.get(tx1.target, []):
                if tx2.target not in seed_set:
                    evidence.append(
                        PatternEvidence(
                            pattern="chain_transfer",
                            candidate_address=tx2.target,
                            description=(
                                f"Address {tx2.target} appears in a two-hop chain from seed "
                                f"{tx1.source} via {tx1.target}."
                            ),
                            related_transactions=[tx1.tx_hash, tx2.tx_hash],
                            weight=13,
                        )
                    )
        return evidence

    def _detect_consolidation(
        self, graph: InvestigationGraph, seed_set: set[str]
    ) -> list[PatternEvidence]:
        incoming: dict[str, list[Transaction]] = defaultdict(list)
        for tx in graph.transactions:
            incoming[tx.target].append(tx)

        evidence: list[PatternEvidence] = []
        for target, txs in incoming.items():
            amount_buckets = Counter(round(tx.amount, 1) for tx in txs)
            repeated_amounts = [amount for amount, count in amount_buckets.items() if count >= 2]
            if target not in seed_set and len(txs) >= 2 and repeated_amounts:
                evidence.append(
                    PatternEvidence(
                        pattern="consolidation",
                        candidate_address=target,
                        description=(
                            f"Address {target} receives repeated similar amounts "
                            f"{repeated_amounts}, suggesting consolidation behavior."
                        ),
                        related_transactions=[tx.tx_hash for tx in txs],
                        weight=11,
                    )
                )
        return evidence
