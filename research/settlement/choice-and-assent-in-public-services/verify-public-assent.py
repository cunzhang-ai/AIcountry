"""Check the constructed choice and standing service comparison."""

DUE_PAYMENTS = 20
ORDINARY_APPOINTMENTS = 4
PEOPLE_PER_APPOINTMENT = 2
DIRECT_PAYMENT_CHOICES = 12
STAFFED_PAYMENT_CHOICES = 8
INDEPENDENT_REVIEW_COST = 2


def valid_permission(response, *, explained=True, authorized=True):
    return response == "affirmed" and explained and authorized


assert not valid_permission("completed visit")
assert not valid_permission("silent")
assert not valid_permission("declined")
assert not valid_permission("affirmed", explained=False)
assert not valid_permission("affirmed", authorized=False)
assert valid_permission("affirmed")

responses = ["affirmed"] * 12 + ["silent"] * 5 + ["declined"] * 3
affirmative = sum(valid_permission(response) for response in responses)
unsupported_records = len(responses) - affirmative
assert affirmative == 12
assert unsupported_records == 8
assert len(responses) == DUE_PAYMENTS

assert DIRECT_PAYMENT_CHOICES + STAFFED_PAYMENT_CHOICES == DUE_PAYMENTS
for appointments, expected in ((ORDINARY_APPOINTMENTS, (20, 0)),
                               (ORDINARY_APPOINTMENTS - 1, (18, 2))):
    staffed_receipts = min(STAFFED_PAYMENT_CHOICES, appointments * PEOPLE_PER_APPOINTMENT)
    received = DIRECT_PAYMENT_CHOICES + staffed_receipts
    assert (received, DUE_PAYMENTS - received) == expected

assert ORDINARY_APPOINTMENTS + INDEPENDENT_REVIEW_COST == 6
print("Public assent comparison passed: valid scope, standing payment and staffed alternatives.")
