"""Check declared dependencies and actions in the constructed case."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Use:
    controlling_family: str | None
    material_scope_confirmed: bool
    already_due: bool = False
    threshold: int | None = None


def disposition(use, corrected_family, new_value):
    if use.already_due:
        return "continue due payment"
    if not use.material_scope_confirmed:
        return "trace unresolved use"
    if use.controlling_family != corrected_family:
        return "retain independently supported action"
    if use.threshold is not None and new_value < use.threshold:
        return "hold optional release"
    return "reassess remaining conditions"


def main():
    summaries = {"English analysis": "register", "translated analysis": "register"}
    assert set(summaries.values()) == {"register"}
    corrected_count = 120 - 30
    assert corrected_count == 90
    extra_vehicle = Use("register", True, threshold=100)
    access_repair = Use("site audit", True)
    earned_pay = Use("verified work", True, already_due=True)
    neighbor = Use(None, False)

    assert disposition(extra_vehicle, "register", 120) == "reassess remaining conditions"
    assert disposition(extra_vehicle, "register", corrected_count) == "hold optional release"
    assert disposition(access_repair, "register", corrected_count) == "retain independently supported action"
    assert disposition(earned_pay, "register", corrected_count) == "continue due payment"
    assert disposition(neighbor, "register", corrected_count) == "trace unresolved use"
    print("Scoped correction: shared source, independent support, due claims and unknown use passed.")


if __name__ == "__main__":
    main()
