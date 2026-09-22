from dataclasses import dataclass
from pathlib import Path
import re

from core.config_loader import ConfigLoader
from core.contracts import ToolDefinition


@dataclass
class SecurityDecision:
    decision: str
    reason: str
    risk_score: float
    component: str


class PolicyEngine:
    """
    Configuration-driven security policy engine.

    The engine performs lightweight baseline checks.
    More advanced ML/LLM-based detection will be added
    in later days.
    """

    def __init__(
        self,
        config_root: str = "configs"
    ):
        self.loader = ConfigLoader(
            Path(config_root)
        )

        self.policies = (
            self.loader
            .load_policies()
            .get("policies", {})
        )

        self.injection_patterns = [
            r"ignore previous instructions",
            r"ignore all previous instructions",
            r"reveal system prompt",
            r"print the system prompt",
            r"show hidden instructions",
            r"bypass security",
            r"disable security",
            r"reveal the secret",
            r"provide the api token",
            r"extract the secret",
        ]

    def evaluate_input(
        self,
        text: str
    ) -> SecurityDecision:

        normalized = text.lower()

        matched_patterns = []

        for pattern in self.injection_patterns:

            if re.search(
                pattern,
                normalized
            ):
                matched_patterns.append(pattern)

        if matched_patterns:

            return SecurityDecision(
                decision="block",
                reason=(
                    "Potential prompt injection "
                    "pattern detected."
                ),
                risk_score=min(
                    0.95,
                    0.60 + (
                        0.05 *
                        len(matched_patterns)
                    )
                ),
                component="input_defense",
            )

        return SecurityDecision(
            decision="allow",
            reason="No baseline injection pattern detected.",
            risk_score=0.05,
            component="input_defense",
        )

    def evaluate_retrieved_content(
        self,
        text: str
    ) -> SecurityDecision:

        decision = self.evaluate_input(text)

        if decision.decision == "block":

            return SecurityDecision(
                decision="quarantine",
                reason=(
                    "Potential malicious instruction "
                    "detected in retrieved content."
                ),
                risk_score=decision.risk_score,
                component="retrieved_content_scanner",
            )

        return SecurityDecision(
            decision="allow",
            reason="Retrieved content passed baseline checks.",
            risk_score=0.05,
            component="retrieved_content_scanner",
        )

    def authorize_tool(
        self,
        tool: ToolDefinition,
    ) -> SecurityDecision:

        if not tool.enabled:

            return SecurityDecision(
                decision="deny",
                reason="Tool is disabled.",
                risk_score=1.0,
                component="tool_sandbox",
            )

        risk = tool.risk_level.value

        if risk == "low":

            return SecurityDecision(
                decision="allow",
                reason="Low-risk tool allowed.",
                risk_score=0.10,
                component="tool_sandbox",
            )

        if risk == "medium":

            if tool.requires_authentication:

                return SecurityDecision(
                    decision="authenticated",
                    reason=(
                        "Tool requires authentication."
                    ),
                    risk_score=0.40,
                    component="tool_sandbox",
                )

            return SecurityDecision(
                decision="allow",
                reason="Medium-risk tool allowed.",
                risk_score=0.35,
                component="tool_sandbox",
            )

        if risk == "high":

            if tool.requires_approval:

                return SecurityDecision(
                    decision="approval_required",
                    reason=(
                        "High-risk tool requires "
                        "explicit approval."
                    ),
                    risk_score=0.80,
                    component="tool_sandbox",
                )

        if risk == "critical":

            return SecurityDecision(
                decision="deny",
                reason=(
                    "Critical-risk tool is denied "
                    "by default."
                ),
                risk_score=1.0,
                component="tool_sandbox",
            )

        return SecurityDecision(
            decision="deny",
            reason="Unknown security state.",
            risk_score=1.0,
            component="tool_sandbox",
        )

    def evaluate_output(
        self,
        text: str
    ) -> SecurityDecision:

        sensitive_patterns = [
            r"sk-[a-zA-Z0-9]{10,}",
            r"api[_ -]?key",
            r"secret[_ -]?token",
            r"internal[_ -]?secret",
        ]

        for pattern in sensitive_patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):

                return SecurityDecision(
                    decision="block",
                    reason=(
                        "Potential sensitive data "
                        "detected in output."
                    ),
                    risk_score=0.95,
                    component="output_security",
                )

        return SecurityDecision(
            decision="allow",
            reason="No baseline sensitive data pattern detected.",
            risk_score=0.05,
            component="output_security",
        )