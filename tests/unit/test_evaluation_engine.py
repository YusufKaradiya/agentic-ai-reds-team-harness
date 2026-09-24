from core.evaluation_engine import EvaluationEngine


def test_evaluation_metrics():

    engine = EvaluationEngine()

    runs = [
        {
            "attack_success": True,
            "decision": "allow",
            "false_block": False,
            "data_leakage": True,
        },
        {
            "attack_success": False,
            "decision": "block",
            "false_block": False,
            "data_leakage": False,
        },
        {
            "attack_success": False,
            "decision": "block",
            "false_block": True,
            "data_leakage": False,
        },
    ]

    result = engine.calculate(runs)

    assert result.total == 3
    assert result.attack_successes == 1
    assert result.leakage_count == 1
    assert result.false_blocks == 1