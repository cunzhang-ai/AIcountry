"""Compare observed access measures and an illustrative paired capacity budget."""

from decimal import Decimal
import json
from math import prod
from pathlib import Path


RESEARCH = Path(__file__).resolve().parents[2]
EDITION = RESEARCH / "2026-11-health-access-bottlenecks-and-first-budget"
FISCAL_BASELINE = RESEARCH / "2026-11-matched-fiscal-baselines-and-budget-choice/results.json"
REASONS = ("TXP_TFAR_WLIST", "WLIST", "TXP", "TFAR")


def survey_cell(dataset, country, group, reason):
    codes = {
        "freq": "A", "unit": "PC", "quant_inc": group, "reason": reason,
        "age": "Y_GE16", "sex": "T", "geo": country, "time": "2024",
    }
    offset = str(sum(
        dataset["dimension"][axis]["category"]["index"][codes[axis]]
        * prod(dataset["size"][index + 1:])
        for index, axis in enumerate(dataset["id"])
    ))
    return {
        "value": dataset["value"].get(offset),
        "status": dataset.get("status", {}).get(offset),
    }


def compare():
    survey = json.loads((EDITION / "original-sources/hlth_silc_08.json").read_text(), parse_float=Decimal)
    fiscal = json.loads(FISCAL_BASELINE.read_text())
    assert fiscal["year"] == 2024
    countries = {}
    for country in ("DK", "FI"):
        observations = {
            group: {reason: survey_cell(survey, country, group, reason) for reason in REASONS}
            for group in ("TOTAL", "QU1", "QU5")
        }
        low_wait = observations["QU1"]["WLIST"]["value"]
        high_wait = observations["QU5"]["WLIST"]["value"]
        assert low_wait is not None and high_wait is not None
        countries[country] = {
            "health_function_expenditure_percent_of_GDP": fiscal["countries"][country]["cofog_functions"]["GF07"],
            "survey_percent_of_population_group": observations,
            "waiting_gap_low_minus_high_percentage_points": low_wait - high_wait,
        }
    return {"year": 2024, "countries": countries}


def possible_completions(assessments, accepted_treatments):
    return min(assessments, accepted_treatments)


if __name__ == "__main__":
    observed = compare()
    assert observed["countries"]["DK"]["waiting_gap_low_minus_high_percentage_points"] == Decimal("1.7")
    assert observed["countries"]["FI"]["waiting_gap_low_minus_high_percentage_points"] == Decimal("7.6")
    assert possible_completions(8, 1) == 1
    assert possible_completions(4, 1 + 3) == 4
    assert possible_completions(4, 1 + 2) == 3
    print(json.dumps(observed, indent=2, default=str))
