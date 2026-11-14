"""Reproduce the stated role constraints in the two-window comparison."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Hours:
    reconciliation: int
    independent_review: int

    def __add__(self, other):
        return Hours(self.reconciliation + other.reconciliation,
                     self.independent_review + other.independent_review)

    def shortfall(self, available):
        return Hours(max(0, self.reconciliation - available.reconciliation),
                     max(0, self.independent_review - available.independent_review))


def main():
    available = Hours(10, 2)
    ordinary = Hours(4, 1)
    benefit = Hours(5, 1)
    mobility = Hours(4, 1)
    no_shortfall = Hours(0, 0)

    assert (ordinary + benefit).shortfall(available) == no_shortfall
    assert (ordinary + mobility).shortfall(available) == no_shortfall
    assert (ordinary + benefit + mobility).shortfall(available) == Hours(3, 1)
    assert (ordinary + benefit + mobility).shortfall(Hours(10, 3)) == Hours(3, 0)

    benefit_handback = Hours(2, 1)
    second_window = ordinary + benefit_handback + mobility
    assert second_window == Hours(10, 3)
    assert second_window.shortfall(available) == Hours(0, 1)
    assert second_window.shortfall(Hours(10, 3)) == no_shortfall
    shared_candidates = 6
    unique_per_unit = 2
    origin_commitments = 4
    assert shared_candidates + 2 * unique_per_unit == 10
    shared_available = shared_candidates - origin_commitments
    assert shared_available + 2 * unique_per_unit == 6
    assert shared_available + unique_per_unit == 4
    print("Transition capacity: concurrent shortfall and independent handback passed.")


if __name__ == "__main__":
    main()
