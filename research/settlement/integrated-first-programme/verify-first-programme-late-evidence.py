"""Check chronological feasibility of the constructed first-programme choices."""

OPENING_CASH = 10
STANDING_PAYMENTS = 8
LATER_RECEIPT = 2
EARLY_ENVELOPE = OPENING_CASH - STANDING_PAYMENTS
TOTAL_ENVELOPE = EARLY_ENVELOPE + LATER_RECEIPT
FIRST_RELIABLE_SIGNAL = 4
LATEST_ACTIVATION = 4
DUE_DAY = 5
ORDINARY_LEAD_TIME = 4


def ordinary_receipt_day(decision_day):
    return decision_day + ORDINARY_LEAD_TIME


def fixed_coverage(prepared, actual_loss):
    return int(prepared == actual_loss and ordinary_receipt_day(1) <= DUE_DAY)


def reserve_coverage(losses, *, verified_day, payment_day, accepting_route):
    if not accepting_route or verified_day is None or payment_day is None:
        return 0
    activation = max(verified_day, payment_day)
    if activation > LATEST_ACTIVATION or activation + 1 > DUE_DAY:
        return 0
    # This is capacity only. The governing law decides any competing calls.
    return min(1, len(losses))


def main():
    assert ordinary_receipt_day(FIRST_RELIABLE_SIGNAL) == 8 > DUE_DAY
    assert ordinary_receipt_day(1) == DUE_DAY
    assert 2 <= EARLY_ENVELOPE and 2 + 1 <= TOTAL_ENVELOPE
    assert 2 + 2 > EARLY_ENVELOPE and 3 + 3 > TOTAL_ENVELOPE
    assert 2 <= EARLY_ENVELOPE and 2 + 2 == TOTAL_ENVELOPE

    events = ("water", "care")
    assert [fixed_coverage("water", event) for event in events] == [1, 0]
    assert [fixed_coverage("care", event) for event in events] == [0, 1]
    ready = dict(verified_day=4, payment_day=4, accepting_route=True)
    assert [reserve_coverage([event], **ready) for event in events] == [1, 1]
    assert reserve_coverage([], **ready) == 0
    assert reserve_coverage(events, **ready) == 1
    for unavailable in (
        {"verified_day": 5},
        {"verified_day": None},
        {"payment_day": 5},
        {"accepting_route": False},
    ):
        assert reserve_coverage(["care"], **(ready | unavailable)) == 0
    print("First programme: same initial choice, actual warning, paid reserve and unmet calls passed.")


if __name__ == "__main__":
    main()
