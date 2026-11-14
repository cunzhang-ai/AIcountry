"""Check the elapsed-time and shared-coverage assumptions of the constructed case."""

PRIOR_SHIFT = (6, 14)
EVENING_REQUEST = (20, 22)
NIGHT_REQUEST = (25, 27)
ADJACENT_REQUEST = (27, 29)
DAILY_REST = 11
DAILY_HOURS = 10
STANDBY_PRICE = 3
PAYMENT_CUTOFF = 23


def compatible_in_case(shifts):
    """The example's shifts all lie within the same 24-hour window."""
    ordered = sorted(shifts)
    if ordered[-1][1] - ordered[0][0] > 24:
        raise ValueError("The constructed check requires a common 24-hour window.")
    if sum(end - start for start, end in ordered) > DAILY_HOURS:
        return False

    period_start, last_end = ordered[0]
    for start, end in ordered[1:]:
        if start < last_end:
            return False
        if start - last_end >= DAILY_REST:
            period_start = start
        elif end - period_start > DAILY_HOURS:
            return False
        last_end = end
    return True


def standby_served(payments, *, qualified, accepted, received_in_time):
    timely_cash = sum(amount for hour, amount in payments if hour <= PAYMENT_CUTOFF)
    return timely_cash >= STANDBY_PRICE and qualified and accepted and received_in_time


def main():
    assert not compatible_in_case([PRIOR_SHIFT, EVENING_REQUEST])
    assert compatible_in_case([PRIOR_SHIFT, NIGHT_REQUEST])
    assert not compatible_in_case([NIGHT_REQUEST, NIGHT_REQUEST])
    assert not compatible_in_case([PRIOR_SHIFT, NIGHT_REQUEST, ADJACENT_REQUEST])

    assert standby_served([(23, 3)], qualified=True, accepted=True, received_in_time=True)
    assert not standby_served(
        [(23, 2), (24, 1)], qualified=True, accepted=True, received_in_time=True
    )
    assert not standby_served([(23, 3)], qualified=False, accepted=True, received_in_time=True)
    assert not standby_served([(23, 3)], qualified=True, accepted=True, received_in_time=False)
    assert not standby_served([(23, 3)], qualified=True, accepted=False, received_in_time=False)
    print("Shared staffing: rest, overlap, paid standby and actual handover passed.")


if __name__ == "__main__":
    main()
