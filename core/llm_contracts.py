from pydantic import BaseModel


class LLMGenerationRequest(BaseModel):

    prompt: str


class LLMGenerationResult(BaseModel):

    text: str
    model: str
    latency_ms: float
    success: bool
    error: str | None = None