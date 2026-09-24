from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from core.detection_engine import DetectionEngine


@dataclass
class SecurityDecision:
    decision: str
    reason: str
    risk_score: float
    component: str
    detection_count: int = 0
    detection_ids: Optional[list] = None


class PolicyEngine:

    def __init__(
        self,
        detection_engine: DetectionEngine | str | Path | None = None
    ):
        if detection_engine is None:
            self.detection_engine = DetectionEngine()
        elif isinstance(detection_engine, (str, Path)):
            self.detection_engine = DetectionEngine(detection_engine)
        else:
            self.detection_engine = detection_engine

    def evaluate_input(
        self,
        text: str,
        defense_enabled: bool = True
    ) -> SecurityDecision:

        if not defense_enabled:

            return SecurityDecision(
                decision="allow",
                reason="Defense disabled: baseline mode",
                risk_score=0.0,
                component="input_policy",
                detection_count=0,
                detection_ids=[],
            )

        matches = self.detection_engine.scan_input(text)

        if not matches:

            return SecurityDecision(
                decision="allow",
                reason="No suspicious pattern detected",
                risk_score=0.0,
                component="input_policy",
                detection_count=0,
                detection_ids=[],
            )

        risk_score = self.detection_engine.get_risk_score(matches)

        if risk_score >= 0.75:
            decision = "block"
        else:
            decision = "review"

        return SecurityDecision(
            decision=decision,
            reason="Suspicious input pattern detected",
            risk_score=risk_score,
            component="input_policy",
            detection_count=len(matches),
            detection_ids=[
                match.pattern_id
                for match in matches
            ],
        )

    def evaluate_retrieved_content(
        self,
        text: str,
        defense_enabled: bool = True
    ) -> SecurityDecision:

        if not defense_enabled:

            return SecurityDecision(
                decision="allow",
                reason="Defense disabled: baseline mode",
                risk_score=0.0,
                component="retrieval_policy",
            )

        matches = self.detection_engine.scan_input(text)

        if not matches:

            return SecurityDecision(
                decision="allow",
                reason="Retrieved content appears safe",
                risk_score=0.0,
                component="retrieval_policy",
            )

        risk_score = self.detection_engine.get_risk_score(matches)

        return SecurityDecision(
            decision="quarantine",
            reason="Suspicious instructions detected in retrieved content",
            risk_score=risk_score,
            component="retrieval_policy",
            detection_count=len(matches),
            detection_ids=[
                match.pattern_id
                for match in matches
            ],
        )

    def evaluate_output(
        self,
        text: str,
        defense_enabled: bool = True
    ) -> SecurityDecision:

        if not defense_enabled:

            return SecurityDecision(
                decision="allow",
                reason="Output defense disabled",
                risk_score=0.0,
                component="output_policy",
            )

        matches = self.detection_engine.scan_output(text)

        if not matches:

            return SecurityDecision(
                decision="allow",
                reason="No sensitive data detected",
                risk_score=0.0,
                component="output_policy",
            )

        risk_score = self.detection_engine.get_risk_score(matches)

        return SecurityDecision(
            decision="block",
            reason="Potential sensitive data detected in output",
            risk_score=risk_score,
            component="output_policy",
            detection_count=len(matches),
            detection_ids=[
                match.pattern_id
                for match in matches
            ],
        )

    def authorize_tool(
        self,
        tool,
        defense_enabled: bool = True,
        user_approved: bool = False
    ) -> SecurityDecision:

        if not tool.enabled:

            return SecurityDecision(
                decision="deny",
                reason="Tool is disabled",
                risk_score=1.0,
                component="tool_authorization",
            )

        if not defense_enabled:

            return SecurityDecision(
                decision="allow",
                reason="Baseline mode: tool policy disabled",
                risk_score=0.0,
                component="tool_authorization",
            )

        risk = tool.risk_level.value

        if risk == "low":

            return SecurityDecision(
                decision="allow",
                reason="Low-risk tool",
                risk_score=0.10,
                component="tool_authorization",
            )

        if risk == "medium":

            if tool.requires_authentication:
                return SecurityDecision(
                    decision="authenticated",
                    reason="Authentication required",
                    risk_score=0.40,
                    component="tool_authorization",
                )

            return SecurityDecision(
                decision="allow",
                reason="Medium-risk tool allowed",
                risk_score=0.40,
                component="tool_authorization",
            )

        if risk == "high":

            if user_approved:
                return SecurityDecision(
                    decision="allow",
                    reason="High-risk tool approved by user",
                    risk_score=0.75,
                    component="tool_authorization",
                )

            return SecurityDecision(
                decision="approval_required",
                reason="Explicit approval required",
                risk_score=0.75,
                component="tool_authorization",
            )

        return SecurityDecision(
            decision="deny",
            reason="Critical-risk tool denied",
            risk_score=1.0,
            component="tool_authorization",
        )