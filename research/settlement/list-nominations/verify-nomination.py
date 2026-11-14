"""Reproduce the authored NM nomination bounds and public seat example."""

from fractions import Fraction


def award(votes, capacities, seats):
    allocated = dict.fromkeys(votes, 0)
    sequence = []
    for _ in range(seats):
        eligible = [name for name in votes if allocated[name] < capacities[name]
                    and votes[name] > 0]
        if not eligible:
            break
        winner = max(eligible, key=lambda name: (
            Fraction(votes[name], 2 * allocated[name] + 1), votes[name]
        ))
        # The named fixture has no ties needing the public draw.
        sequence.append(winner)
        allocated[winner] += 1
    return sequence


if __name__ == "__main__":
    materials, vote_close, result, freeze = -51, -48, -47, -40
    minimum_voting_hours = 48
    late_finding = -41
    assert (vote_close - materials) * 24 >= minimum_voting_hours
    assert freeze - result == 7
    assert (freeze - late_finding) * 24 < minimum_voting_hours

    received = {"Nila": 38, "Bo": 44}
    withheld_originals = 18
    corrected = received | {"Nila": received["Nila"] + withheld_originals}
    assert corrected == {"Nila": 56, "Bo": 44}

    # In the separate denial-of-access case, missing choices cannot be
    # reconstructed. Compare two possible endpoints, not inferred votes.
    assert max(corrected, key=corrected.get) == "Nila"
    opposite = received | {"Bo": received["Bo"] + withheld_originals}
    assert max(opposite, key=opposite.get) == "Bo"

    votes = {"A": 300, "B": 130, "C": 70}
    complete = {"A": 3, "B": 1, "C": 1}
    assert award(votes, complete, 5) == ["A", "B", "A", "C", "A"]
    assert award(votes, complete | {"A": 2}, 5) == ["A", "B", "A", "C"]
    print("Seven days after the result; a one-day interval cannot fit a rerun.")
    print("Protected originals: 56–44. Missing choices: outcome indeterminate.")
    print("Full pool: A, B, A, C, A. Two A nominees: one seat unfilled.")
