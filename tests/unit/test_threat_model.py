from pathlib import Path

from core.threat_model import ThreatModel


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_threat_model():
    model = ThreatModel(
        PROJECT_ROOT / "configs"
    )

    assert len(model.assets) >= 4
    assert len(model.trust_boundaries) >= 4
    assert len(model.threats) >= 4


def test_tool_abuse_threat():
    model = ThreatModel(
        PROJECT_ROOT / "configs"
    )

    threat = model.get_threat("T003")

    assert threat["category"] == "tool_abuse"
    assert threat["severity"] == "high"