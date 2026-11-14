"""Reproduce the constructed two-budget renewal choices."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Work:
    cash: int
    shared_weeks: int


def totals(*work):
    return Work(sum(item.cash for item in work), sum(item.shared_weeks for item in work))


def fits(work, cash_limit, week_limit=6):
    return work.cash <= cash_limit and work.shared_weeks <= week_limit


binding = Work(20, 0)
water = Work(55, 4)
school = Work(30, 3)
school_bridge = Work(10, 0)
pump = Work(12, 1)
expansion_start = Work(20, 2)
expansion_continuation = Work(50, 2)
preparation = Work(5, 0)
independent_school = Work(42, 0)

early_expansion = totals(binding, water, school_bridge, expansion_start)
late_expansion = totals(binding, school, pump, expansion_continuation)
protected_first = totals(binding, water, school_bridge, preparation)
protected_second = totals(binding, school, pump)
both_with_shared_crew = totals(binding, water, school)
both_with_separate_crew = totals(binding, water, independent_school)

assert early_expansion == Work(105, 6) and fits(early_expansion, 120)
assert late_expansion == Work(112, 6) and not fits(late_expansion, 100)
# A lawful transfer has to come out of the first-year envelope.
carry_forward = 12
assert fits(early_expansion, 120 - carry_forward)
assert fits(late_expansion, 100 + carry_forward)
assert not fits(late_expansion, 100 + carry_forward - 1)
assert protected_first == Work(90, 4) and fits(protected_first, 120)
assert protected_second == Work(62, 4) and fits(protected_second, 100)
assert both_with_shared_crew == Work(105, 7) and not fits(both_with_shared_crew, 120)
assert both_with_separate_crew == Work(117, 4) and fits(both_with_separate_crew, 120)
assert totals(binding, pump) == Work(32, 1)
print("Renewal capacity: binding cash, later shortfall, shared crew and paid alternatives passed.")
