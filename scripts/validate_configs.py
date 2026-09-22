import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.config_loader import ConfigLoader
from core.contracts import (
    AttackDefinition,
    ToolDefinition,
    ModelConfig,
    EvaluationConfig,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

loader = ConfigLoader(
    PROJECT_ROOT / "configs"
)


def validate_attacks():
    attack_dir = PROJECT_ROOT / "configs" / "attacks"

    for path in sorted(attack_dir.glob("[A-Z][A-Z]-*.yaml")):
        data = loader.load_attack(path.name)
        attack = AttackDefinition.model_validate(data)

        print(
            f"[OK] Attack: "
            f"{attack.id} - {attack.name}"
        )


def validate_tools():
    data = loader.load_tools()

    for item in data["tools"]:
        tool = ToolDefinition.model_validate(item)

        print(
            f"[OK] Tool: "
            f"{tool.id} - {tool.name}"
        )


def validate_model():
    data = loader.load_model()

    ollama = data["ollama"]

    model = ModelConfig(
        provider=data["provider"],
        base_url=ollama["base_url"],
        model=ollama["model"],
        temperature=ollama["temperature"],
        timeout_seconds=ollama["timeout_seconds"],
    )

    print(
        f"[OK] Model: "
        f"{model.provider}/{model.model}"
    )


def validate_evaluation():
    data = loader.load_evaluation()
    experiment = data["experiment"]

    config = EvaluationConfig(
        baseline_enabled=experiment["baseline_enabled"],
        defended_enabled=experiment["defended_enabled"],
        repetitions=experiment["repetitions"],
        random_seed=experiment["random_seed"],
    )

    print(
        f"[OK] Evaluation repetitions: "
        f"{config.repetitions}"
    )


def main():
    print("=" * 60)
    print("CONFIGURATION VALIDATION")
    print("=" * 60)

    validate_attacks()
    validate_tools()
    validate_model()
    validate_evaluation()

    print("=" * 60)
    print("ALL CONFIGURATIONS VALID")
    print("=" * 60)


if __name__ == "__main__":
    main()