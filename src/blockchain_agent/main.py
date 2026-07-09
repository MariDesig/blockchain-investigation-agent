from __future__ import annotations

import argparse

from rich.console import Console
from rich.markdown import Markdown

from blockchain_agent.agent import BlockchainInvestigationAgent
from blockchain_agent.config import load_settings
from blockchain_agent.graph_client.mock import MockGraphClient
from blockchain_agent.reports.generator import ReportGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a blockchain investigation on seed addresses")
    parser.add_argument("--network", default=None, help="Blockchain network, for example ethereum")
    parser.add_argument("--seeds", nargs="+", required=True, help="Known service addresses")
    parser.add_argument("--depth", type=int, default=None, help="Graph expansion depth")
    return parser


def main() -> None:
    settings = load_settings()
    args = build_parser().parse_args()

    network = args.network or settings.default_network
    depth = args.depth or settings.default_depth

    agent = BlockchainInvestigationAgent(graph_client=MockGraphClient())
    report = agent.investigate(seed_addresses=args.seeds, network=network, depth=depth)
    markdown = ReportGenerator().to_markdown(report)

    console = Console()
    console.print(Markdown(markdown))


if __name__ == "__main__":
    main()
