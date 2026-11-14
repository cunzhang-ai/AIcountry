"""Check the bounded floor decision with independently restored choices."""

from itertools import product

verified = {"A": 4, "B": 3, "abstain": 3}
eligible = 12
threshold = (eligible + 3) // 4
choices = tuple(verified)


def disposition(restored):
    assert sum(verified.values()) + len(restored) == eligible
    counts = verified.copy()
    for choice in restored:
        counts[choice] += 1
    if counts["A"] > counts["B"] and counts["A"] >= threshold:
        return "A"
    if counts["B"] > counts["A"] and counts["B"] >= threshold:
        return "B"
    if counts["A"] == counts["B"] and counts["A"] >= threshold:
        return "verified lot"
    return "no eligible text"


def attainable(confirmed):
    unknown = eligible - sum(verified.values()) - len(confirmed)
    return {
        disposition(confirmed + completion)
        for completion in product(choices, repeat=unknown)
    }


assert attainable(()) == {"A", "B", "verified lot"}
assert attainable(("B",)) == {"A", "B", "verified lot"}
assert attainable(("A",)) == {"A"}
assert attainable(("B", "B")) == {"B"}
assert attainable(("A", "A")) == {"A"}
assert attainable(("B", "abstain")) == {"verified lot"}
assert attainable(("abstain", "abstain")) == {"A"}
# A possible lead does not independently qualify the process.
# Opportunity restoration and expiry remain governed by the existing rules.
assert eligible - sum(verified.values()) == 2 < eligible
# The shared vehicle already serves a protected duty in the same window.
vehicles, existing_claims = 1, 1
assert vehicles - existing_claims == 0
assert vehicles + 1 - existing_claims == 1
print("Original denominator, unresolved choices and protected vehicle capacity verified.")
