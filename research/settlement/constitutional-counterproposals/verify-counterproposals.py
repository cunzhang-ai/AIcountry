"""Reproduce the authored pairing, approval and preference rules."""


def qualifying_pair(first_vote_day, materials_ready_day):
    return first_vote_day - materials_ready_day >= 90


def result(initiative_yes, initiative_no, alternative_yes, alternative_no, preference):
    initiative = initiative_yes + initiative_no > 0 and (
        5 * initiative_yes >= 3 * (initiative_yes + initiative_no)
    )
    alternative = alternative_yes > alternative_no

    if not (initiative and alternative):
        if initiative:
            return "initiative"
        if alternative:
            return "alternative"
        return "predecessor"
    if preference is None:
        return "unresolved"
    if preference[0] >= preference[1]:
        return "initiative"
    return "alternative"


first_vote = 120 - 14
assert qualifying_pair(first_vote, 16)
assert not qualifying_pair(first_vote, 17)
assert result(630, 370, 670, 330, (540, 460)) == "initiative"
assert result(590, 410, 670, 330, (540, 460)) == "alternative"
assert result(630, 370, 670, 330, (500, 500)) == "initiative"
assert result(630, 370, 670, 330, (0, 0)) == "initiative"
assert result(630, 370, 670, 330, None) == "unresolved"
assert result(630, 370, 670, 330, (490, 510)) == "alternative"
assert result(590, 410, 500, 500, (540, 460)) == "predecessor"
assert result(630, 370, 500, 500, None) == "initiative"
print("Counterproposal: deadlines, distinct thresholds, verified tie and unresolved preference passed.")
