"""Exercise the constructed school staffing comparison."""

OFFERED = 20
REMOTE_BASE = 12
ORIGIN_BASE = 20
HOURLY_COST = 50
LOCAL_BUDGET = 300
NATIONAL_GRANT = 1_000


def unmet(remote, origin):
    return max(0, OFFERED - remote) + max(0, OFFERED - origin)


def correction_trigger(missed_days, window_end):
    days_in_window = {day for day in missed_days if window_end - 29 <= day <= window_end}
    return len(days_in_window) >= 10


assert unmet(REMOTE_BASE, ORIGIN_BASE) == 8
assert unmet(REMOTE_BASE + 8, ORIGIN_BASE - 8) == 8
assert (8 + 4) * HOURLY_COST == 600

returned, shared, origin_cover, remote_alternate = 4, 4, 4, 4
return_cost = (returned + 2) * HOURLY_COST
shared_cost = (shared + 2 + 2) * HOURLY_COST
origin_cost = (origin_cover + 2) * HOURLY_COST
alternate_cost = (remote_alternate + 2) * HOURLY_COST
assert return_cost == LOCAL_BUDGET
assert return_cost + shared_cost + origin_cost + alternate_cost == LOCAL_BUDGET + NATIONAL_GRANT
assert unmet(REMOTE_BASE + returned + shared, ORIGIN_BASE - shared + origin_cover) == 0
assert unmet(REMOTE_BASE + returned, ORIGIN_BASE) == 4

# Before release, move the teacher only with working origin cover.
for origin_ready, alternate_ready, expected_remote in (
    (True, True, 20),
    (False, True, 20),
    (False, False, 16),
):
    moved = shared if origin_ready else 0
    cover = origin_cover if moved else 0
    fallback = remote_alternate if not moved and alternate_ready else 0
    remote = REMOTE_BASE + returned + moved + fallback
    origin = ORIGIN_BASE - moved + cover
    assert (remote, origin) == (expected_remote, OFFERED)

forecast_losses = [1, 2, 3, 5, 6, 9, 10, 15, 17, 21]
assert correction_trigger(forecast_losses, 30)
assert not correction_trigger(forecast_losses[:-1], 30)
assert correction_trigger(range(1, 11), 10)
assert not correction_trigger([1, *range(22, 31)], 31)
assert not correction_trigger([10] * 10, 10)
print("School staffing comparison passed: origin, budget, common loss and trigger.")
