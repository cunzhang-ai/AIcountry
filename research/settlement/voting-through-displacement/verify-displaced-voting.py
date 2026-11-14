"""Reproduce the authored joint election, shelter and rescue comparison."""

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Route:
    capacity: int
    cost: int
    latest_receipt: int
    distinct_crew: bool

    def civic_slots(self, close):
        if self.latest_receipt <= close and self.distinct_crew:
            return self.capacity
        return 0


close = 0
electors = 120
cash = 22
rescue = 12
shelter = 6
rescue_due, rescue_received = 20, 20
rescue_deadline, rescue_receipt = -4, -5
shelter_due, shelter_received = 120, 120
shelter_deadline, shelter_receipt = -2, -2
assert rescue_received >= rescue_due and rescue_receipt <= rescue_deadline
assert shelter_received >= shelter_due and shelter_receipt <= shelter_deadline

host = Route(capacity=80, cost=2, latest_receipt=-1, distinct_crew=True)
shared_shuttle = Route(capacity=40, cost=1, latest_receipt=-1, distinct_crew=False)
mobile = Route(capacity=40, cost=2, latest_receipt=-1, distinct_crew=True)
short_mobile = Route(capacity=30, cost=2, latest_receipt=-1, distinct_crew=True)
late_mobile = Route(capacity=40, cost=2, latest_receipt=1, distinct_crew=True)

assert rescue + shelter + host.cost + shared_shuttle.cost == 21
assert electors - host.civic_slots(close) - shared_shuttle.civic_slots(close) == 40
assert rescue + shelter + host.cost + mobile.cost == cash
assert host.civic_slots(close) + mobile.civic_slots(close) == electors
assert electors - host.civic_slots(close) - short_mobile.civic_slots(close) == 10
assert late_mobile.civic_slots(close) == 0

accepted_at_host = -1
transferred_to_origin = 3
assert accepted_at_host <= close < transferred_to_origin
ordinary = 117
conditional = {"supported proof": True, "source correction": True, "duplicate": False}
assert ordinary + len(conditional) == electors
assert ordinary + sum(conditional.values()) == 119
# Scope: two lists, each with enough eligible willing nominees.
def local_seats(first, second):
    votes = (first, second)
    seats = [0, 0]
    for _ in range(9):
        quotients = [Fraction(votes[i], 2 * seats[i] + 1) for i in range(2)]
        assert quotients[0] != quotients[1]
        seats[quotients.index(max(quotients))] += 1
    return tuple(seats)


assert local_seats(94, 86) == (5, 4)
assert local_seats(94, 96) == (4, 5)
for first_addition in range(11):
    for second_addition in range(11 - first_addition):
        assert local_seats(104 + first_addition, 76 + second_addition) == (5, 4)
print("Displaced voting: joint funding, crew conflict, receipt, conditional count and bounded list-seat effects passed.")
