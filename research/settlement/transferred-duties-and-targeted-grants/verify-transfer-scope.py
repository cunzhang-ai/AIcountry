"""Verify preliminary figures and the constructed missing-case reconciliation."""

from decimal import Decimal


def main():
    assert Decimal("55.2") + Decimal("25.4") - 56 == Decimal("24.6")
    assert Decimal("15.3") + Decimal("18.0") == Decimal("33.3")
    sending = ("A", "B", "C", "D", "E")
    receiving = ("A", "B", "C", "D", "D")
    due = set(sending) | {"F"}
    missing = due - set(receiving)
    assert len(sending) == len(receiving) == 5 and missing == {"E", "F"}
    for distinct_alternates, outstanding in ((0, 2), (1, 1), (2, 0)):
        assert max(0, len(missing) - distinct_alternates) == outstanding
    print("Transfer: scoped funding arithmetic and the omitted duties passed.")


if __name__ == "__main__":
    main()
