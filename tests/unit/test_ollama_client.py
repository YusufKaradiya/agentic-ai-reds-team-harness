from core.ollama_client import OllamaClient


def test_ollama_client_creation():

    client = OllamaClient()

    assert client.base_url
    assert client.model
def test_ollama_available():

    client = OllamaClient()

    if not client.is_available():
        return

    response = client.generate(
        "Say hello in one short sentence."
    )

    assert response.success is True
    assert len(response.text) > 0