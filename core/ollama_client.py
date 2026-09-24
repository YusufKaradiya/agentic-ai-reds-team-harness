import time
from dataclasses import dataclass

import requests

from core.config_loader import ConfigLoader


@dataclass
class LLMResponse:
    text: str
    model: str
    latency_ms: float
    success: bool
    error: str | None = None


class OllamaClient:

    def __init__(
        self,
        config_path="configs/attacks/model.yaml"
    ):

        loader = ConfigLoader(
            config_path
        )

        self.config = loader.load()

        self.base_url = self.config.get(
            "base_url",
            "http://localhost:11434"
        )

        self.model = self.config.get(
            "model",
            "llama3.2:3b"
        )

        self.temperature = self.config.get(
            "temperature",
            0.0
        )

        self.timeout = self.config.get(
            "timeout_seconds",
            60
        )

        self.max_tokens = self.config.get(
            "max_tokens",
            512
        )

        self.system_prompt = self.config.get(
            "system_prompt",
            ""
        )

    def is_available(self) -> bool:

        try:

            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )

            return response.status_code == 200

        except requests.RequestException:

            return False

    def generate(
        self,
        prompt: str
    ) -> LLMResponse:

        start = time.perf_counter()

        try:

            payload = {
                "model": self.model,
                "prompt": prompt,
                "system": self.system_prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                },
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

            data = response.json()

            latency_ms = (
                time.perf_counter() - start
            ) * 1000

            return LLMResponse(
                text=data.get(
                    "response",
                    ""
                ),
                model=data.get(
                    "model",
                    self.model
                ),
                latency_ms=round(
                    latency_ms,
                    2
                ),
                success=True,
            )

        except requests.RequestException as exc:

            latency_ms = (
                time.perf_counter() - start
            ) * 1000

            return LLMResponse(
                text="",
                model=self.model,
                latency_ms=round(
                    latency_ms,
                    2
                ),
                success=False,
                error=str(exc),
            )