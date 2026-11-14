"""Check the scoped chronology and authored package choices."""

from datetime import date
import json
from pathlib import Path


observed = json.loads(
    (Path(__file__).resolve().parents[2]
     / "2026-11-first-budget-package-and-lawful-start" / "observations.json").read_text()
)["dutch_commencement"]
milestones = tuple(
    date.fromisoformat(observed[key])
    for key in (
        "senate_assent_date", "decree_date", "related_instruments_decree_date",
        "effective_date", "alternate_publication_decree_date",
        "stated_end_of_specified_alternate_publication_scope",
    )
)
assert all(earlier < later for earlier, later in zip(milestones, milestones[1:]))
assert observed["actual_access_and_outcome"] is None
print("Observed: statutory start, continuing prior cases and a later technical fallback.")

uses = {
    "baseline": (7, 12, 6, 3),
    "intake": (1, 2, 0, 1),
    "award": (2, 3, 1, 1),
    "remedy_overlap": (1, 2, 1, 1),
}
limits = (10, 18, 8, 5)
coupled = frozenset(("award", "remedy_overlap"))


def total(*components):
    return tuple(sum(use) for use in zip(*(uses[name] for name in components), strict=True))


def fits(*components):
    return all(used <= available for used, available in zip(total(*components), limits, strict=True))


def prospective_group_authorized(assents, receiver_ready):
    return coupled <= assents and receiver_ready and fits("baseline", *coupled)


assert total("baseline", "intake") == (8, 14, 6, 4)
assert total("baseline", *coupled) == (10, 17, 8, 5)
assert total("baseline", "intake", *coupled) == (11, 19, 8, 6)
assert fits("baseline", "intake") and not fits("baseline", "intake", *coupled)
assert fits("baseline", "award")
assert not prospective_group_authorized({"award"}, True)
assert not prospective_group_authorized(coupled, False)
assert prospective_group_authorized(coupled, True)

# A failed ordinary receiver prevents a guarded act, while already-due
# entitlement and its original clock retain independent legal effect.
already_due = True
receiver_after_start = False
allowed_verification = already_due and receiver_after_start
unmet_remedy = already_due and not receiver_after_start
assert already_due and not allowed_verification and unmet_remedy
print("Authored: the whole group fits the four limits; adding intake fails cash and slots.")
print("Partial assent cannot start the optional group; already-due rights survive failure.")
