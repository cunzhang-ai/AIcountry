"""Check the constructed like-period noise and distinct event comparison."""

from math import log10

AVERAGE_LIMIT = 50
EVENT_LIMIT = 4


def combined_level(*source_levels):
    return 10 * log10(sum(10 ** (level / 10) for level in source_levels))


def exceedances(road, rail, events, *, allowance=0):
    return combined_level(road, rail) + allowance > AVERAGE_LIMIT, events > EVENT_LIMIT


assert round(combined_level(48, 48), 2) == 51.01
assert exceedances(48, 48, 9) == (True, True)
assert exceedances(47, 44, 3) == (False, False)

assert round(combined_level(43, 48), 2) == 49.19
assert exceedances(43, 48, 7) == (False, True)
assert round(combined_level(50, 44), 2) == 50.97
assert exceedances(50, 44, 9) == (True, True)

assert exceedances(44, 47, 3, allowance=0.5) == (False, False)
assert exceedances(46, 44, 3, allowance=0.5) == (False, False)

source_work, verification = 6, 2
cash_available = 6
assert source_work <= cash_available < source_work + verification
assert source_work + verification - cash_available == 2

print("Night exposure comparison passed: acoustic energy, separate events, both places and funding.")
