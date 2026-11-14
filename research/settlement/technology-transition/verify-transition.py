"""Reproduce the authored earnings trigger, separate ledgers and service test."""

from fractions import Fraction

GENERAL_RECEIPTS = 40 + 25 + 30
GENERAL_DUE = 100 + 5 + 3
EARNED_RECEIPTS = 16
EARNED_DUE = 20
BACKING = EARNED_DUE - EARNED_RECEIPTS
GENERAL_REQUIREMENT = GENERAL_DUE + BACKING


def trigger(reference, observed, threshold, involuntary_loss=True):
    return involuntary_loss and all(
        Fraction(before - after, before) >= threshold
        for before, after in zip(reference, observed, strict=True)
    )


def gap(*extra_receipts):
    return GENERAL_REQUIREMENT - (GENERAL_RECEIPTS + sum(extra_receipts))


if __name__ == "__main__":
    assert trigger((250, 250), (200, 200), Fraction(5, 100))
    assert trigger((40, 40), (32, 32), Fraction(10, 100))
    assert not trigger((40, 40), (32, 32), Fraction(10, 100), False)
    assert not trigger((40, 40), (32, 40), Fraction(10, 100))
    assert not trigger((250, 250), (250, 250), Fraction(5, 100))

    assert BACKING == 4
    assert gap() == GENERAL_DUE + EARNED_DUE - (GENERAL_RECEIPTS + EARNED_RECEIPTS) == 17
    assert gap(12, 5) == 0
    assert gap(10, 7) == 0
    assert gap(12) == 5
    assert gap(6) == 11
    assert gap(10, 7) + 6 == 6

    qualified_regular, qualified_backup, required = 8, 2, 10
    assert qualified_regular + qualified_backup == required
    assert qualified_regular < required
    print("General gap 17; restricted backing 4; both reconcile after consolidation.")
    print("Durable package passes at 17. A recurring 12 leaves 5. Collected levy 6 leaves 11.")
    print("Without the qualified alternate, two protected shifts are uncovered.")
