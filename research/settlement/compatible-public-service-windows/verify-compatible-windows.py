"""Check the constructed access comparison in minutes from 09:00."""


def can_confirm(
    start: int,
    available_cash: int,
    *,
    slot_available: bool = True,
    person_accepts: bool = True,
) -> bool:
    earliest_arrival = 25 + 25
    appointment_duration = 15
    cover_ends = 105
    decision_work = 30
    decision_due = 150
    cost = 4 + 1
    return (
        earliest_arrival <= start
        and start + appointment_duration <= cover_ends
        and start + appointment_duration + decision_work <= decision_due
        and available_cash >= cost
        and slot_available
        and person_accepts
    )


if __name__ == "__main__":
    assert not can_confirm(30, 6)
    assert can_confirm(70, 6)
    assert 105 - (70 + 15) == 20
    assert 150 - (70 + 15 + 30) == 35
    assert 6 - (4 + 1) == 1
    assert not can_confirm(70, 6, slot_available=False)
    assert not can_confirm(70, 4)
    assert not can_confirm(70, 6, person_accepts=False)
    assert not can_confirm(91, 6)
    print("Compatible windows require elapsed time, an accepted slot and paid capacity.")
