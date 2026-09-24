from pathlib import Path

from core.config_loader import ConfigLoader
from core.contracts import AttackDefinition


class AttackLoader:

    def __init__(
        self,
        attack_directory="configs/attacks"
    ):

        attack_path = Path(attack_directory)
        attacks_subdirectory = attack_path / "attacks"

        self.attack_directory = (
            attacks_subdirectory
            if attacks_subdirectory.is_dir()
            else attack_path
        )

        self.attacks = {}

        self.load_attacks()

    def load_attacks(self):

        self.attacks = {}

        for file in sorted(
            self.attack_directory.glob("*-*.yaml")
        ):

            loader = ConfigLoader(
                str(file)
            )

            data = loader.load()

            if not data:
                continue

            attack = AttackDefinition.model_validate(
                data
            )

            self.attacks[
                attack.id
            ] = attack

    def list_attacks(self):

        return list(
            self.attacks.values()
        )

    def get_attack(self, attack_id):

        if attack_id not in self.attacks:

            raise ValueError(
                f"Unknown attack ID: {attack_id}"
            )

        return self.attacks[attack_id]