from __future__ import annotations

from blockchain_agent.models import InvestigationReport


class ReportGenerator:
    """Creates a readable analyst-facing report."""

    def to_markdown(self, report: InvestigationReport) -> str:
        lines: list[str] = []
        lines.append("# Blockchain Investigation Report")
        lines.append("")
        lines.append(f"Network: `{report.network}`")
        lines.append(f"Seed addresses: {', '.join(f'`{address}`' for address in report.seed_addresses)}")
        lines.append("")

        if not report.candidates:
            lines.append("No candidate addresses were detected.")
            return "\n".join(lines)

        lines.append("## Candidate addresses")
        lines.append("")
        for index, candidate in enumerate(report.candidates, start=1):
            lines.append(f"### {index}. `{candidate.address}`")
            lines.append("")
            lines.append(f"Confidence: **{candidate.confidence}%**")
            lines.append("")
            lines.append("Evidence:")
            for item in candidate.evidence:
                txs = ", ".join(f"`{tx}`" for tx in item.related_transactions)
                lines.append(f"- **{item.pattern}**: {item.description}")
                if txs:
                    lines.append(f"  - Transactions: {txs}")
            lines.append("")
            lines.append("Manual review: recommended before applying service labels.")
            lines.append("")

        return "\n".join(lines)
