# Blockchain Investigation Agent

Professional MVP for blockchain investigation and address-pattern discovery.

The project is designed to help analysts start from one or more known service addresses, explore a transaction graph, detect behavioral patterns, rank candidate addresses, and produce an explainable report.

> Current stage: mock graph client + deterministic pattern engine. The architecture is prepared for later integration with internal `graph/*` API methods.

## What the agent does

- accepts seed blockchain addresses;
- expands a transaction graph to a configurable depth;
- detects investigation patterns such as common counterparties, shared intermediates, fan-in, fan-out, chain transfers, and consolidation;
- assigns a confidence score to candidate addresses;
- produces a Markdown/JSON-style investigation report;
- keeps the graph client replaceable, so the mock implementation can later be swapped for `graph.bittax.ru` or another internal API.

## Architecture

```text
User / Analyst
  -> Agent
  -> Graph Client
  -> Pattern Detector
  -> Scoring Engine
  -> Report Generator
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
python -m blockchain_agent.main --network ethereum --seeds 0xSERVICE_A 0xSERVICE_B --depth 2
```

## Docker start

```bash
docker compose up --build
```

## Repository structure

```text
src/blockchain_agent/
  agent.py              # orchestration logic
  config.py             # runtime settings
  main.py               # CLI entrypoint
  graph_client/         # mock and future real API clients
  patterns/             # deterministic investigation rules
  reports/              # report generation
docs/
  architecture.md
  patterns.md
  graph_api_integration.md
  roadmap.md
tests/
  test_patterns.py
  test_scoring.py
```

## Integration plan

The mock client implements the same interface that a future real client should implement:

```python
get_transactions(address: str, network: str) -> list[Transaction]
expand(seed_addresses: list[str], network: str, depth: int) -> InvestigationGraph
```

When `graph/*` Swagger documentation is available, add a real client in:

```text
src/blockchain_agent/graph_client/bittax.py
```

and keep the rest of the agent unchanged.
