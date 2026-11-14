"""Reproduce the authored difference between two filing triggers."""
TRIGGERS = {"dispatch": 0, "receipt": 2}
WINDOW = 10


def timing_question(adopted_versions, filing):
    deadlines = tuple(TRIGGERS[trigger] + WINDOW for trigger in adopted_versions)
    outcomes = {filing <= deadline for deadline in deadlines}
    if len(outcomes) > 1:
        return "preserve and refer", deadlines
    return "timing agrees", deadlines


def publication_check(adopted_versions, published_versions):
    return "matches" if adopted_versions == published_versions else "correct publication"


def check_case():
    dispatch_only = ("dispatch", "dispatch")
    receipt_only = ("receipt", "receipt")
    conflicting = ("dispatch", "receipt")

    assert publication_check(receipt_only, conflicting) == "correct publication"
    assert publication_check(conflicting, conflicting) == "matches"
    assert timing_question(receipt_only, 11) == ("timing agrees", (12, 12))
    assert timing_question(conflicting, 11) == ("preserve and refer", (10, 12))
    assert timing_question(conflicting[::-1], 11) == ("preserve and refer", (12, 10))
    assert timing_question(conflicting, 9) == ("timing agrees", (10, 12))
    assert timing_question(conflicting, 10) == ("timing agrees", (10, 12))
    assert timing_question(conflicting, 12) == ("preserve and refer", (10, 12))
    assert timing_question(conflicting, 13) == ("timing agrees", (10, 12))
    assert timing_question(dispatch_only, 11) == ("timing agrees", (10, 10))
    # "Timing agrees" only describes this trigger. It decides no other
    # eligibility, exception, judicial interpretation or substantive relief.


if __name__ == "__main__":
    check_case()
    print("Adopted disagreement changes day-11 treatment; a copy error can be corrected without changing law.")
    print("Day 9 agrees on timing. Day 11 requires protected receipt and competent review regardless of version order.")
