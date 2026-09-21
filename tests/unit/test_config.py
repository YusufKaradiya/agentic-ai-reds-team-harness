from core.config import settings


def test_environment():
    assert settings.APP_ENV == "development"


def test_ollama_configuration():
    assert settings.OLLAMA_BASE_URL.startswith("http://")


def test_vector_database():
    assert settings.VECTOR_DB_TYPE in {
        "chroma",
        "qdrant"
    }