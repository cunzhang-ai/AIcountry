"""Check the authored portfolio, preserving ordinary receipt and resources."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    funds: int
    reviews: int

    def plus(self, other):
        return Window(self.funds + other.funds, self.reviews + other.reviews)

    def covers(self, needed):
        return self.funds >= needed.funds and self.reviews >= needed.reviews


available = (Window(8, 4), Window(6, 4))
protected = (Window(4, 2), Window(4, 2))
ordinary_check = (Window(2, 1), Window(2, 1))
ai_check = (Window(2, 1), Window(1, 1))
communication = (Window(2, 1), Window(2, 2))


def totals(*supplements):
    windows = list(protected)
    for supplement in supplements:
        for index, requirement in enumerate(supplement):
            windows[index] = windows[index].plus(requirement)
    return tuple(windows)


def failures(requirements, capacity=available):
    return tuple(
        index + 1
        for index, (available_window, required_window) in enumerate(zip(capacity, requirements, strict=True))
        if not available_window.covers(required_window)
    )


assert not failures(totals(ordinary_check))
assert not failures(totals(ai_check))
assert not failures(totals(communication))
combined = totals(ai_check, communication)
assert combined == (Window(8, 4), Window(7, 5))
assert failures(combined) == (2,)
assert failures(combined, (Window(8, 4), Window(7, 4))) == (2,)
assert failures(combined, (Window(8, 4), Window(6, 5))) == (2,)
assert not failures(combined, (Window(8, 4), Window(7, 5)))

released_analyst_blocks = 3
due_reconciliation = 2
assert released_analyst_blocks - due_reconciliation == 1
qualified_inspection_appointments = 2
verified_defects_due = 3
assert verified_defects_due - qualified_inspection_appointments == 1
assert qualified_inspection_appointments + 1 == verified_defects_due

print("The combined offer fits the first window only. Ordinary receipt and independent review stay funded.")
