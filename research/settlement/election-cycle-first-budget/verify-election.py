"""Reconcile published Danish rows and test a separate authored funding calendar."""

from datetime import date
from html import unescape
import json
from pathlib import Path
import re


def numeric_rows(path, anchor):
    content = path.read_text()
    start = content.index(anchor)
    table = content[start:content.index("</table>", start)]
    rows = re.findall(r"<tr\b[^>]*>(.*?)</tr>", table, re.S)
    amounts = []
    for row in rows[1:]:
        cells = re.findall(r"<td\b[^>]*>(.*?)</td>", row, re.S)
        amounts.append(int(unescape(re.sub(r"<[^>]+>", "", cells[-1])).strip().replace(".", "")))
    return amounts


def published_accounts():
    archive = Path(__file__).resolve().parents[2] / "2026-11-election-cycle-and-first-budget"
    observed = json.loads((archive / "observations.json").read_text())
    dates = {name: date.fromisoformat(value) for name, value in observed["dates"].items()}
    assert (dates["poll"] - dates["call"]).days == 26
    assert (dates["council_transfer"] - dates["poll"]).days == 37
    assert (dates["ordinary_benefit_schedule"] - dates["poll"]).days == 7
    assert dates["ordinary_benefit_schedule"].weekday() == 1
    estimate = observed["election_estimate_dkk_thousands_2026_price_and_wages"]
    assert sum(estimate.values()) == observed["published_total_dkk_thousands"] == 34951
    originals = archive / "original-sources"
    council = originals / "copenhagen-council-transfer.html"
    assert numeric_rows(council, "Tabel 1. Serviceudgifter") == [
        *estimate.values(), observed["published_total_dkk_thousands"]
    ]
    transfer = observed["internal_transfer_dkk_thousands"]
    assert transfer["culture_and_leisure"] == observed["published_total_dkk_thousands"]
    assert sum(transfer.values()) == 0
    second_table = council.read_text().split("1109", 1)[1].split("</table>", 1)[0]
    assert re.findall(r">(-?34\.951)<", second_table) == ["-34.951", "34.951"]
    care = observed["care_2025_dkk_thousands"]
    assert care["corrected_service_frame"] - care["actual_service_expense"] == 14789
    assert care["reported_home_care_overspend_rounded"] == 18500
    care_source = unescape((originals / "copenhagen-2025-care-accounts.html").read_text())
    for amount in ("5.739.793", "5.725.004", "14.789", "hjemmeplejen på 18,5 mio. kr."):
        assert amount in care_source
    call_source = (originals / "danish-election-call.html").read_text()
    assert "26.02.2026" in call_source and "24. marts 2026" in call_source
    print("Copenhagen: 26 days from call to poll and 37 days to the later council transfer.")
    print("The DKK 34.951m internal transfer consolidates to zero; 2025 care scopes stay separate.")


def due_shortfalls(cash_by_date, needs_by_date):
    return tuple(max(0, due - cash) for cash, due in zip(cash_by_date, needs_by_date, strict=True))


def authored_case():
    election_needs = (2, 5, 10, 12)
    discretionary = (2, 2, 2, 2)
    protected = (2, 5, 10, 12)
    assert due_shortfalls(discretionary, election_needs) == (0, 3, 8, 10)
    assert due_shortfalls(protected, election_needs) == (0, 0, 0, 0)

    ordinary_needs = {"care": 4, "justice": 2, "household": 5}
    ordinary_sources = dict(ordinary_needs)
    assert sum(ordinary_sources.values()) + protected[-1] == 23
    shared_cash_after_displacing_own_care_source = protected[-1] - ordinary_needs["care"]
    assert election_needs[-1] - shared_cash_after_displacing_own_care_source == 4

    available_technical_shifts = 4
    protected_shifts = {"election": 2, "household": 2}
    elective_migration_shifts = 2
    assert sum(protected_shifts.values()) == available_technical_shifts
    assert sum(protected_shifts.values()) + elective_migration_shifts - available_technical_shifts == 2

    spent = election_needs[-1]
    repeat_required = 3
    assert repeat_required - (protected[-1] - spent) == 3
    print("An unsigned transfer leaves early gaps of 3, 8 and 10; protected dated tranches fit.")
    print("Double-counted care cash leaves a gap of 4. The optional migration lacks two shifts.")
    print("An exhausted first cap leaves all three repeat-poll units to qualify separately.")


if __name__ == "__main__":
    published_accounts()
    authored_case()
