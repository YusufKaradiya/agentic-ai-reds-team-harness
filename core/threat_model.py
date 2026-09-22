from pathlib import Path
from typing import Any

from core.config_loader import ConfigLoader


class ThreatModel:
    def __init__(self, config_root: Path):
        self.loader = ConfigLoader(config_root)
        self.data = self.loader.load_yaml(
            "threat-model.yaml"
        )

    @property
    def assets(self) -> list[dict[str, Any]]:
        return self.data.get("assets", [])

    @property
    def trust_boundaries(self) -> list[dict[str, Any]]:
        return self.data.get(
            "trust_boundaries",
            []
        )

    @property
    def threats(self) -> list[dict[str, Any]]:
        return self.data.get("threats", [])

    def get_threat(self, threat_id: str):
        for threat in self.threats:
            if threat["id"] == threat_id:
                return threat

        raise KeyError(
            f"Threat not found: {threat_id}"
        )