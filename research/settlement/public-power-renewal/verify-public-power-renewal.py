"""Check the illustrative distinction between powers and continuing services."""

EXPIRY = 0
REVIEW_DAYS = [-180, -120, -75, -45]
BENEFITS_DUE = 20
TRANSITION_HOURS = 12
EVIDENCE_HOURS = 6


def authority_on(day, primary_act_effective=None):
    return day < EXPIRY or (
        primary_act_effective is not None and primary_act_effective <= day
    )


assert REVIEW_DAYS == sorted(REVIEW_DAYS)
assert all(day < EXPIRY for day in REVIEW_DAYS)
assert authority_on(-1)
assert not authority_on(EXPIRY)
assert authority_on(EXPIRY, primary_act_effective=-1)
assert not authority_on(EXPIRY, primary_act_effective=5)
assert not authority_on(4, primary_act_effective=5)
assert authority_on(5, primary_act_effective=5)

for day, effective, expected_disposition in (
    (0, None, (False, 20)),
    (0, -1, (True, 20)),
    (0, 5, (False, 20)),
    (5, 5, (True, 20)),
):
    # The payment schedule comes from a different provision.
    disposition = (authority_on(day, primary_act_effective=effective), BENEFITS_DUE)
    assert disposition == expected_disposition

funded_hours = TRANSITION_HOURS + EVIDENCE_HOURS
assert funded_hours == 18
assert TRANSITION_HOURS + 2 * EVIDENCE_HOURS - funded_hours == 6
print("Power renewal comparison passed: expiry, prospective renewal, payment and workload.")
