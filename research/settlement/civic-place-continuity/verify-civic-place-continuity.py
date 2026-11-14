"""Verify the constructed evening uses, distinct rooms and closure."""
from itertools import permutations

USES = ("free drop-in", "protected booking")
ROOMS = {"school": 3, "community": 2}


def feasible_assignments(cash, accepted_rooms):
    options = []
    for count in range(len(USES) + 1):
        for uses in permutations(USES, count):
            for rooms in permutations(accepted_rooms, count):
                cost = sum(ROOMS[room] for room in rooms)
                if cost <= cash:
                    options.append((tuple(zip(uses, rooms)), cost))
    return options


def check_evening():
    assert feasible_assignments(5, ()) == [((), 0)]
    assert max(len(assignment) for assignment, _ in feasible_assignments(5, ("school",))) == 1
    assert max(len(assignment) for assignment, _ in feasible_assignments(4, ROOMS)) == 1

    joined = [cost for assignment, cost in feasible_assignments(5, ROOMS) if len(assignment) == 2]
    assert joined and set(joined) == {5}

    committed = 5
    accepting_after_route_loss = ()
    assert feasible_assignments(committed, accepting_after_route_loss) == [((), 0)]
    assert committed == 5


if __name__ == "__main__":
    check_evening()
    print("Both simultaneous uses fit at five units with distinct rooms. Only one fits at four.")
    print("Daytime vouchers and a complete route loss supply neither evening use.")
