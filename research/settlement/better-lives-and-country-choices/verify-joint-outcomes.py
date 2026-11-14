"""Verify the reversal and uncertainty in the constructed same-person case."""

POPULATION = set(range(1, 11))
separate_heat = set(range(1, 9))
separate_care = set(range(3, 11))
coordinated_heat = set(range(1, 8))
coordinated_care = set(range(1, 8))


def marginal_overlap_bounds(first_count, second_count, eligible):
    return max(0, first_count + second_count - eligible), min(first_count, second_count)


def usable_bounds(heat, care, confirmed, unresolved):
    overlap = heat & care
    assert heat | care <= POPULATION
    assert not confirmed & unresolved
    assert confirmed | unresolved <= overlap
    return len(confirmed), len(confirmed | unresolved)


assert marginal_overlap_bounds(len(separate_heat), len(separate_care), len(POPULATION)) == (6, 8)
assert len(separate_heat & separate_care) == 6
separate_confirmed = set(range(3, 8))
coordinated_confirmed = set(range(1, 8))
assert usable_bounds(separate_heat, separate_care, separate_confirmed, set()) == (5, 5)
assert usable_bounds(coordinated_heat, coordinated_care, coordinated_confirmed, set()) == (7, 7)
separate_range = usable_bounds(separate_heat, separate_care, separate_confirmed, {8})
coordinated_range = usable_bounds(coordinated_heat, coordinated_care, coordinated_confirmed - {7}, {7})
assert separate_range == (5, 6)
assert coordinated_range == (6, 7)
assert not coordinated_range[0] > separate_range[1]
print("Separate service counts reverse the usable-route result; partial records leave overlap unresolved.")
