"""Check independently adopted authorizations, commencement and follow-through."""

EXPIRY = 10
FALLBACK_VOTE_DAY = 12

national_advance = (2, 3, 2)
local_own = (2, 4, 3)
assert tuple(a + b for a, b in zip(national_advance, local_own)) == (4, 7, 5)


def effective(*, mode, national_text, local_text, proof_day, withdrawn, valid_making, operative_stay, prior_performance_required=False,
              prior_performance_verified=False):
    if mode != "common event":
        return False
    return (
        valid_making and not withdrawn and not operative_stay and proof_day <= EXPIRY
        and (not prior_performance_required or prior_performance_verified)
        and national_text is not None and national_text == local_text
    )


matched = dict(mode="common event", national_text="H exact scope",
               local_text="H exact scope", proof_day=9, withdrawn=False, valid_making=True, operative_stay=False)
assert effective(**matched)
assert effective(**(matched | {"proof_day": 10}))
assert not effective(**(matched | {"proof_day": 11}))
assert not effective(**(matched | {"mode": "mutual completed commencement"}))
assert not effective(**(matched | {"local_text": "H amended scope"}))
assert not effective(**(matched | {"local_text": None}))
assert not effective(**(matched | {"withdrawn": True}))
assert not effective(**(matched | {"valid_making": False}))
assert not effective(**(matched | {"operative_stay": True}))
assert not effective(**(matched | {"prior_performance_required": True}))
assert effective(**(matched | {"prior_performance_required": True,
                                 "prior_performance_verified": True}))


def disposition(*, effective_h, cash, staffed, lease_bound, fallback_vote):
    if lease_bound:
        return "carry binding H"
    if effective_h:
        return "release H" if cash and staffed else "H cannot release"
    return "release authorized P" if fallback_vote else "no optional start"


assert FALLBACK_VOTE_DAY > EXPIRY
state = dict(effective_h=True, cash=True, staffed=True, lease_bound=False, fallback_vote=False)
assert disposition(**state) == "release H"
assert disposition(**(state | {"cash": False})) == "H cannot release"
assert disposition(**(state | {"cash": False, "lease_bound": True})) == "carry binding H"
assert disposition(**(state | {"effective_h": False, "fallback_vote": True})) == "release authorized P"
assert disposition(**(state | {"effective_h": False})) == "no optional start"
early_protection_cost = 3
qualified_early_receipts = 0
forecast_later_receipts = 5
assert qualified_early_receipts < early_protection_cost < forecast_later_receipts
assert qualified_early_receipts + 3 >= early_protection_cost
print("Separate adoption, matched commencement, later release and fallback verified.")
