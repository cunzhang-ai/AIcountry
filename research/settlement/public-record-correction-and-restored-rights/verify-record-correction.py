"""Check period matching, handoff and actual remedy in a constructed case."""

APRIL_RECORD = ("April", 1, 90)
MAY_RECORD = ("May", 1, 80)
HOUSING_DUE = 5


def update_record(record, notice):
    period, revision, _ = record
    notice_period, notice_revision, _ = notice
    if period == notice_period and notice_revision > revision:
        return notice
    return record


def housing_shortfall(eligible, receipts, deadline):
    if not eligible:
        return 0
    received = sum(amount for day, amount in receipts if day <= deadline)
    return HOUSING_DUE - received


def timely_trip(record, accepted_day, delivered_day):
    _, _, earnings = record
    return (
        earnings <= 40
        and accepted_day is not None
        and delivered_day is not None
        and accepted_day <= delivered_day <= 1
    )


def main():
    april_correction = ("April", 2, 30)
    june_change = ("June", 1, 30)
    housing_record = update_record(APRIL_RECORD, april_correction)
    travel_record = update_record(APRIL_RECORD, april_correction)

    assert housing_record == travel_record == april_correction
    assert update_record(housing_record, APRIL_RECORD) == april_correction
    assert update_record(housing_record, april_correction) == april_correction
    assert update_record(MAY_RECORD, april_correction) == MAY_RECORD
    assert update_record(APRIL_RECORD, june_change) == APRIL_RECORD

    eligible = housing_record[2] <= 50
    assert housing_shortfall(eligible, [], deadline=2) == 5  # A returned transfer.
    assert housing_shortfall(eligible, [(2, 5)], deadline=2) == 0
    assert housing_shortfall(eligible, [(3, 5)], deadline=2) == 5
    assert housing_shortfall(eligible, [(3, 5)], deadline=3) == 0
    repeated_notice = update_record(housing_record, april_correction)
    assert housing_shortfall(repeated_notice[2] <= 50, [(2, 5)], deadline=2) == 0

    assert not timely_trip(APRIL_RECORD, accepted_day=1, delivered_day=1)
    assert timely_trip(travel_record, accepted_day=1, delivered_day=1)
    assert not timely_trip(travel_record, accepted_day=None, delivered_day=None)
    assert not timely_trip(travel_record, accepted_day=1, delivered_day=2)
    print("Record correction: fact periods, stale replay, urgent receipt and settlement passed.")


if __name__ == "__main__":
    main()
