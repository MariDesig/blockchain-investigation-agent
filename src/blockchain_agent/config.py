from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    default_network: str = "ethereum"
    default_depth: int = 2
    graph_api_base_url: str = "https://api-kyt.bittax.ru"
    graph_api_token: str | None = None


def load_settings() -> Settings:
    return Settings(
        default_network=os.getenv("DEFAULT_NETWORK", "ethereum"),
        default_depth=int(os.getenv("DEFAULT_DEPTH", "2")),
        graph_api_base_url=os.getenv("GRAPH_API_BASE_URL", "https://api-kyt.bittax.ru"),
        graph_api_token=os.getenv("GRAPH_API_TOKEN") or None,
    )
