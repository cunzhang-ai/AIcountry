"""Verify the constructed handback calendar and restricted payments."""

ANNUAL_EFFECT = 91
OUTER_END = 101
WATER_CAP = 4


def provider(day, accepted_day):
    if accepted_day is not None and day >= max(ANNUAL_EFFECT, accepted_day):
        return "successor"
    if ANNUAL_EFFECT <= day < OUTER_END:
        return "continuation"
    return "uncovered"


assert provider(91, 90) == "successor"
assert provider(92, 97) == "continuation"
assert provider(98, 97) == "successor"
assert provider(98, None) == "continuation"
assert provider(102, None) == "uncovered"
assert provider(102, 97) == "successor"
assert sum(2 for day in (92, 98) if provider(day, 97) == "continuation") == 2
assert sum(2 for day in (92, 98) if provider(day, None) == "continuation") == WATER_CAP


def received(day, accepted_day, successor_operational=True):
    actor = provider(day, accepted_day)
    if actor == "successor" and not successor_operational:
        return "unserved; original claim continues"
    return actor


assert received(98, 97, successor_operational=False) == "unserved; original claim continues"
assert received(98, None, successor_operational=False) == "continuation"


def closeout_eligible(*, bridge_commitment, earned_by_expiry, payment_day):
    return bridge_commitment and earned_by_expiry and 91 <= payment_day <= 120


assert not closeout_eligible(bridge_commitment=False, earned_by_expiry=True, payment_day=93)
assert closeout_eligible(bridge_commitment=True, earned_by_expiry=True, payment_day=94)
assert not closeout_eligible(bridge_commitment=True, earned_by_expiry=False, payment_day=98)
assert not closeout_eligible(bridge_commitment=True, earned_by_expiry=True, payment_day=121)
print("Distinct handback dates, fixed expiry, water cap and accrued-only closeout verified.")
