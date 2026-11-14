"""Reproduce the authored investment and later public-return terms."""

from dataclasses import dataclass, replace
from fractions import Fraction


@dataclass(frozen=True)
class Offer:
    name: str
    gross_cost: tuple[int, int]
    scope_accepted: bool = True
    independent_route: bool = True
    return_verifiable: bool = True
    exclusive: bool = False


def can_bind(offer, balance, approvals):
    return (
        offer.name in approvals
        and all(required <= cash for required, cash in zip(offer.gross_cost, balance))
        and offer.scope_accepted
        and offer.independent_route
        and not offer.exclusive
        and (offer.name != 'staged' or offer.return_verifiable)
    )


def assessed_return(distributable_cash):
    return min(Fraction(2), max(Fraction(0), Fraction(distributable_cash - 3, 2)))


def usable_receipt(received=Fraction(0), *, received_on=None, decision_day, available=False):
    if received_on is None or received_on > decision_day or not available:
        return Fraction(0)
    return received


def main():
    purchase = Offer('purchase', (3, 6))
    staged = Offer('staged', (3, 6))
    equity = Offer('equity', (4, 7))
    approvals = {'purchase', 'staged', 'equity'}

    assert can_bind(purchase, (3, 6), approvals)
    assert can_bind(staged, (3, 6), approvals)
    assert not can_bind(equity, (3, 6), approvals)
    assert not can_bind(staged, (3, 6), {'purchase'})
    assert not can_bind(replace(staged, return_verifiable=False), (3, 6), approvals)
    assert not can_bind(replace(staged, exclusive=True), (3, 6), approvals)
    assert not can_bind(replace(staged, independent_route=False), (3, 6), approvals)
    assert not can_bind(replace(staged, scope_accepted=False), (3, 6), approvals)

    assert assessed_return(2) == 0
    assert assessed_return(5) == 1
    assert 5 - assessed_return(5) == 4
    high = assessed_return(8)
    assert high == 2
    assert usable_receipt(decision_day=30) == 0
    early = 2 + usable_receipt(high, received_on=365, decision_day=30, available=True)
    assert not can_bind(staged, (early, 6), approvals)
    assert usable_receipt(high, received_on=365, decision_day=365) == 0
    assert usable_receipt(Fraction(1), received_on=365, decision_day=365, available=True) == 1
    assert usable_receipt(high, received_on=365, decision_day=365, available=True) == 2
    print('Public returns passed: gross award cost, accepted scope, capped claim and dated cash.')


if __name__ == '__main__':
    main()
