"""Reproduce the authored recall gate, vote and separate successor."""


def petition_passes(valid_signatures, opening_electorate):
    return 100 * valid_signatures >= 15 * opening_electorate


def recall_passes(yes, no, opening_electorate):
    return yes > no and 4 * yes >= opening_electorate


def disposition(recall, replacement_valid):
    if recall is None:
        return "recall unresolved"
    if not recall:
        return "ordinary council"
    if replacement_valid:
        return "replacement for remainder"
    return "limited caretaker"


electorate = 10_000
assert petition_passes(1570 - 70, electorate)
assert not petition_passes(1499, electorate)
assert not petition_passes(1500, 10_001)
call_to_close, voting_window = 90, 14
assert call_to_close - voting_window == 76
first_ordinary_vote = 250
assert 159 + call_to_close < first_ordinary_vote
assert not 160 + call_to_close < first_ordinary_vote
assert recall_passes(2600, 2400, electorate)
assert not recall_passes(2450, 550, electorate)
assert not recall_passes(2500, 2500, electorate)
assert recall_passes(2500, 2499, electorate)
assert not recall_passes(0, 0, electorate)
assert disposition(True, True) == "replacement for remainder"
assert disposition(False, True) == "ordinary council"
assert disposition(True, False) == "limited caretaker"
assert disposition(None, True) == "recall unresolved"
print("Local recall: petition, affirmative floor, separate successor and unresolved results passed.")
