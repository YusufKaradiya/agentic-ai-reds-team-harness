import time
from datetime import datetime, timezone
from uuid import uuid4

from core.attack_loader import AttackLoader
from core.audit_logger import AuditLogger
from core.policy_engine import PolicyEngine
from core.tool_registry import ToolRegistry
from database.database import Database
from tools.mock_tools import MockToolExecutor


class AgentController:

    def __init__(
        self,
        config_root: str = "configs",
        database_path: str = "data/redteam.db",
    ):

        self.database = Database(
            database_path
        )

        self.attack_loader = AttackLoader(
            config_root
        )

        self.tool_registry = ToolRegistry(
            config_root
        )

        self.policy_engine = PolicyEngine(
            config_root
        )

        self.audit_logger = AuditLogger(
            self.database
        )

        self.tool_executor = (
            MockToolExecutor()
        )

    def run_attack(
        self,
        attack_id: str,
        tool_id: str | None = None,
    ) -> dict:

        start_time = time.perf_counter()

        run_id = str(uuid4())

        attack = self.attack_loader.get_attack(
            attack_id
        )

        self.audit_logger.log(
            run_id=run_id,
            event_type="run_started",
            component="agent_controller",
            decision="started",
            reason="Attack execution started.",
            metadata={
                "attack_id": attack.id,
                "category": attack.category.value,
            },
        )

        input_decision = (
            self.policy_engine.evaluate_input(
                attack.payload
            )
        )

        self.audit_logger.log(
            run_id=run_id,
            event_type="security_decision",
            component=input_decision.component,
            decision=input_decision.decision,
            reason=input_decision.reason,
            metadata={
                "risk_score":
                    input_decision.risk_score
            },
        )

        tool_called = False
        data_leakage = False
        attack_success = False

        final_decision = input_decision.decision

        if input_decision.decision == "block":

            status = "blocked"

        else:

            status = "allowed"

            if tool_id:

                tool = self.tool_registry.get_tool(
                    tool_id
                )

                tool_decision = (
                    self.policy_engine
                    .authorize_tool(tool)
                )

                self.audit_logger.log(
                    run_id=run_id,
                    event_type="tool_authorization",
                    component=tool_decision.component,
                    decision=tool_decision.decision,
                    reason=tool_decision.reason,
                    metadata={
                        "tool_id": tool.id,
                        "risk_level":
                            tool.risk_level.value,
                    },
                )

                if tool_decision.decision == "allow":

                    tool_result = (
                        self.tool_executor.execute(
                            tool.id
                        )
                    )

                    tool_called = True

                    self.audit_logger.log(
                        run_id=run_id,
                        event_type="tool_execution",
                        component="mock_tool_executor",
                        decision="executed",
                        reason=(
                            "Mock tool executed."
                        ),
                        metadata={
                            "tool_id": tool.id,
                            "success":
                                tool_result.success,
                        },
                    )

                else:

                    final_decision = (
                        tool_decision.decision
                    )

                    status = "tool_blocked"

        latency_ms = (
            time.perf_counter() -
            start_time
        ) * 1000

        expected = attack.expected_behavior

        if (
            expected.decision == final_decision
            and expected.leakage == data_leakage
        ):
            attack_success = False
        else:
            attack_success = True

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        self.database.insert_run(
            run_id=run_id,
            attack_id=attack.id,
            attack_name=attack.name,
            category=attack.category.value,
            severity=attack.severity.value,
            status=status,
            decision=final_decision,
            attack_success=attack_success,
            data_leakage=data_leakage,
            tool_called=tool_called,
            latency_ms=latency_ms,
            created_at=timestamp,
        )

        self.audit_logger.log(
            run_id=run_id,
            event_type="run_completed",
            component="agent_controller",
            decision=final_decision,
            reason="Attack execution completed.",
            metadata={
                "status": status,
                "latency_ms": latency_ms,
            },
        )

        return {
            "run_id": run_id,
            "attack_id": attack.id,
            "attack_name": attack.name,
            "category": attack.category.value,
            "severity": attack.severity.value,
            "status": status,
            "decision": final_decision,
            "risk_score": input_decision.risk_score,
            "attack_success": attack_success,
            "data_leakage": data_leakage,
            "tool_called": tool_called,
            "latency_ms": round(
                latency_ms,
                2
            ),
        }