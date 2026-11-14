"""Check standing and independent interpreting capacity in the authored case."""
from itertools import permutations

REASONS = ("time to arrange transition", "notice must reach the person")


def electoral_standing(months, *, adult=True, local_home=True):
    return adult and local_home and months >= 6, adult and months >= 48


def accounts_available(assignments, response_day, *, vote_day=12):
    if response_day >= vote_day:
        return ()
    staff = set()
    accepted = []
    for reason, interpreter in assignments:
        if interpreter not in staff:
            staff.add(interpreter)
            accepted.append(reason)
    return tuple(accepted)


def check_hearing():
    assert electoral_standing(8) == (True, False)
    assert electoral_standing(2) == (False, False)
    assert electoral_standing(48) == (True, True)

    for order in permutations(REASONS):
        one = tuple((reason, "shared interpreter") for reason in order)
        separate = tuple(zip(order, ("interpreter A", "interpreter B")))
        assert len(accounts_available(one, response_day=10)) == 1
        assert set(accounts_available(separate, response_day=10)) == set(REASONS)
        assert not accounts_available(separate, response_day=13)
        # The hearing supplies no electoral qualification or binding assent.


if __name__ == "__main__":
    check_hearing()
    print("Both adults can raise direct effects. Neither supplies national-elector initiative support in the fixture.")
    print("Two simultaneous interpretations preserve both reasons before the vote. One interpreter or a late response cannot.")
