"""Check the constructed small-claim gates and household payment example."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MeritsGate:
    usable_service: bool
    fair_opportunity: bool
    proof_of_liability_and_amount: bool
    judicial_decision: bool

    @property
    def may_order(self):
        return all((
            self.usable_service,
            self.fair_opportunity,
            self.proof_of_liability_and_amount,
            self.judicial_decision,
        ))


@dataclass(frozen=True)
class Payment:
    receipt_id: str
    amount: int
    actually_received: bool


def account(principal, direct_cost, transfers):
    credited = {}
    for transfer in transfers:
        if not transfer.actually_received:
            continue
        assert transfer.amount > 0
        previous = credited.setdefault(transfer.receipt_id, transfer.amount)
        assert previous == transfer.amount
    received = sum(credited.values())
    assert received <= principal
    return received, principal - received, received - direct_cost


def main():
    basket = 100
    principal = 60
    assert principal <= 2 * basket
    assert 120 <= 2 * basket and 100 <= 2 * basket
    assert 120 + 100 > 2 * basket

    assert MeritsGate(True, True, True, True).may_order
    assert not MeritsGate(False, True, True, True).may_order
    assert not MeritsGate(True, False, True, True).may_order
    assert not MeritsGate(True, True, False, True).may_order
    assert not MeritsGate(True, True, True, False).may_order

    first = Payment("first", 20, True)
    pending = Payment("second", 40, False)
    second = Payment("second", 40, True)
    assert account(principal, 5, [first, first, pending]) == (20, 40, 15)
    assert account(principal, 5, [first, pending, second]) == (60, 0, 55)
    assert account(principal, 70, [first, second]) == (60, 0, -10)
    print("Small claims: scope, lawful hearing, unique receipt and net recovery passed.")


if __name__ == "__main__":
    main()
