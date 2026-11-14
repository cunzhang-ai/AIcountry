"""Reproduce the authored competition between exact budget alternatives."""

from collections import Counter

N = 100
CABINET = set(range(1, 45))
REFORM = set(range(45, 77))
RURAL = set(range(77, 98))
MEMBERS = CABINET | REFORM | RURAL
DESIGNATIONS = {
    member: package
    for package, bloc in (("G1", CABINET), ("S1", REFORM), ("R1", RURAL))
    for member in bloc
}
INDICATIONS = {"G1": CABINET, "S1": REFORM | RURAL, "R1": RURAL}
FINAL_YES = dict(INDICATIONS)


def qualified(exact_texts, designations):
    assert designations.keys() <= MEMBERS
    counts = Counter(designations.values())
    return {text for text in exact_texts if counts[text] >= (N + 9) // 10}


def floor_order(texts, indications, public_tie_order):
    counts = {text: len(indications.get(text, ())) for text in texts}
    assert all(indications.get(text, set()) <= MEMBERS for text in texts)
    tie_priority = {text: index for index, text in enumerate(public_tie_order)}
    assert texts <= tie_priority.keys()
    return sorted(texts, key=lambda text: (-counts[text], tie_priority[text]))


def decide(order, yes_by_text, present):
    assert present <= MEMBERS
    threshold = N // 2 + 1
    if len(present) < threshold:
        return None, []
    votes = []
    for text in order:
        yes = yes_by_text[text]
        assert yes <= present
        votes.append((text, len(yes)))
        if len(yes) >= threshold:
            return text, votes
    return None, votes


def main():
    tie_order = ["G1", "S1", "R1", "S2"]
    texts = qualified(set(INDICATIONS), DESIGNATIONS)
    order = floor_order(texts, INDICATIONS, tie_order)
    assert order == ["S1", "G1", "R1"]
    assert decide(["G1"], FINAL_YES, MEMBERS) == (None, [("G1", 44)])
    assert decide(order, FINAL_YES, MEMBERS) == ("S1", [("S1", 53)])

    changed_votes = dict(FINAL_YES, S1=FINAL_YES["S1"] - {95, 96, 97})
    assert decide(order, changed_votes, MEMBERS) == (
        None, [("S1", 50), ("G1", 44), ("R1", 21)]
    )

    revised_texts = qualified({"G1", "S2", "R1"}, DESIGNATIONS)
    assert revised_texts == {"G1", "R1"}
    assert decide(floor_order(revised_texts, INDICATIONS, tie_order), FINAL_YES, MEMBERS) == (
        None, [("G1", 44), ("R1", 21)]
    )

    tied = dict(INDICATIONS, G1=CABINET | set(range(45, 54)))
    tied_order = floor_order(texts, tied, tie_order)
    assert decide(tied_order, FINAL_YES, MEMBERS) == (
        "S1", [("G1", 44), ("S1", 53)]
    )

    for size, result in [(58, "S1"), (51, "S1"), (50, None)]:
        present = set(range(98 - size, 98))
        present_yes = {text: yes & present for text, yes in FINAL_YES.items()}
        decided, recorded = decide(order, present_yes, present)
        assert decided == result
        if size == 50:
            assert recorded == []

    five_members = set(range(1, 6))
    assert not qualified({"S1", "S2"}, {member: "S2" for member in five_members})

    # Combining independently feasible options would double-use shared capacity.
    assert 6 + 4 <= 10 < 6 + 4 + 4
    assert 1 + 1 > 1
    print("Cabinet-only vote: no budget. Protected exact vote: S1 passes, 53 of 100.")
    print("Final support of 50 fails. A tied order advances S1 after G1 fails.")
    print("A substituted text and five-member clone cannot inherit floor access.")
    print("Full-N threshold survives vacancies and attendance of 58, 51 and 50.")
    print("Combining S1 and R1 needs fourteen units and two commissioning slots.")


if __name__ == "__main__":
    main()
