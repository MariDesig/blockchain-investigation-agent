from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


Address = str
PatternName = Literal[
    "common_counterparty",
    "shared_intermediate_wallet",
    "fan_in",
    "fan_out",
    "chain_transfer",
    "consolidation",
]
HypothesisStatus = Literal["proposed", "supported", "weak", "rejected"]
AuditEventLevel = Literal["debug", "info", "warning", "error"]


@dataclass(frozen=True)
class Transaction:
    tx_hash: str
    network: str
    source: Address
    target: Address
    amount: float
    timestamp: str


@dataclass
class InvestigationGraph:
    seed_addresses: list[Address]
    transactions: list[Transaction]

    @property
    def addresses(self) -> set[Address]:
        result: set[Address] = set(self.seed_addresses)
        for tx in self.transactions:
            result.add(tx.source)
            result.add(tx.target)
        return result


@dataclass
class PatternEvidence:
    pattern: PatternName
    candidate_address: Address
    description: str
    related_transactions: list[str] = field(default_factory=list)
    weight: int = 10


@dataclass
class CandidateResult:
    address: Address
    confidence: int
    evidence: list[PatternEvidence]


@dataclass
class Hypothesis:
    candidate_address: Address
    statement: str
    status: HypothesisStatus
    support_score: int
    supporting_evidence: list[PatternEvidence] = field(default_factory=list)
    contradicting_factors: list[str] = field(default_factory=list)
    next_checks: list[str] = field(default_factory=list)


@dataclass
class AuditEvent:
    step: str
    message: str
    level: AuditEventLevel = "info"
    metadata: dict[str, str | int | float | bool] = field(default_factory=dict)


@dataclass
class InvestigationMemoryRecord:
    network: str
    seed_addresses: list[Address]
    hypotheses: list[Hypothesis]
    audit_events: list[AuditEvent]


@dataclass
class InvestigationReport:
    network: str
    seed_addresses: list[Address]
    candidates: list[CandidateResult]
    hypotheses: list[Hypothesis] = field(default_factory=list)
    audit_events: list[AuditEvent] = field(default_factory=list)
