"""Check published differences and the illustrative renewal and claim dates."""

from decimal import Decimal as D
import json
from pathlib import Path


def shortfall(due, received):
    return max(0, due - received)


def available_by(cutoff, receipts):
    return sum(amount for day, amount in receipts if day <= cutoff)


def cash_gap_for_two_claims(*, public_cash_day, public_cash):
    due = 12 + 12
    private_cash = available_by(5, ((4, 14), (7, 2)))
    timely_public_cash = available_by(5, ((public_cash_day, public_cash),))
    bounded_public_cash = min(10, timely_public_cash)
    return shortfall(due, private_cash + bounded_public_cash)


edition = Path(__file__).resolve().parents[2] / '2026-11-home-insurance-exit-and-safe-transition'
data = json.loads((edition / 'observations.json').read_text(), parse_float=D)
low = data['lowest_expected_climate_loss_zip_code_quintile']
high = data['highest_expected_climate_loss_zip_code_quintile']
premium_key = 'average_inflation_adjusted_premium_per_policy_usd'
relative_premium = 100 * (D(high[premium_key]) / D(low[premium_key]) - 1)
nonrenewal_points = high['nonrenewal_percent'] - low['nonrenewal_percent']
assert high[premium_key] - low[premium_key] == 1044
assert round(relative_premium) == 82
assert nonrenewal_points == D('0.71')

renewal_due = 8
available_for_premium = 5
assert shortfall(renewal_due, available_for_premium + available_by(10, ((9, 3),))) == 0
assert shortfall(renewal_due, available_for_premium + available_by(10, ((11, 3),))) == 3
assert shortfall(4, 1) == 3

assert cash_gap_for_two_claims(public_cash_day=5, public_cash=8) == 2
assert cash_gap_for_two_claims(public_cash_day=5, public_cash=10) == 0
assert cash_gap_for_two_claims(public_cash_day=6, public_cash=10) == 10

print(f'Observed premium difference: {relative_premium:.2f}%; nonrenewal difference: {nonrenewal_points} percentage points.')
print('The timely premium bridge closes renewal but leaves the deductible short by three.')
print('The public layer must settle ten by day five to close both illustrative claims.')
