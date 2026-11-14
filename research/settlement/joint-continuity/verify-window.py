"""Reproduce Design232's authored window and incremental budget comparison."""

from collections import Counter
from itertools import combinations

WINDOWS = {
    "C": (1, 4, 4, "clinic crew"),
    "W": (1, 5, 3, "water crew"),
    "J": (1, 3, 2, "court clerk"),
    "E": (2, 4, 2, "election custodian"),
}
SOURCES = {
    "clinic": (4, 12, "clinic site"),
    "water": (3, 12, "water site"),
    "hub": (3, 8, "shared hub"),
    "wider hub": (4, 8, "shared hub"),
    "court": (2, 4, "court site"),
    "election": (2, 4, "election site"),
}
# J source, E source, added capital, added annual net source.
PACKAGES = {
    "retain": ("hub", "hub", 0, 0),
    "widen": ("wider hub", "wider hub", 2, 1),
    "move E": ("hub", "election", 2, 1),
    "move J": ("court", "hub", 2, 2),
    "split": ("court", "election", 4, 3),
}
FAILURES = {
    "feeder": {"normal feeder"},
    "feeder and hub": {"normal feeder", "shared hub"},
}


def feasible(duties, package, unavailable, shared_clerk=False):
    court, election, _, _ = PACKAGES[package]
    assignments = {"C": "clinic", "W": "water", "J": court, "E": election}
    energy = Counter()
    power = Counter()
    staff = Counter()
    for duty in duties:
        start, end, load, worker = WINDOWS[duty]
        source = assignments[duty]
        if SOURCES[source][2] in unavailable:
            return False
        if shared_clerk and duty in ("J", "E"):
            worker = "shared clerk"
        energy[source] += (end - start) * load
        for hour in range(start, end):
            power[source, hour] += load
            staff[worker, hour] += 1
    return (
        all(total <= SOURCES[source][1] for source, total in energy.items())
        and all(load <= SOURCES[source][0] for (source, _), load in power.items())
        and all(count == 1 for count in staff.values())
    )


def complete_packages(capital, recurring, shared_clerk=False):
    return [
        package for package, (_, _, cost, annual) in PACKAGES.items()
        if cost <= capital and annual <= recurring
        and all(feasible(WINDOWS, package, outage, shared_clerk)
                for outage in FAILURES.values())
    ]


if __name__ == "__main__":
    # C and W have committed sources. List inclusion-maximal simultaneous
    # schedules without treating an omitted duty as released or lower priority.
    candidate_sets = [
        frozenset(("C", "W", *added))
        for count in range(3) for added in combinations("JE", count)
    ]
    expected = {
        "retain": ({"CWJ", "CWE"}, {"CW"}),
        "widen": ({"CWEJ"}, {"CW"}),
        "move E": ({"CWEJ"}, {"CWE"}),
        "move J": ({"CWEJ"}, {"CWJ"}),
        "split": ({"CWEJ"}, {"CWEJ"}),
    }
    for package in PACKAGES:
        outcomes = []
        for outage in FAILURES.values():
            possible = [duties for duties in candidate_sets
                        if feasible(duties, package, outage)]
            maximum = {''.join(duty for duty in "CWEJ" if duty in duties)
                       for duties in possible if not any(duties < other for other in possible)}
            outcomes.append(maximum)
        assert tuple(outcomes) == expected[package], (package, outcomes)
        print(package, *[" or ".join(sorted(maximum)) for maximum in outcomes])

    assert complete_packages(4, 3) == ["split"]
    assert complete_packages(4, 2) == []
    assert complete_packages(4, 3, shared_clerk=True) == []
    print("Complete paid route: split. Weak source or shared clerk: none.")
