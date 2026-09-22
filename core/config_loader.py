from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:
    """Loads YAML configuration files."""

    def __init__(self, config_root: Path | str):
        self.config_root = Path(config_root)

    def load_yaml(self, relative_path: str) -> dict[str, Any]:
        path = self.config_root / relative_path

        if not path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {path}"
            )

        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if data is None:
            return {}

        if not isinstance(data, dict):
            raise ValueError(
                f"Expected YAML object in {path}"
            )

        return data

    def load_attack(self, filename: str) -> dict[str, Any]:
        return self.load_yaml(
            f"attacks/{filename}"
        )

    def load_tools(self) -> dict[str, Any]:
        return self.load_yaml("attacks/tools.yaml")

    def load_policies(self) -> dict[str, Any]:
        return self.load_yaml("attacks/policies.yaml")

    def load_model(self) -> dict[str, Any]:
        return self.load_yaml("attacks/model.yaml")

    def load_evaluation(self) -> dict[str, Any]:
        return self.load_yaml("attacks/evaluation.yaml")