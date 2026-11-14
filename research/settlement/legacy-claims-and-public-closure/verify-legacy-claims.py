"""Check the constructed closure comparison, in cash units."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Outcome:
    received: int
    due_unpaid: int
    restricted_balance: int


def settle(
    opening_cash: int,
    release: int,
    casework: int,
    verified_claim: int,
    can_deliver: bool = True,
) -> Outcome:
    first_window_payments = 6
    available = opening_cash - first_window_payments - release - casework
    assert available >= 0
    received = min(available, verified_claim) if can_deliver else 0
    return Outcome(received, verified_claim - received, available - received)


if __name__ == "__main__":
    assert settle(12, 0, 3, 3) == Outcome(3, 0, 0)
    assert settle(12, 4, 2, 3) == Outcome(0, 3, 0)
    assert settle(12, 0, 2, 3) == Outcome(3, 0, 1)
    assert settle(12, 0, 2, 5) == Outcome(4, 1, 0)
    assert settle(12, 0, 2, 3, can_deliver=False) == Outcome(0, 3, 4)
    print("Closed-scheme cash, later claims, and independent delivery gates passed.")
