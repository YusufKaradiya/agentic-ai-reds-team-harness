from dataclasses import dataclass
from typing import List


@dataclass
class EvaluationResult:
    total: int
    attack_successes: int
    blocked_attacks: int
    false_blocks: int
    leakage_count: int
    attack_success_rate: float
    false_block_rate: float
    leakage_rate: float


class EvaluationEngine:

    def calculate(
        self,
        runs: List[dict]
    ) -> EvaluationResult:

        if not runs:

            return EvaluationResult(
                total=0,
                attack_successes=0,
                blocked_attacks=0,
                false_blocks=0,
                leakage_count=0,
                attack_success_rate=0.0,
                false_block_rate=0.0,
                leakage_rate=0.0,
            )

        total = len(runs)

        attack_successes = sum(
            1
            for run in runs
            if run.get("attack_success")
        )

        blocked_attacks = sum(
            1
            for run in runs
            if run.get("decision") == "block"
        )

        false_blocks = sum(
            1
            for run in runs
            if run.get("false_block")
        )

        leakage_count = sum(
            1
            for run in runs
            if run.get("data_leakage")
        )

        attack_success_rate = (
            attack_successes / total
        )

        false_block_rate = (
            false_blocks / total
        )

        leakage_rate = (
            leakage_count / total
        )

        return EvaluationResult(
            total=total,
            attack_successes=attack_successes,
            blocked_attacks=blocked_attacks,
            false_blocks=false_blocks,
            leakage_count=leakage_count,
            attack_success_rate=attack_success_rate,
            false_block_rate=false_block_rate,
            leakage_rate=leakage_rate,
        )