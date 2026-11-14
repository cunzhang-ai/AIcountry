"""Reproduce the authored independent-capacity and receipt comparisons."""

government_and_rival = {"government amendment", "rival amendment"}
ordinary_authoring = {"government amendment"}
independent_authoring = {"rival amendment"}

assert not government_and_rival <= ordinary_authoring
assert government_and_rival <= (ordinary_authoring | independent_authoring)
assert not government_and_rival <= (ordinary_authoring | ordinary_authoring)

cutoffs = {"care": 3, "opposition evidence": 4, "successor act": 6}
shared = {"care": 3, "opposition evidence": 7, "successor act": 5}
separate = {"care": 3, "opposition evidence": 3, "successor act": 5}


def late(receipt, deadlines):
    return {duty for duty, cutoff in deadlines.items() if receipt.get(duty, float("inf")) > cutoff}


assert late(shared, cutoffs) == {"opposition evidence"}
assert not late(separate, cutoffs)
assert late(separate, cutoffs | {"next care": 8}) == {"next care"}
assert not late(separate | {"next care": 8}, cutoffs | {"next care": 8})

print("A restored chamber leaves authoring exposed. A first executed remedy leaves the next call to qualify.")
