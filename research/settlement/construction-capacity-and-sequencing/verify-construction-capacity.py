#!/usr/bin/env python3
"""Reproduce the two-window construction and inspection comparison."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Use:
    crew: int
    inspections: int
    public_cash: int


def combine(*uses: Use) -> Use:
    return Use(
        sum(use.crew for use in uses),
        sum(use.inspections for use in uses),
        sum(use.public_cash for use in uses),
    )


def shortages(use: Use, capacity: Use) -> Use:
    return Use(
        max(0, use.crew - capacity.crew),
        max(0, use.inspections - capacity.inspections),
        max(0, use.public_cash - capacity.public_cash),
    )


private_ordinary = Use(2, 1, 0)
first_base = combine(Use(6, 2, 8), private_ordinary)
second_base = combine(Use(5, 2, 8), private_ordinary)
first_capacity = Use(10, 4, 20)
second_capacity = Use(10, 4, 14)
housing = Use(2, 1, 5)
depot_early = Use(2, 1, 5)
depot_later = Use(2, 1, 6)
private_extra = Use(1, 1, 0)
no_shortage = Use(0, 0, 0)

assert shortages(combine(first_base, housing), first_capacity) == no_shortage
assert shortages(combine(first_base, depot_early), first_capacity) == no_shortage
assert shortages(combine(first_base, housing, depot_early), first_capacity) == Use(2, 1, 0)
assert shortages(combine(second_base, depot_later), second_capacity) == no_shortage

stressed_second = combine(second_base, depot_later, private_extra)
assert shortages(stressed_second, second_capacity) == Use(0, 1, 0)
assert shortages(stressed_second, Use(10, 5, 14)) == no_shortage
assert shortages(combine(stressed_second, Use(0, 0, 2)), Use(10, 5, 14)) == Use(0, 0, 2)
assert shortages(combine(second_base, private_extra), second_capacity) == no_shortage

print("Two starts fit the first cash ceiling but exceed crews by two and inspections by one.")
print("Staging fits until private demand fills the later inspection window; the unbound depot waits.")
