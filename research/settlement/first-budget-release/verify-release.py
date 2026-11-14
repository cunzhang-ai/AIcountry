"""Reproduce the authored first-budget case without choosing political priorities."""

from collections import Counter
from itertools import combinations

FIELDS = (
    "early_cash", "total_cash", "recurring", "early_commission",
    "late_commission", "early_assurance", "late_assurance",
)
CORE = ("C", "W", "J")
OPTIONAL = ("P", "H", "D")
USES = {
    "C": (2, 4, 1, 1, 0, 0, 0),
    "W": (3, 4, 1, 1, 0, 0, 0),
    "J": (1, 2, 0, 0, 0, 1, 1),
    "P": (1, 3, 0, 0, 1, 0, 1),
    "H": (2, 5, 2, 1, 0, 1, 0),
    "D": (2, 4, 1, 0, 1, 1, 1),
    "water_switch": (1, 1, 0, 0, 0, 0, 0),
}
LIMITS = {
    "ordinary": (8, 15, 4, 2, 1, 2, 2),
    "weak": (7, 13, 3, 2, 1, 2, 2),
    "weak_with_early_bridge": (8, 14, 3, 2, 1, 2, 2),
    "early_delay": (5, 15, 4, 2, 1, 2, 2),
}


def shortfalls(options, scenario, lost_water_provider=False):
    measures = CORE + options
    if lost_water_provider:
        measures += ("water_switch",)
    totals = Counter()
    for measure in measures:
        totals.update(dict(zip(FIELDS, USES[measure])))
    return {
        name: totals[name] - available
        for name, available in zip(FIELDS, LIMITS[scenario])
        if totals[name] > available
    }


def feasible_options(scenario, lost_water_provider=False):
    return {
        options for count in range(len(OPTIONAL) + 1)
        for options in combinations(OPTIONAL, count)
        if not shortfalls(options, scenario, lost_water_provider)
    }


if __name__ == "__main__":
    assert feasible_options("ordinary") == {(), ("P",), ("D",)}
    assert feasible_options("weak") == {(), ("P",)}
    assert feasible_options("ordinary", True) == {(), ("P",)}
    assert feasible_options("weak", True) == {()}
    assert feasible_options("early_delay") == set()
    assert shortfalls(("H",), "ordinary") == {"early_commission": 1}
    assert shortfalls(("P", "D"), "ordinary") == {
        "early_cash": 1, "total_cash": 2, "late_commission": 1, "late_assurance": 1
    }
    # With P already binding, dropping it is not a lawful recovery branch.
    assert shortfalls(("P",), "weak", True) == {"early_cash": 1, "total_cash": 1}
    assert shortfalls(("P",), "weak_with_early_bridge", True) == {}
    assert shortfalls((), "early_delay") == {"early_cash": 1}
    print("Ordinary: core, core + P and core + D fit. H lacks an early crew.")
    print("Weak + provider loss: only core fits before optional commitment.")
    print("Already-bound P leaves one unit uncovered early and cumulatively.")
