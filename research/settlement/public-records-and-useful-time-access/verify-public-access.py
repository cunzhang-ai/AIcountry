"""Reconcile the official annual aggregates and the worked disclosure routes."""

import csv
from decimal import Decimal
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / '2026-11-public-records-and-useful-time-access'
with (edition / 'annual-source-extract.csv').open(encoding='utf-8', newline='') as source:
    rows = list(csv.DictReader(source))

expected = {
    '2024': (41, 83041, 81389, 58026, 3690, 19673, '71.29', '75.83'),
    '2025': (39, 94526, 93736, 76455, 4751, 12530, '81.56', '86.63'),
}
for year, (count, total, denominator, met, extended, late, strict_rate, reported_rate) in expected.items():
    cohort = [row for row in rows if row['Quarter'] == year]
    assert len(cohort) == len({row['Government body'] for row in cohort}) == count
    received = sum(int(row['Total requests received']) for row in cohort)
    on_hold = sum(int(row['Requests on-hold or lapsed']) for row in cohort)
    assert received == total and received - on_hold == denominator
    for label, expected_value in (
        ('Total requests received (excluding on-hold and lapsed)', denominator),
        ('20-day deadline met', met),
        ('Permitted extension to 20-day deadline', extended),
        ('Late response (i.e. 20-day deadline missed)', late),
    ):
        assert sum(int(row[label]) for row in cohort) == expected_value
    assert met + extended + late == denominator
    assert f'{Decimal(met) * 100 / denominator:.2f}' == strict_rate
    assert f'{Decimal(met + extended) * 100 / denominator:.2f}' == reported_rate
    print(f'{year}: {received} receipts; {strict_rate}% met the base deadline; {reported_rate}% in time including extensions.')


def released_by_hearing(
    funded_units: int, *, date_of_delivery: int, independent_original: bool,
    qualified_redaction: bool = True,
) -> tuple[bool, bool]:
    summary = funded_units >= 2 and date_of_delivery < 7
    underlying = (
        summary and funded_units >= 6 and independent_original and qualified_redaction
    )
    return summary, underlying


assert released_by_hearing(6, date_of_delivery=6, independent_original=True) == (True, True)
assert released_by_hearing(5, date_of_delivery=6, independent_original=True) == (True, False)
assert released_by_hearing(6, date_of_delivery=8, independent_original=True) == (False, False)
assert released_by_hearing(6, date_of_delivery=6, independent_original=False) == (True, False)
assert released_by_hearing(
    6, date_of_delivery=6, independent_original=True, qualified_redaction=False
) == (True, False)
print('By the hearing, the original needs funded independent retrieval and qualified protected release.')
