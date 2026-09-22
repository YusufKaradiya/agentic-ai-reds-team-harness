from pathlib import Path

from core.config_loader import ConfigLoader
from core.contracts import AttackDefinition


class AttackLoader:
    """
    Loads attack definitions from YAML configuration.
    """

    def __init__(self, config_root: str = "configs"):
        self.config_root = Path(config_root)

        self.loader = ConfigLoader(
            self.config_root
        )

    def list_attacks(self) -> list[AttackDefinition]:
        attack_directory = (
            self.config_root / "attacks"
        )

        attacks = []

        for path in sorted(
            attack_directory.glob("[A-Z][A-Z]-*.yaml")
        ):
            data = self.loader.load_attack(
                path.name
            )

            attack = AttackDefinition.model_validate(
                data
            )

            attacks.append(attack)

        return attacks

    def get_attack(
        self,
        attack_id: str
    ) -> AttackDefinition:

        attacks = self.list_attacks()

        for attack in attacks:
            if attack.id == attack_id:
                return attack

        raise KeyError(
            f"Attack not found: {attack_id}"
        )