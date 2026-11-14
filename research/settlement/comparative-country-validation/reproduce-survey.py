"""Extract matching 2024 and 2025 survey cells from archived Eurostat responses."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUTS = ROOT / "2026-11-comparative-country-validation" / "original-sources"


def cell(data, **filters):
    offset = 0
    for name, size in zip(data["id"], data["size"], strict=True):
        codes = data["dimension"][name]["category"]["index"]
        code = filters.get(name)
        if code is None:
            assert size == 1, name
            code = next(iter(codes))
        offset = offset * size + codes[code]
    return {"value": data["value"].get(str(offset)), "status": data.get("status", {}).get(str(offset))}


population = json.loads((INPUTS / "hlth_silc_08.json").read_text())
conditional = json.loads((INPUTS / "hlth_silc_08b.json").read_text())
results = {}
for geo in ("DK", "FI"):
    results[geo] = {}
    for time in ("2024", "2025"):
        results[geo][time] = {
            "survey_population": {
                group: {
                    reason: cell(population, geo=geo, time=time, quant_inc=group, reason=reason)
                    for reason in ("TXP_TFAR_WLIST", "WLIST", "TXP", "TFAR")
                }
                for group in ("TOTAL", "QU1", "QU5")
            },
            "reports_need": {
                group: cell(conditional, geo=geo, time=time, rskpovth=group)
                for group in ("TOTAL", "B_60")
            },
        }
assert results["DK"]["2025"]["survey_population"]["QU1"]["TXP_TFAR_WLIST"]["value"] == 4.7
assert results["FI"]["2025"]["reports_need"]["B_60"]["value"] == 18.9


def score(qualified_slots, reachable):
    return min(qualified_slots, reachable)


assert score(4 + 2, 2 + 2) == 4
assert score(4, 2 + 4) == 4
assert score(4 + 1, 2 + 3) == 5
assert score(4 + 2, 2 + 4) == 6
assert (6 + 3, 2 + 2 * 3) == (9, 8)
assert (6 + 6, 2 + 2 * 6) == (12, 14)
assert 6 + 6 + 2 == 2 + 2 * 6

first_missing = {1, 2, 3}
same_people_missing = {1, 2, 3}
different_people_missing = {4, 5, 6}
assert len(first_missing & same_people_missing) == 3
assert len(first_missing & different_people_missing) == 0

print(json.dumps(results, indent=2))
