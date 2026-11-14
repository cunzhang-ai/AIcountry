"""Verify the constructed programme on separate owned cash and qualified work axes."""

import json
from pathlib import Path

CASE = json.loads(Path(__file__).with_name("case.json").read_text())
VECTORS = ("national", "local", "work")
PACKAGES = CASE["packages"]


def requirements(package):
    measures = [CASE["measures"][name] for name in PACKAGES[package]]
    return {
        **{
            axis: tuple(sum(measure[axis][index] for measure in measures) for index in range(3))
            for axis in VECTORS
        },
        "foreign": sum(measure["foreign"] for measure in measures),
    }


def constraints(package, limits):
    needed = requirements(package)
    gaps = {
        axis: tuple(max(0, amount - available) for amount, available in zip(needed[axis], limits[axis]))
        for axis in VECTORS
    }
    return {**gaps, "foreign": max(0, needed["foreign"] - limits["foreign"])}


def release_conditions(package, limits, voted_packages, accepted_measures, received_advance):
    measures = set(PACKAGES[package])
    gaps = constraints(package, limits)
    housing_ready = all(
        advance + own >= due
        for advance, own, due in zip(
            received_advance, CASE["measures"]["H"]["local"], CASE["housing_local_gross_due"]
        )
    )
    return (
        package in voted_packages
        and measures <= accepted_measures
        and not any(any(gaps[axis]) for axis in VECTORS)
        and not gaps["foreign"]
        and ("H" not in measures or housing_ready)
    )


reference = CASE["paths"]["reference"]
weaker = CASE["paths"]["weaker"]
advance = CASE["housing_advance"]
accepted = {"E", "P", "H", "A"}
votes = {"repair", "reference", "weaker_housing", "weaker_preparation"}
no_gaps = {"national": (0, 0, 0), "local": (0, 0, 0), "work": (0, 0, 0), "foreign": 0}
assert requirements("reference") == {
    "national": (5, 9, 2), "local": (4, 8, 3), "work": (3, 2, 2), "foreign": 1
}
assert constraints("repair", weaker) == no_gaps
assert constraints("accelerated", reference) == {
    "national": (0, 0, 0), "local": (0, 1, 0), "work": (0, 1, 0), "foreign": 0
}
assert release_conditions("reference", reference, votes, accepted, advance)
assert not release_conditions("reference", weaker, votes, accepted, advance)
assert release_conditions("weaker_housing", weaker, votes, accepted, advance)
assert release_conditions("weaker_preparation", weaker, votes, accepted, advance)
assert not release_conditions("weaker_housing", weaker, {"reference"}, accepted, advance)
assert not release_conditions("weaker_housing", weaker, votes, accepted - {"H"}, advance)
assert not release_conditions("weaker_housing", weaker, votes, accepted, (0, 3, 2))
assert release_conditions("weaker_preparation", weaker, votes, accepted - {"H"}, (0, 0, 0))
assert not release_conditions("weaker_preparation", {**weaker, "foreign": 0}, votes, accepted, advance)
assert not release_conditions("weaker_housing", {**weaker, "work": [2, 1, 2]}, votes, accepted, advance)

housing = CASE["measures"]["H"]
assert housing["national"] == advance
assert tuple(national + own for national, own in zip(advance, housing["local"])) == tuple(
    CASE["housing_local_gross_due"]
)
recurring_national = reference["national"][2] - requirements("reference")["national"][2]
recurring_local = reference["local"][2] - requirements("reference")["local"][2]
assert (recurring_national, recurring_local) == (4, 2)

print("Integrated programme passed. Votes, early cash, local advance, foreign settlement and work remain distinct.")
