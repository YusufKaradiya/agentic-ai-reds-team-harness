from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class AttackCategory(str, Enum):
    DIRECT_INJECTION = "direct_injection"
    INDIRECT_INJECTION = "indirect_injection"
    TOOL_ABUSE = "tool_abuse"
    DATA_EXFILTRATION = "data_exfiltration"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ExpectedBehavior(BaseModel):
    decision: str
    leakage: bool
    tool_call: bool


class AttackDefinition(BaseModel):
    id: str
    name: str
    category: AttackCategory
    severity: Severity
    version: str

    description: str
    payload: str
    target: str

    expected_behavior: ExpectedBehavior

    tags: List[str] = Field(default_factory=list)


class ToolDefinition(BaseModel):
    id: str
    name: str
    risk_level: Severity
    permission: str

    requires_authentication: bool
    requires_approval: bool
    enabled: bool


class PolicyRule(BaseModel):
    action: str


class ModelConfig(BaseModel):
    provider: str

    base_url: str
    model: str
    temperature: float = 0.0
    timeout_seconds: int = 60


class EvaluationConfig(BaseModel):
    baseline_enabled: bool
    defended_enabled: bool
    repetitions: int
    random_seed: int