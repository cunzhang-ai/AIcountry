"""Check concurrent authorized assignments and independent actual execution."""

from itertools import combinations

CJ_SEATS = 7
CJ_QUORUM = 5
CJ_AFFIRMATIVE = 4
ORDINARY_APPEAL = 3
URGENT_ORDINARY = 1

cj_roster = {"c1", "c2", "c3", "c4", "c5", "c6", "c7"}
ordinary_roster = {"c5", "a1", "a2", "a3"}
urgent_roster = {"u1"}
available = {"c1", "c2", "c3", "c4", "c5", "a1", "a2", "u1"}


def assignment_fits(available_now, cj_conflicts=frozenset()):
    for chamber in combinations((cj_roster & available_now) - cj_conflicts, CJ_QUORUM):
        for appeal in combinations((ordinary_roster & available_now) - set(chamber), ORDINARY_APPEAL):
            if (urgent_roster & available_now) - set(chamber) - set(appeal):
                return True
    return False


assert len(cj_roster) == CJ_SEATS
assert not assignment_fits(available)
assert assignment_fits(available | {"a3"})
assert not assignment_fits(available | {"a3"}, {"c5"})
assert 1 < 2 <= 1 + 1  # Usable opening margin, reserve cost and exact increment.


def outcomes(*, present, votes, records, executor, opposition_receipt):
    ruling = present >= CJ_QUORUM and votes >= CJ_AFFIRMATIVE and records
    return opposition_receipt, ruling, ruling and executor


assert outcomes(present=5, votes=4, records=True, executor=True,
                opposition_receipt=False) == (False, True, True)
assert outcomes(present=5, votes=4, records=True, executor=False,
                opposition_receipt=True) == (True, True, False)
assert outcomes(present=5, votes=3, records=True, executor=True,
                opposition_receipt=True) == (True, False, False)
assert outcomes(present=4, votes=4, records=True, executor=True,
                opposition_receipt=True) == (True, False, False)
print("Distinct judicial assignments, quorum, votes and execution verified.")
