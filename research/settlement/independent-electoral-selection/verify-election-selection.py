"""Reproduce Design288's constructed appointment and decision window."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Appointment:
    source_attendance: tuple[int, int, int]
    source_yes: tuple[int, int, int]
    notice: int = -48
    vote: int = -30
    published: int = -30
    takes_office: int = 0
    records: bool = True
    accepted: bool = True
    staffed_review: bool = True


def can_seat(appointment, decision_day):
    attendance = appointment.source_attendance
    yes = appointment.source_yes
    lawful_vote = (
        all(1 <= affirmative <= present <= 3 for affirmative, present in zip(yes, attendance))
        and sum(attendance) >= 6
        and sum(yes) >= 6
    )
    lawful_timing = (
        appointment.vote - appointment.notice >= 14
        and appointment.vote <= appointment.published
        and appointment.takes_office - appointment.published >= 21
        and appointment.takes_office <= decision_day
    )
    return all((
        lawful_vote, lawful_timing, appointment.records,
        appointment.accepted, appointment.staffed_review,
    ))


def commission_can_decide(present, affirmative):
    return 4 <= affirmative <= present and 5 <= present <= 7


def main():
    independent = Appointment((3, 2, 2), (3, 2, 1))
    no_lay = replace(independent, source_attendance=(3, 3, 0), source_yes=(3, 3, 0))
    lawful_refusal = replace(independent, source_yes=(3, 2, 0))
    delayed = replace(independent, takes_office=8)
    late_notice = replace(independent, published=-20)
    candidates_denied_entry = replace(independent, records=False)
    unqualified_review = replace(independent, staffed_review=False)
    deadline = 7
    assert can_seat(independent, deadline)
    for blocked in (no_lay, lawful_refusal, delayed, late_notice, candidates_denied_entry, unqualified_review):
        assert not can_seat(blocked, deadline)

    assert not commission_can_decide(4 + can_seat(no_lay, deadline), 4)
    present = 4 + can_seat(independent, deadline)
    assert commission_can_decide(present, 4)
    assert not commission_can_decide(present, 3)
    assert not commission_can_decide(4, 4)

    ordinary_slots = 12
    constitutional_slots = 9
    election_slots = 9
    assert ordinary_slots + constitutional_slots == 21
    assert ordinary_slots + constitutional_slots + election_slots == 30

    original_hearing, appointment_challenge = 'ordinary due hearing', 'appointment challenge'
    required_hearings = {original_hearing, appointment_challenge}
    assert required_hearings - {appointment_challenge} == {original_hearing}
    assert not required_hearings - {original_hearing, appointment_challenge}
    print('Electoral selection passed: source loss, timely appointment, decision votes and court cover.')


if __name__ == '__main__':
    main()
