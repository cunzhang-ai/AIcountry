"""Evaluate the authored paired comparison at the original useful cutoffs."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Receipt:
    hour: int
    source: str
    amount: int = 0
    usable: bool = True


DEADLINES = {
    "benefit": 2,
    "opposition": 3,
    "care": 3,
    "executed_review": 4,
    "handover": 6,
    "career_continuity": 6,
    "next_care": 8,
}
BUDGETS = {"benefit": 2, "care": 4, "institutions": 4}
SOURCES = {
    "benefit": ("benefit", 2),
    "care": ("care", 2),
    "next_care": ("care", 2),
    "opposition": ("institutions", 1),
    "executed_review": ("institutions", 2),
    "handover": ("institutions", 1),
    "career_continuity": ("institutions", 1),
}

REPAIR = {
    "benefit": Receipt(5, "benefit", 2),
    "opposition": Receipt(3, "institutions", 1),
    "care": Receipt(5, "care", 2),
    "executed_review": Receipt(5, "institutions", 2),
    "handover": Receipt(7, "institutions", 1),
    "next_care": Receipt(8, "care", 2),
}
INDEPENDENT = {
    "benefit": Receipt(2, "benefit", 2),
    "opposition": Receipt(3, "institutions", 1),
    "care": Receipt(3, "care", 2),
    "executed_review": Receipt(4, "institutions", 2),
    "handover": Receipt(5, "institutions", 1),
    "next_care": Receipt(8, "care", 2),
}


def assess(receipts, unresolved_care=0, appointment_effective=True):
    """Report failed receipt and an unfunded proposal as distinct findings."""
    spending = dict.fromkeys(BUDGETS, 0)
    spending["care"] = unresolved_care
    expected = set(DEADLINES) - {"career_continuity" if appointment_effective else "handover"}
    late_or_unusable = expected.symmetric_difference(receipts)
    for duty, receipt in receipts.items():
        cutoff = DEADLINES[duty]
        source, required = SOURCES[duty]
        spending[receipt.source] += receipt.amount
        if (receipt.source != source or receipt.amount != required
                or not receipt.usable or receipt.hour > cutoff):
            late_or_unusable.add(duty)
    shortfall = {
        source: amount - BUDGETS[source]
        for source, amount in spending.items()
        if amount > BUDGETS[source]
    }
    return late_or_unusable, shortfall


def select(repair, independent):
    if assess(repair) == (set(), {}):
        return "R"
    if assess(independent) == (set(), {}):
        return "I"
    return "hold dependent moves"


assert assess(REPAIR) == ({"benefit", "care", "executed_review", "handover"}, {})
assert assess(INDEPENDENT) == (set(), {})
assert assess(INDEPENDENT, unresolved_care=2) == (set(), {"care": 2})
assert select(REPAIR, INDEPENDENT) == "I"
assert select(INDEPENDENT, INDEPENDENT) == "R"

late = dict(INDEPENDENT, next_care=replace(INDEPENDENT["next_care"], hour=9))
assert assess(late) == ({"next_care"}, {})
assert select(REPAIR, late) == "hold dependent moves"

shared = dict(INDEPENDENT, executed_review=replace(INDEPENDENT["executed_review"], usable=False))
assert assess(shared) == ({"executed_review"}, {})
central = dict(shared, handover=replace(shared["handover"], usable=False))
assert assess(central) == ({"executed_review", "handover"}, {})

diversion = dict(INDEPENDENT, next_care=Receipt(8, "benefit", 2))
assert assess(diversion) == ({"next_care"}, {"benefit": 2})

no_receiving_crew = dict(INDEPENDENT, next_care=Receipt(8, "care", 2, usable=False))
assert assess(no_receiving_crew) == ({"next_care"}, {})

# Before effective appointment, continue only the already lawful work.
unresolved = dict(INDEPENDENT)
del unresolved["handover"]
unresolved["career_continuity"] = Receipt(5, "institutions", 1)
assert assess(unresolved, appointment_effective=False) == (set(), {})
no_career_act = dict(unresolved, career_continuity=Receipt(5, "institutions", 1, usable=False))
assert assess(no_career_act, appointment_effective=False) == ({"career_continuity"}, {})

formation_repeat_trigger = 30
repeat_poll_close = formation_repeat_trigger + 90
bridge_last_day = 90
uncovered_bridge_days = range(bridge_last_day + 1, repeat_poll_close + 1)
assert (uncovered_bridge_days.start, uncovered_bridge_days.stop - 1) == (91, 120)
assert len(uncovered_bridge_days) == 30

print("The opening comparison selects independent execution only while both calls and protected control qualify.")
