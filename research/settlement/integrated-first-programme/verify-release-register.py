"""Apply the authored shared loss to the previous integrated budget."""

from pathlib import Path
from runpy import run_path


base = run_path(str(Path(__file__).with_name("verify-programme.py")))
case = base["CASE"]
requirements = base["requirements"]
base_release = base["release_conditions"]
reference = case["paths"]["reference"]
weaker = case["paths"]["weaker"]
reserve = {"national": (1, 1, 0), "local": (0, 1, 0), "foreign": 0, "work": (0, 1, 0)}


def needs_with_reserve(package):
    need = requirements(package)
    return {
        **{
            axis: tuple(amount + extra for amount, extra in zip(need[axis], reserve[axis]))
            for axis in ("national", "local", "work")
        },
        "foreign": need["foreign"] + reserve["foreign"],
    }


def shortages(package, limits):
    need = needs_with_reserve(package)
    return {
        **{
            axis: tuple(max(0, amount - limit) for amount, limit in zip(need[axis], limits[axis]))
            for axis in ("national", "local", "work")
        },
        "foreign": max(0, need["foreign"] - limits["foreign"]),
    }


def can_release(package, limits, votes, accepted_measures, reserve_ready, received_advance):
    remaining = {
        **{
            axis: tuple(limit - extra for limit, extra in zip(limits[axis], reserve[axis]))
            for axis in ("national", "local", "work")
        },
        "foreign": limits["foreign"] - reserve["foreign"],
    }
    return (
        "reserve" in votes
        and reserve_ready
        and base_release(package, remaining, votes, accepted_measures, received_advance)
    )


accepted = {"E", "P", "H"}
voted = {"reference", "weaker_housing", "weaker_preparation", "reserve"}
advance = case["housing_advance"]
assert needs_with_reserve("reference") == {
    "national": (6, 10, 2), "local": (4, 9, 3), "foreign": 1, "work": (3, 3, 2)
}
assert shortages("weaker_housing", weaker) == {
    "national": (1, 0, 0), "local": (0, 0, 0), "foreign": 0, "work": (0, 1, 0)
}
assert shortages("accelerated", reference) == {
    "national": (1, 1, 0), "local": (0, 2, 0), "foreign": 0, "work": (0, 2, 0)
}
assert can_release("reference", reference, voted, accepted, True, advance)
assert not can_release("reference", reference, voted, accepted, True, (0, 3, 2))
assert not can_release("reference", weaker, voted, accepted, True, advance)
assert not can_release("weaker_housing", weaker, voted, accepted, True, advance)
assert can_release("weaker_preparation", weaker, voted, accepted - {"H"}, True, (0, 0, 0))
assert not can_release("weaker_preparation", weaker, {"reference", "reserve"}, accepted, True, advance)
assert not can_release("weaker_preparation", weaker, voted - {"reserve"}, accepted, True, advance)
assert not can_release("weaker_preparation", weaker, voted, accepted, False, advance)
assert not can_release("weaker_preparation", weaker, voted, accepted - {"P"}, True, advance)

housing_due = case["housing_local_gross_due"]
housing_own = case["measures"]["H"]["local"]
advance_available = (0, 3, 2)
housing_payment_gap = tuple(
    max(0, due - own - available)
    for due, own, available in zip(housing_due, housing_own, advance_available)
)
assert housing_payment_gap == (2, 0, 0)

print("Release register passed. A priced independent reserve changes the weaker option, and later settlement leaves the original shortfall visible.")
