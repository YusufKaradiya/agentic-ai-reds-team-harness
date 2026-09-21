from pathlib import Path
import sys


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from core.config import settings


def main():
    print("=" * 50)
    print("AGENTIC AI RED-TEAM HARNESS")
    print("DAY 1 HEALTH CHECK")
    print("=" * 50)

    print(f"Environment       : {settings.APP_ENV}")
    print(f"Ollama URL        : {settings.OLLAMA_BASE_URL}")
    print(f"Ollama Model      : {settings.OLLAMA_MODEL}")
    print(f"Vector DB         : {settings.VECTOR_DB_TYPE}")
    print(f"Database          : {settings.DATABASE_URL}")
    print(f"MLflow            : {settings.MLFLOW_TRACKING_URI}")
    print(f"OTEL Service      : {settings.OTEL_SERVICE_NAME}")

    print("=" * 50)
    print("Configuration loaded successfully.")
    print("=" * 50)


if __name__ == "__main__":
    main()