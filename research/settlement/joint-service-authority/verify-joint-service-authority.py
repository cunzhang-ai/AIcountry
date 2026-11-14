"""Check the constructed joint-service authority and resource boundaries."""
from itertools import combinations

POPULATION = {"A": 58, "B": 20, "C": 12, "D": 10}
TOTAL_CASH = 18
CONTINUING_CASH = 12
OPTIONAL_COST = 6


def vote(affirmative, *, inside_compact=True):
    assert set(affirmative) <= POPULATION.keys()
    councils = len(set(affirmative))
    residents = sum(POPULATION[council] for council in set(affirmative))
    passes = (
        inside_compact
        and councils * 2 > len(POPULATION)
        and residents * 2 > sum(POPULATION.values())
    )
    return councils, residents, passes


def optional_release(approved_count, *, vehicle_slots=1):
    if approved_count == 0:
        return "retained service"
    available = TOTAL_CASH - CONTINUING_CASH
    if approved_count * OPTIONAL_COST > available or approved_count > vehicle_slots:
        return "hold optional scope"
    return "optional release fits"


def check_joint_service():
    assert vote("A") == (1, 58, False)
    assert vote("BCD") == (3, 42, False)
    assert vote("ACD") == (3, 80, True)
    assert vote("AC") == (2, 70, False)
    assert vote("ACD", inside_compact=False) == (3, 80, False)
    assert vote("ACCD") == (3, 80, True)
    assert not any(vote(group)[2] for size in range(4) for group in combinations("BCD", size))
    assert not vote("AB")[2]

    assert optional_release(0) == "retained service"
    assert optional_release(1) == "optional release fits"
    assert optional_release(2) == "hold optional scope"
    assert optional_release(1, vehicle_slots=0) == "hold optional scope"


if __name__ == "__main__":
    check_joint_service()
    print("One council with 58 percent and three councils with 42 percent each fail a threshold.")
    print("Three councils with 80 percent authorize one in-scope option. An outside levy and shared capacity conflict fail.")
