"""Check the declared timetable, role and staffing facts in the worked case."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Capacity:
    service: int
    correction: int
    briefings: int
    independent_review: int

    def covers(self, required):
        return all((
            self.service >= required.service,
            self.correction >= required.correction,
            self.briefings >= required.briefings,
            self.independent_review >= required.independent_review,
        ))


def available_briefing_hours(qualified, remaining_hours, first_pass_hours):
    return min(remaining_hours, first_pass_hours) if qualified else 0


def may_direct_service(requester, lawful_office_holder, request_in_scope):
    return requester == lawful_office_holder and request_in_scope


def useful_receipt(receipt_hour, decision_hour, time_to_use):
    return receipt_hour is not None and receipt_hour + time_to_use <= decision_hour


def main():
    qualified_contestants = 3
    hours_per_first_pass = 2
    required = Capacity(8, 2, qualified_contestants * hours_per_first_pass, 2)
    assert sum(vars(required).values()) == 18
    assert required.covers(required)
    assert not Capacity(8, 2, 4, 2).covers(required)
    assert not Capacity(8, 2, 8, 0).covers(required)

    assert available_briefing_hours(True, 48, hours_per_first_pass) == 2
    assert available_briefing_hours(False, 48, hours_per_first_pass) == 0
    assert available_briefing_hours(True, 1, hours_per_first_pass) == 1
    assert useful_receipt(24, 48, 12)
    assert not useful_receipt(45, 48, 12)
    assert not useful_receipt(None, 48, 12)

    assert may_direct_service("caretaker", "caretaker", True)
    assert not may_direct_service("caretaker", "caretaker", False)
    assert not may_direct_service("group_a", "caretaker", True)
    assert may_direct_service("group_a", "group_a", True)
    print("Transition preparation: separated capacity, eligibility and useful receipt passed.")


if __name__ == "__main__":
    main()
