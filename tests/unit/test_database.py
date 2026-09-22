from database.database import Database


def test_database_creates_tables(
    tmp_path
):

    db_path = tmp_path / "test.db"

    database = Database(
        str(db_path)
    )

    database.insert_run(
        run_id="test-run",
        attack_id="PI-001",
        attack_name="Test Attack",
        category="direct_injection",
        severity="high",
        status="blocked",
        decision="block",
        attack_success=False,
        data_leakage=False,
        tool_called=False,
        latency_ms=10.0,
        created_at="2026-01-01T00:00:00Z",
    )

    runs = database.get_runs()

    assert len(runs) == 1
    assert runs[0]["attack_id"] == "PI-001"