from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    APP_ENV = os.getenv("APP_ENV", "development")

    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "llama3"
    )

    VECTOR_DB_TYPE = os.getenv(
        "VECTOR_DB_TYPE",
        "chroma"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///redteam.db"
    )

    MLFLOW_TRACKING_URI = os.getenv(
        "MLFLOW_TRACKING_URI",
        "http://localhost:5000"
    )

    OTEL_SERVICE_NAME = os.getenv(
        "OTEL_SERVICE_NAME",
        "agentic-ai-redteam"
    )


settings = Settings()