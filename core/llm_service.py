from core.ollama_client import OllamaClient


class LLMService:

    def __init__(self, config_path="configs/attacks/model.yaml"):

        self.client = OllamaClient(config_path)

    def available(self):

        return self.client.is_available()

    def generate(
        self,
        prompt: str
    ):

        return self.client.generate(
            prompt
        )