"""Reproduce the reported scopes without treating annual balances as cash."""

import json
from pathlib import Path


research = Path(__file__).resolve().parents[2]
observations = json.loads(
    (research / '2026-11-copenhagen-care-and-water-budget' / 'observations.json').read_text()
)


def main():
    care = observations['health_and_care']
    variance = care['service_budget'] - care['service_expense']
    combined_pressure = care['home_care_overspend_rounded'] + care['nursing_overspend_rounded']
    assert variance == care['reported_service_underspend'] == 14789
    assert combined_pressure == 36700
    assert round((variance + combined_pressure) / 1000, 1) == 51.5
    assert care['requested_service_carryforward_march'] == 8788
    assert care['own_technical_service_carryforward_april_rounded'] == -100

    water = observations['water_company']
    sales = water['supply_area_sales'] + water['external_utility_sales']
    adjustment = water['regulatory_adjustments']
    assert sales + adjustment == water['annual_revenue'] == 865620
    assert round(100 * adjustment / water['annual_revenue'], 1) == 48.1
    assert water['annual_profit'] == 204201
    assert water['year_end_bank_deposits'] == 50
    assert water['customer_receivables_current'] + water['customer_receivables_noncurrent'] == 609240

    council = observations['council_2026']
    assert council['remaining_citywide_service_allowance_and_financing_rounded'] == 8700
    assert (council['dementia_package_service_rounded'], council['afforestation_service_rounded']) == (
        5800, 3000,
    )
    assert all(value is None for value in observations['joint_window'].values())
    print('Copenhagen care and water passed: observed arithmetic and unresolved joint release.')


if __name__ == '__main__':
    main()
