"""Reconcile the manually transcribed national columns of Tables 1, 1a and 1b."""

import csv
import json
from decimal import Decimal
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree
from zipfile import ZipFile


source = (
    Path(__file__).resolve().parents[2]
    / "2026-11-clinical-pathway-bottlenecks/original-sources/table-1-extract.csv"
)


def percent(value, total):
    return str((100 * Decimal(value) / total).quantize(Decimal("0.01")))


with source.open(newline="") as stream:
    counts = {
        row.pop("stage"): {key: int(value) for key, value in row.items()}
        for row in csv.DictReader(stream)
    }

diagnostic = counts["diagnostic_start"]
treatment = counts["treatment_start"]
combined = counts["all_reported_starts"]
assert combined == {key: diagnostic[key] + treatment[key] for key in combined}

result = {}
for stage, row in counts.items():
    compliant_late = sum(value for field, value in row.items() if field.startswith("late_"))
    total = row["total"]
    assert row["timely"] + compliant_late + row["noncompliant"] == total
    result[stage] = {
        "episodes": total,
        "timely_percent": percent(row["timely"], total),
        "legally_compliant_percent": percent(total - row["noncompliant"], total),
        "late_compliant_episodes": compliant_late,
        "late_compliant_capacity_percent_of_all_stage_episodes": percent(
            row["late_capacity_with_duty_met"], total
        ),
    }

assert result["all_reported_starts"]["timely_percent"] == "94.52"
assert result["all_reported_starts"]["legally_compliant_percent"] == "99.96"
assert result["diagnostic_start"]["timely_percent"] == "95.50"
assert result["treatment_start"]["timely_percent"] == "90.49"
def numeric_cells(book_path, sheet_name):
    with ZipFile(book_path) as book:
        workbook = ElementTree.fromstring(book.read("xl/workbook.xml"))
        sheet = next(node for node in workbook.findall(".//{*}sheet") if node.get("name") == sheet_name)
        rel_id = next(value for key, value in sheet.attrib.items() if key.endswith("}id"))
        relationships = ElementTree.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        target = next(node.get("Target") for node in relationships if node.get("Id") == rel_id)
        worksheet_path = target.lstrip("/") if target.startswith("/") else str(PurePosixPath("xl") / target)
        worksheet = ElementTree.fromstring(book.read(worksheet_path))
        return {
            node.get("r"): int(node.findtext("{*}v"))
            for node in worksheet.findall(".//{*}c")
            if node.get("t") in (None, "n") and (node.findtext("{*}v") or "").isdigit()
        }


pathways = {}
for pathway in ("B12", "B26"):
    denominator = numeric_cells(source.parent / "denmark-2026-q2-counts.xlsx", pathway)
    proportion = numeric_cells(source.parent / "denmark-2026-q2-proportions.xlsx", pathway)
    pathways[pathway] = {}
    for period, column in (("2025 Q2", "X"), ("2026 Q2", "AB")):
        pathways[pathway][period] = {}
        for region, shift in (("Zealand", 0), ("Denmark", 1)):
            pathways[pathway][period][region] = {
                stage: {
                    "episodes_as_published": denominator[f"{column}{row + shift}"],
                    "percent_as_published": proportion[f"{column}{row + shift}"],
                }
                for stage, row in (("OF1", 11), ("OF2A", 20), ("OF3A", 42), ("OF4A", 75))
            }

assert pathways["B26"]["2026 Q2"]["Zealand"]["OF1"] == {
    "episodes_as_published": 707,
    "percent_as_published": 37,
}
assert pathways["B12"]["2026 Q2"]["Zealand"]["OF3A"] == {
    "episodes_as_published": 78,
    "percent_as_published": 33,
}
print(json.dumps({"statutory_wait_report_2025_q4": result, "recommended_times": pathways}, indent=2))
