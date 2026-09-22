from core.config_loader import ConfigLoader
from core.contracts import (
    AttackDefinition,
    ToolDefinition,
)


def test_attack_contract():
    loader = ConfigLoader("configs")

    data = loader.load_attack("PI-001.yaml")

    attack = AttackDefinition.model_validate(data)

    assert attack.id == "PI-001"
    assert attack.category.value == "direct_injection"
    assert attack.severity.value == "high"


def test_tool_contract():
    loader = ConfigLoader("configs")

    data = loader.load_tools()

    tools = [
        ToolDefinition.model_validate(item)
        for item in data["tools"]
    ]

    assert len(tools) == 4

    send_email = next(
        tool
        for tool in tools
        if tool.id == "send_email"
    )

    assert send_email.requires_approval is True