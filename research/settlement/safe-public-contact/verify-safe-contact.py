"""Check the constructed dates and independent civil notice decision."""

RELAY_SCAN = 2
ALTERNATE_DELIVERY = 4
PAYMENT_DUE = 6
PAYMENT = 300
REPLY_PERIOD = 20
DETERMINATION_DUE = 30
CIVIL_FILING = 1


def reply_deadline(events):
    for day, receiver, usable in events:
        if receiver in {"person", "express service agent"} and usable:
            return day + REPLY_PERIOD
    return None


def civil_case_can_advance_without_ordinary_proof(*, court_direction, effective_opportunity,
                                                  deliberate_refusal):
    return court_direction and (effective_opportunity or deliberate_refusal)


scan = (RELAY_SCAN, "relay", True)
assert RELAY_SCAN + REPLY_PERIOD == 22
for events, expected_deadline in (
    ([scan], None),
    ([scan, (ALTERNATE_DELIVERY, "person", False)], None),
    ([scan, (ALTERNATE_DELIVERY, "collection agent", True)], None),
    ([scan, (ALTERNATE_DELIVERY, "person", True)], 24),
    ([scan, (ALTERNATE_DELIVERY, "express service agent", True)], 24),
):
    deadline = reply_deadline(events)
    assert deadline == expected_deadline
    # No case has grounds to interrupt the standing payment based on silence.
    assert deadline is None or PAYMENT_DUE < deadline < DETERMINATION_DUE

assert (CIVIL_FILING, PAYMENT_DUE, PAYMENT, DETERMINATION_DUE) == (1, 6, 300, 30)

assert 4 * 35 + 2 * 40 == 220
assert 2 * 50 == 100
assert 220 + 100 == 320

for direction, opportunity, refusal, can_advance in (
    (False, False, False, False),
    (True, False, False, False),
    (False, False, True, False),
    (True, False, True, True),
    (True, True, False, True),
):
    assert civil_case_can_advance_without_ordinary_proof(
        court_direction=direction, effective_opportunity=opportunity, deliberate_refusal=refusal
    ) == can_advance
print("Safe contact comparison passed: reply, payment, funding and judicial direction.")
