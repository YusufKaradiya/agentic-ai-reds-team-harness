import re
from dataclasses import dataclass
from typing import List

from core.config_loader import ConfigLoader


@dataclass
class DetectionMatch:
    pattern_id: str
    pattern_name: str
    category: str
    severity: str
    matched_text: str


class DetectionEngine:

    def __init__(self, config_path="configs/detection-patterns.yaml"):
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.load()

        self.patterns = self.config.get("patterns", [])
        self.sensitive_patterns = self.config.get(
            "sensitive_patterns", []
        )

    def _scan_patterns(self, text: str, patterns: list) -> List[DetectionMatch]:
        matches = []

        if not text:
            return matches

        for item in patterns:

            if not item.get("enabled", True):
                continue

            pattern = item.get("pattern")

            if not pattern:
                continue

            try:
                result = re.search(pattern, text)

            except re.error:
                continue

            if result:
                matches.append(
                    DetectionMatch(
                        pattern_id=item.get("id", "UNKNOWN"),
                        pattern_name=item.get("name", "unknown"),
                        category=item.get("category", "unknown"),
                        severity=item.get("severity", "medium"),
                        matched_text=result.group(0),
                    )
                )

        return matches

    def scan_input(self, text: str) -> List[DetectionMatch]:
        return self._scan_patterns(
            text,
            self.patterns
        )

    def scan_output(self, text: str) -> List[DetectionMatch]:
        return self._scan_patterns(
            text,
            self.sensitive_patterns
        )

    def is_suspicious(self, text: str) -> bool:
        return len(self.scan_input(text)) > 0

    def has_sensitive_data(self, text: str) -> bool:
        return len(self.scan_output(text)) > 0

    def get_risk_score(self, matches: List[DetectionMatch]) -> float:

        if not matches:
            return 0.0

        severity_weights = {
            "low": 0.25,
            "medium": 0.50,
            "high": 0.75,
            "critical": 1.00,
        }

        scores = [
            severity_weights.get(match.severity, 0.50)
            for match in matches
        ]

        return min(max(scores), 1.0)