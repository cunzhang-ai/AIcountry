"""Check fixed seats, explicit corrected designations and the one-slot result."""
from collections import Counter
from itertools import product


def result(choices):
    threshold = 5
    tally = Counter({"A": 4, "B": 5})
    tally.update(choice for choice in choices if choice)
    maximum = max(tally.values())
    return tuple(sorted(text for text, votes in tally.items() if votes == maximum and votes >= threshold))


if __name__ == "__main__":
    assert result(("A", "A")) == ("A",)
    assert result(("A", None)) == ("A", "B")
    assert result(("A", "B")) == ("B",)
    assert result((None, None)) == ("B",)
    possible = {result(choices) for choices in product(("A", "B", None), repeat=2)}
    assert possible == {("A",), ("B",), ("A", "B")}
    print("Corrected support can change the one protected floor slot.")
