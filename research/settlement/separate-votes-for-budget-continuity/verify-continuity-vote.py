"""Check the constructed independent vote, cash and deadline gates."""


def can_bind(yes_votes: int, cash: int, cost: int, acceptance_day: int) -> bool:
    majority = 100 // 2 + 1
    return yes_votes >= majority and cash >= cost and acceptance_day <= 85


if __name__ == "__main__":
    assert not can_bind(44, 5, 4, 85)
    assert can_bind(55, 5, 4, 85)
    assert not can_bind(55, 5, 4 + 3, 85)
    assert not can_bind(55, 5, 4, 86)
    assert 5 - 4 == 1
    assert 3 - (5 - 4) == 2
    print("The separate majority funds only the exact timely continuation.")
