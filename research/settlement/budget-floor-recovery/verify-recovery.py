"""Reproduce the authored priority and final votes with exact text identity."""

from collections import Counter

N = 100
MAJORITY = N // 2 + 1
GOVERNMENT = set(range(1, 47))
OPPOSITION = set(range(47, 90))
INDEPENDENTS = set(range(90, 98))
MEMBERS = GOVERNMENT | OPPOSITION | INDEPENDENTS
PRIORITY_SUPPORTERS = INDEPENDENTS | OPPOSITION | {1}
ORDINARY_ORDER = ["G", "O"]
FINAL_YES = {
    "I": PRIORITY_SUPPORTERS - {1},
    "G": GOVERNMENT | INDEPENDENTS,
    "O": OPPOSITION,
}
# Identity is established from operative text and binding conditions.
REQUESTED_TEXT = {"I": "I", "I_same_text": "I", "I2": "I2"}


def priority_ballot(choices, present, requested_text):
    assert present <= MEMBERS
    if len(present) < MAJORITY:
        return "unheld", None, Counter()

    members = [member for member, _ in choices]
    assert set(members) <= present
    assert len(members) == len(set(members)), "Only one selection per member."
    tallies = Counter(requested_text[entry] for _, entry in choices)
    admitted = [text for text, count in tallies.items() if count >= MAJORITY]
    assert len(admitted) <= 1
    return "held", next(iter(admitted), None), tallies


def final_votes(priority, unchanged_texts, yes_by_text):
    order = [priority] + ORDINARY_ORDER if priority in unchanged_texts else ORDINARY_ORDER
    counts = []
    for text in order:
        affirmative = yes_by_text[text]
        assert affirmative <= MEMBERS
        counts.append((text, len(affirmative)))
        if len(affirmative) >= MAJORITY:
            return text, counts
    return None, counts


def main():
    assert len(MEMBERS) == 97
    assert len(INDEPENDENTS) < (N + 9) // 10
    choices = [(member, "I") for member in sorted(PRIORITY_SUPPORTERS)]
    unchanged = {"I", "G", "O"}

    held, priority, tallies = priority_ballot(choices, MEMBERS, REQUESTED_TEXT)
    assert (held, priority, tallies) == ("held", "I", {"I": 52})
    assert final_votes(priority, unchanged, FINAL_YES) == ("I", [("I", 51)])
    assert final_votes(None, unchanged, FINAL_YES) == ("G", [("G", 54)])

    withdrawals = dict(FINAL_YES, I=FINAL_YES["I"] - {90})
    assert final_votes(priority, unchanged, withdrawals) == ("G", [("I", 50), ("G", 54)])

    split = choices[:27] + [(member, "I2") for member, _ in choices[27:]]
    assert priority_ballot(split, MEMBERS, REQUESTED_TEXT) == (
        "held", None, {"I": 27, "I2": 25}
    )

    aliases = choices[:27] + [(member, "I_same_text") for member, _ in choices[27:]]
    assert priority_ballot(aliases, MEMBERS, REQUESTED_TEXT) == ("held", "I", {"I": 52})

    absent_quorum = set(range(1, 51))
    assert priority_ballot([], absent_quorum, REQUESTED_TEXT) == ("unheld", None, {})
    assert final_votes(priority, {"I2", "G", "O"}, FINAL_YES) == ("G", [("G", 54)])

    try:
        priority_ballot(choices + [choices[0]], MEMBERS, REQUESTED_TEXT)
    except AssertionError as error:
        assert str(error) == "Only one selection per member."
    else:
        raise AssertionError("A repeated member was accepted.")

    print("Eight ordinary sponsors miss the ten-percent gate.")
    print("Priority: 52 actual members. Final approval: 51 separate yes votes.")
    print("Final support of 50 fails; ordinary G passes with 54.")
    print("Identical labels aggregate distinct people; material versions remain 27 and 25.")
    print("An unavailable quorum is unheld; a replacement cannot inherit priority.")


if __name__ == "__main__":
    main()
