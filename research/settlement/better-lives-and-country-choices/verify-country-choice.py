"""Check the constructed outcome bounds and the revised programme choice."""

from dataclasses import dataclass

ELIGIBLE = 20
CASH_LIMIT, PAID_LIMIT = 6, 4


@dataclass(frozen=True)
class Offer:
    cash: int
    paid_blocks: int
    timely: int
    missing: int
    rights_covered: bool

    def bounds(self):
        assert 0 <= self.timely <= self.timely + self.missing <= ELIGIBLE
        return self.timely, self.timely + self.missing

    def fits(self, added_cash=0, added_blocks=0):
        return (
            self.rights_covered
            and self.cash + added_cash <= CASH_LIMIT
            and self.paid_blocks + added_blocks <= PAID_LIMIT
        )


repair = Offer(6, 4, 16, 2, True)
plural = Offer(6, 4, 17, 2, True)
direct = Offer(6, 4, 16, 1, True)
mutual = Offer(5, 4, 16, 3, False)
assert [offer.bounds() for offer in (repair, plural, direct, mutual)] == [
    (16, 18), (17, 19), (16, 17), (16, 19)
]
assert plural.bounds()[0] <= repair.bounds()[1]
assert plural.bounds()[0] <= direct.bounds()[1]
assert repair.fits() and plural.fits() and direct.fits()
assert not mutual.fits()
assert not plural.fits(added_cash=1, added_blocks=1)
assert not direct.fits(added_cash=1)  # Additional binding carryover needs a separate source.


def selected_later(direct_authorized, carryover_in_allocation, repair_qualified):
    if direct_authorized and carryover_in_allocation and direct.fits():
        return "D"
    return "R" if repair_qualified and repair.fits() else "uncovered"


assert selected_later(True, True, True) == "D"
assert selected_later(False, True, True) == "R"
assert selected_later(True, False, True) == "R"
assert selected_later(False, True, False) == "uncovered"
print("Missing-outcome bounds, protected coverage and the two-budget disposition verified.")
