from core.agent_controller import AgentController


def test_direct_injection_workflow(
    tmp_path
):

    database_path = (
        tmp_path / "integration.db"
    )

    controller = AgentController(
        config_root="configs",
        database_path=str(database_path),
    )

    result = controller.run_attack(
        attack_id="PI-001"
    )

    assert result["decision"] == "block"

    assert result["tool_called"] is False

    assert result["data_leakage"] is False

    runs = controller.database.get_runs()

    assert len(runs) == 1

    assert runs[0]["attack_id"] == "PI-001"