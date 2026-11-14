"""Check the constructed reserve and receiving comparison."""


def protected_receipt(
    first_release: int,
    first_received: int,
    *,
    later_hold: int = 0,
    cash: int = 10,
    later_delivery_capacity: int = 6,
    activate_later: bool = True,
) -> tuple[int, int]:
    assert 0 <= first_received <= first_release <= min(6, cash)
    remaining_usable = 10 - first_release - later_hold
    assert remaining_usable >= 0
    later_received = (
        min(6, remaining_usable, later_delivery_capacity, cash - first_release)
        if activate_later
        else 0
    )
    return 2 + first_received, 1 + later_received


if __name__ == "__main__":
    assert protected_receipt(0, 0, activate_later=False) == (2, 1)
    assert protected_receipt(6, 4) == (6, 5)
    assert protected_receipt(4, 4) == (6, 7)
    assert protected_receipt(4, 4, later_hold=2) == (6, 5)
    assert protected_receipt(4, 4, cash=8) == (6, 5)
    assert protected_receipt(4, 4, later_delivery_capacity=4) == (6, 5)
    print("Reserve release, usable carryover and actual receiving reconcile by window.")
