#!/usr/bin/env python3
"""Reproduce the constructed payroll and service paths in the companion case."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    extra_wages_due: int
    extra_payroll_charge: int
    restored_visits: int
    visits_received: int


def compare(small_provider_hours: int, statutory_floor: int, backup_cash: int) -> Result:
    hourly_increase = max(0, statutory_floor - 10)
    extra_wages = small_provider_hours * hourly_increase
    available_backup = min(10, backup_cash // 4, 40 - small_provider_hours)
    return Result(
        extra_wages,
        extra_wages // 4,
        available_backup,
        60 + small_provider_hours + available_backup,
    )


ordinary = compare(40, 10, 0)
funded = compare(40, 12, 40)
delayed = compare(20, 12, 0)
independent_backup = compare(20, 12, 40)

assert ordinary == Result(0, 0, 0, 100)
assert funded == Result(80, 20, 0, 100)
assert funded.extra_wages_due + funded.extra_payroll_charge + 40 == 140
assert delayed == Result(40, 10, 0, 80)
assert independent_backup == Result(40, 10, 10, 90)
assert 100 - delayed.visits_received == 20
assert 100 - independent_backup.visits_received == 10

print("Matched payroll and care: 100 visits on time, 80 after late cash, 90 with independent backup.")
