#!/usr/bin/env python3
"""Check the constructed case dispositions and staffing comparison."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Outcome:
    correct: int
    unsupported_adverse: int
    open: int


routine, contested, disputed = 20, 10, 4
total = routine + contested
initial_work = routine + 2 * contested
full_review = initial_work + disputed
ordinary_work = routine + 2 * contested
shared_summary = Outcome(total - disputed, disputed, 0)


def independently_reviewed(qualified_units: int) -> Outcome:
    assert qualified_units >= initial_work
    resolved_disagreements = min(disputed, qualified_units - initial_work)
    remaining = disputed - resolved_disagreements
    return Outcome(total - remaining, 0, remaining)


assert shared_summary == Outcome(26, 4, 0)
assert full_review == 44 and ordinary_work == 40
assert independently_reviewed(44) == Outcome(30, 0, 0)
assert independently_reviewed(40) == Outcome(26, 0, 4)
assert full_review - initial_work == 4
assert full_review - ordinary_work == 4

print("Shared summary: four unsupported adverse decisions; independent first view: 30 correct with 44 units.")
print("With 40 units: 26 correct and four open on the assisted route, or all 30 correct on the ordinary route.")
