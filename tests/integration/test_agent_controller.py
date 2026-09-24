from core.agent_controller import AgentController


def test_defense_blocks_injection():

    controller = AgentController()

    result = controller.run_attack(
        attack_id="PI-001",
        defense_enabled=True
    )

    assert result["decision"] == "block"

    assert result["attack_success"] is False

    assert result["tool_called"] is False


def test_baseline_allows_injection():

    controller = AgentController()

    result = controller.run_attack(
        attack_id="PI-001",
        defense_enabled=False
    )

    assert result["mode"] == "baseline"

    assert result["decision"] == "allow"