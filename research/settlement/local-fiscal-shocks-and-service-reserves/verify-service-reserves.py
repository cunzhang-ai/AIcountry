"""Reproduce the matched dates and the illustrative two-window reserve test."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
import json
from pathlib import Path


@dataclass(frozen=True)
class Package:
    name: str
    cost: int
    eligible: bool = True
    available: bool = True


def qualify_in_priority_order(packages, settled_cash):
    funded = []
    missing = []
    for package in packages:
        if not package.eligible:
            continue
        if package.available and package.cost <= settled_cash:
            funded.append(package.name)
            settled_cash -= package.cost
        else:
            missing.append(package.name)
    return funded, missing, settled_cash


edition = Path(__file__).resolve().parents[2] / '2026-11-local-fiscal-shocks-and-service-reserves'
inputs = json.loads((edition / 'observations.json').read_text(), parse_float=Decimal)
assert sum(row['reported_amount_millions'] for row in inputs['historical_advances']) == Decimal('283.1')

payment = inputs['alberta_2020_21']
delay = (
    date.fromisoformat(payment['federal_listed_payment_date'])
    - date.fromisoformat(payment['claim_year_end'])
).days
forecast_shortfalls = [
    forecast['amount_millions'] * 1_000_000 - payment['federal_listed_amount']
    for forecast in payment['provincial_forecasts']
]
assert delay == 736
assert forecast_shortfalls == [173_488_689, 130_488_689]

higher_priority = Package('A', 4)
other_call = Package('B', 4)
own_policy_loss = Package('discretionary tax reduction', 1, eligible=False)
early_calls = (higher_priority, other_call, own_policy_loss)
assert 6 // 2 < higher_priority.cost == other_call.cost


def early_cash(supplement_day: int) -> int:
    receipts = ((1, 6), (supplement_day, 2))
    return sum(amount for day, amount in receipts if day <= 2)


assert qualify_in_priority_order(early_calls, early_cash(3)) == (['A'], ['B'], 2)
assert qualify_in_priority_order(early_calls, early_cash(2)) == (['A', 'B'], [], 0)
assert qualify_in_priority_order(
    (higher_priority, Package('B', 4, available=False)), 8
) == (['A'], ['B'], 4)

next_calls = (Package('next', 3),)
assert qualify_in_priority_order(next_calls, 3) == (['next'], [], 0)
assert qualify_in_priority_order(next_calls, 2) == ([], ['next'], 2)

print(f'Listed Alberta payment was {delay} days after claim-year end.')
print(f'Forecast less listed payment, CAD: {forecast_shortfalls}.')
print('Six early units support one complete package; eight can support both.')
print('The next service needs three settled units and fails with only two.')
