"""Join the pinned 2025 original sources and compare explicit work scenarios."""

import json
from fractions import Fraction
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[2]
EDITION = RESEARCH / "2026-11-matched-national-work-and-first-budget"
ORIGINALS = EDITION / "original-sources"


def read(path):
    return json.loads(path.read_text(), parse_float=Fraction)


def source_cell(dataset, **selection):
    dimensions = dataset["dimension"]
    assert set(selection) == set(dimensions["id"]), selection
    offset = 0
    for axis in dimensions["id"]:
        indexes = dimensions[axis]["category"]["index"]
        offset = offset * len(indexes) + indexes[selection[axis]]
    value = dataset["value"][offset]
    if not isinstance(value, (int, Fraction)) or isinstance(value, bool):
        raise ValueError(f"Missing or unsupported source value for {selection}")
    return value


def labour_scope(data, metric, sector):
    return source_cell(data, SOCIO=metric, BRANCHE=sector,
                       ContentsCode="NABB69", Tid="2025")


def production_scope(data, metric, sector):
    return source_cell(data, TRANSAKT=metric, BRANCHE=sector, PRISENHED="V",
                       ContentsCode="NABP69", Tid="2025")


def split(total, government):
    assert 0 <= government <= total
    return {"total": total, "government": government, "non_government": total - government}


def million_hours(worked, paid_week, government_gain=0, other_gain=0):
    """Same tasks at a stipulated quality, in million reference-hour equivalents."""
    ratio = Fraction(paid_week, 37)
    remaining = {
        name: Fraction(worked[name], 1000) * (1 - ratio * (1 + gain))
        for name, gain in (("government", government_gain), ("non_government", other_gain))
    }
    remaining["signed_total"] = sum(remaining.values())
    return remaining


def calculate():
    labour = read(ORIGINALS / "NABB69-2025.json")["dataset"]
    production = read(ORIGINALS / "NABP69-2025.json")["dataset"]
    assert labour["updated"] == production["updated"]

    work = {}
    for name, code in (("all_hours_thousand", "EMPH_DC"),
                       ("employee_hours_thousand", "SALH_DC"),
                       ("employment_average", "EMPM_DC"),
                       ("employee_average", "SALM_DC")):
        work[name] = split(labour_scope(labour, code, "V"),
                           labour_scope(labour, code, "VMEMO"))
    work["other_hours_thousand"] = {
        scope: total - work["employee_hours_thousand"][scope]
        for scope, total in work["all_hours_thousand"].items()
    }
    compensation = split(production_scope(production, "D1D", "V"),
                         production_scope(production, "D1D", "VMEMO"))
    output = split(production_scope(production, "P1K", "V"),
                   production_scope(production, "P1K", "VMEMO"))
    gva = split(production_scope(production, "B1GD", "V"),
                production_scope(production, "B1GD", "VMEMO"))

    industries = set(labour["dimension"]["BRANCHE"]["category"]["index"]) - {"V", "VMEMO"}
    assert industries == set(production["dimension"]["BRANCHE"]["category"]["index"]) - {
        "V", "VMEMO"
    }
    assert len(industries) == 69
    leaf_hours_residual = (
        sum(labour_scope(labour, "SALH_DC", sector) for sector in industries)
        - work["employee_hours_thousand"]["total"]
    )
    leaf_compensation_residual = (
        sum(production_scope(production, "D1D", sector) for sector in industries)
        - compensation["total"]
    )
    published_fiscal = read(RESEARCH / "2026-11-observed-government-baseline/results.json")
    public_d1 = published_fiscal["official_general_government_million_dkk"]["compensation"]
    assert compensation["government"] == public_d1

    hours = work["employee_hours_thousand"]
    both_stage_gains = {str(week): Fraction(37, week) - 1 for week in (36, 32)}
    matched_gain = both_stage_gains["32"]
    non_government_gain = matched_gain * Fraction(hours["total"], hours["non_government"])
    no_gain_36 = million_hours(hours, 36)
    no_gain_32 = million_hours(hours, 32)
    matched = million_hours(hours, 32, matched_gain, matched_gain)
    concentrated = million_hours(hours, 32, other_gain=non_government_gain)
    assert no_gain_36["signed_total"] > 0 and no_gain_32["signed_total"] > no_gain_36["signed_total"]
    assert matched == million_hours(hours, 37)
    assert concentrated["signed_total"] == 0
    assert concentrated["government"] == no_gain_32["government"] > 0
    assert concentrated["non_government"] == -concentrated["government"]

    return {
        "source_release": labour["updated"],
        **work,
        "employee_compensation_million_DKK": compensation,
        "gross_output_million_DKK": output,
        "gross_value_added_million_DKK": gva,
        "industry_employee_hours_residual_thousand": leaf_hours_residual,
        "industry_compensation_residual_million_DKK": leaf_compensation_residual,
        "matched_gain_fraction": both_stage_gains,
        "32_non_government_only_gain_fraction": non_government_gain,
        "signed_shortfalls_million_reference_hours": {
            "retain": million_hours(hours, 37),
            "36_no_gain": no_gain_36,
            "32_no_gain": no_gain_32,
            "32_matched_gain": matched,
            "32_concentrated_gain": concentrated,
        },
        "actual_qualified_staffing_cost_and_source": None,
        "actual_legal_authority_and_service_outcomes": None,
    }


def encode(value):
    if isinstance(value, Fraction):
        return {"exact_fraction": str(value), "decimal": float(value)}
    raise TypeError(type(value).__name__)


if __name__ == "__main__":
    print(json.dumps(calculate(), default=encode, indent=2))
