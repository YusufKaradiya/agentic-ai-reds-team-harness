from core.attack_loader import AttackLoader


def test_attack_loader():

    loader = AttackLoader("configs")

    attacks = loader.list_attacks()

    assert len(attacks) >= 5


def test_get_attack():

    loader = AttackLoader("configs")

    attack = loader.get_attack("PI-001")

    assert attack.id == "PI-001"
    assert attack.target == "agent"