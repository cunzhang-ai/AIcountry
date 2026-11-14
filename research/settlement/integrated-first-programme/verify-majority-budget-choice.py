"""Reproduce the exact first-budget choices and proposed ordering."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import json

SEATS = 100
MAJORITY = SEATS // 2 + 1
PREPARATION = "preparation"
HOUSING = "housing"
REPAIR = "repair"
DOCKET = (PREPARATION, HOUSING, REPAIR)

# Each row gives the size, ranked tiers, and separately indicated approvals.
PROFILE = (
    (25, ((PREPARATION,), (HOUSING,), (REPAIR,)), (PREPARATION, HOUSING)),
    (30, ((HOUSING,), (PREPARATION,), (REPAIR,)), (HOUSING, PREPARATION)),
    (15, ((HOUSING,), (REPAIR,), (PREPARATION,)), (HOUSING,)),
    (30, ((REPAIR,), (PREPARATION,), (HOUSING,)), (REPAIR,)),
)


def tally(profile):
    approvals = Counter()
    comparisons = Counter()
    assert sum(size for size, _, _ in profile) <= SEATS
    for size, tiers, accepted in profile:
        ranks = {name: level for level, tier in enumerate(tiers) for name in tier}
        assert len(ranks) == sum(len(tier) for tier in tiers)
        assert set(ranks) <= set(DOCKET)
        assert len(set(accepted)) == len(accepted)
        assert set(accepted) <= set(DOCKET)
        for name in accepted:
            approvals[name] += size
        for left, right in permutations(ranks, 2):
            if ranks[left] < ranks[right]:
                comparisons[left, right] += size
    return approvals, comparisons


def final_order(profile, *, docket=DOCKET, recovered=None, prior_draw=DOCKET):
    approvals, comparisons = tally(profile)
    assert recovered is None or recovered in docket
    assert set(docket) <= set(prior_draw)
    ordinary = sorted(docket, key=lambda name: (-approvals[name], prior_draw.index(name)))
    fallback = ([recovered] if recovered else []) + [name for name in ordinary if name != recovered]
    first = [
        name for name in docket
        if len(docket) > 1 and all(
            comparisons[name, rival] >= MAJORITY for rival in docket if rival != name
        )
    ]
    assert len(first) <= 1
    return first + [name for name in fallback if name not in first]


def exact_votes(order, results):
    for name in order:
        present, yes = results[name]
        assert 0 <= yes <= present <= SEATS
        if present < MAJORITY:
            return "unheld", name
        if yes >= MAJORITY:
            return "passed", name
    return "exhausted", None


def check_budget():
    case = json.loads(Path(__file__).with_name("case.json").read_text())
    reference = case["paths"]["reference"]
    expected = {
        "weaker_preparation": ([3, 6, 0], [2, 4, 0], [1, 1, 2], 1),
        "weaker_housing": ([4, 7, 2], [3, 6, 3], [2, 2, 2], 1),
        "repair": ([0, 0, 0], [0, 0, 0], [0, 0, 0], 0),
    }
    for package, values in expected.items():
        measures = [case["measures"][key] for key in case["packages"][package]]
        for label, expected_use in zip(("national", "local", "work"), values[:3]):
            use = [sum(measure[label][window] for measure in measures) for window in range(3)]
            assert use == expected_use
            assert all(need <= cash for need, cash in zip(use, reference[label]))
        foreign = sum(measure["foreign"] for measure in measures)
        assert foreign == values[3] and foreign <= reference["foreign"]
    gross_local = [
        energy + housing for energy, housing in
        zip(case["measures"]["E"]["local"], case["housing_local_gross_due"])
    ]
    assert gross_local == [5, 9, 5]
    assert all(need <= cash for need, cash in zip(gross_local, reference["local"]))


def check_votes():
    approvals, comparisons = tally(PROFILE)
    assert approvals == {PREPARATION: 55, HOUSING: 70, REPAIR: 30}
    assert [comparisons[PREPARATION, rival] for rival in (HOUSING, REPAIR)] == [55, 55]
    assert [comparisons[rival, PREPARATION] for rival in (HOUSING, REPAIR)] == [45, 45]
    old_order = sorted(DOCKET, key=approvals.get, reverse=True)
    results = {name: (SEATS, count) for name, count in approvals.items()}
    assert exact_votes(old_order, results) == ("passed", HOUSING)
    revised_order = final_order(PROFILE)
    assert revised_order == [PREPARATION, HOUSING, REPAIR]
    assert exact_votes(revised_order, results) == ("passed", PREPARATION)
    assert final_order(PROFILE, recovered=HOUSING) == revised_order
    assert final_order(PROFILE, recovered=REPAIR) == [PREPARATION, REPAIR, HOUSING]
    assert exact_votes(revised_order, results | {PREPARATION: (100, 50)}) == ("passed", HOUSING)
    assert exact_votes(revised_order, results | {PREPARATION: (50, 49)}) == ("unheld", PREPARATION)
    assert exact_votes(revised_order, {name: (100, 50) for name in DOCKET}) == ("exhausted", None)

    omitted = ((19, PROFILE[0][1], PROFILE[0][2]), (6, (), PROFILE[0][2]), *PROFILE[1:])
    tied = (
        (19, PROFILE[0][1], PROFILE[0][2]),
        (6, (DOCKET,), PROFILE[0][2]),
        *PROFILE[1:],
    )
    for profile in (omitted, tied):
        _, pairs = tally(profile)
        assert all(pairs[PREPARATION, rival] == 49 for rival in (HOUSING, REPAIR))
        assert final_order(profile) == old_order
    assert final_order(omitted, recovered=REPAIR) == [REPAIR, HOUSING, PREPARATION]
    assert final_order(PROFILE, docket=(HOUSING,)) == [HOUSING]

    cycle = (
        (35, ((PREPARATION,), (HOUSING,), (REPAIR,)), (PREPARATION,)),
        (33, ((HOUSING,), (REPAIR,), (PREPARATION,)), (HOUSING,)),
        (32, ((REPAIR,), (PREPARATION,), (HOUSING,)), (REPAIR,)),
    )
    _, pairs = tally(cycle)
    assert [pairs[PREPARATION, HOUSING], pairs[HOUSING, REPAIR], pairs[REPAIR, PREPARATION]] == [67, 68, 65]
    assert final_order(cycle, recovered=REPAIR) == [REPAIR, PREPARATION, HOUSING]
    assert len(list(combinations(range(11), 2))) == 55


if __name__ == "__main__":
    check_budget()
    check_votes()
    print("Housing passed first at 70 under approval order. Preparation passes at 55 under the revised order.")
    print("Fallback, preference omission and ties, cycles, failed enactment and quorum all reproduced.")
