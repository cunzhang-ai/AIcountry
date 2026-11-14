"""Reproduce funding boundaries and the authored water receipt exercise."""

from datetime import date
import json
from pathlib import Path


research = Path(__file__).resolve().parents[2]
observations = json.loads(
    (research / '2026-11-copenhagen-emergency-reserve' / 'observations.json').read_text()
)
BASIC_DELIVERIES = {42: (0, 1), 60: (2, 1)}
EXTENSION = {80: (1, 1)}


def shortages(deliveries, restoration_hour):
    stock = [4, 1]
    missed = {}
    previous_deadline = 0
    for deadline, need in ((24, (2, 1)), (48, (2, 1)), (72, (2, 1)), (84, (1, 1))):
        if restoration_hour < deadline:
            break
        for hour, quantities in deliveries.items():
            if previous_deadline < hour <= deadline:
                stock = [available + delivered for available, delivered in zip(stock, quantities)]
        missed[deadline] = tuple(max(0, required - available) for required, available in zip(need, stock))
        stock = [max(0, available - required) for available, required in zip(stock, need)]
        previous_deadline = deadline
    return missed


def main():
    regional = observations['regional_preparedness']
    assert regional['april_improvements_conditional'] + regional['april_exercises_conditional'] == 35000
    assert regional['september_revised_owner_total'] - regional['april_improvements_conditional'] == 5870
    assert regional['september_revised_owner_total'] - regional['september_copenhagen_appropriation'] == 11540
    assert regional['september_copenhagen_appropriation'] + regional['september_older_people_share'] == (
        regional['september_copenhagen_grant_reported_received']
    )

    agreement = observations['published_budget_agreement']
    assert agreement['capital_2026_through_2029'] == 44400
    assert sum(agreement['organization_service_2027_through_2030']) == 31500
    assert round(regional['september_older_people_share'] / 1000, 1) == (
        agreement['older_people_state_financing_2026_rounded'] / 1000
    )
    agenda = observations['water_agenda']
    assert date.fromisoformat(agenda['assessment']) < date.fromisoformat(agenda['meeting'])
    assert agenda['proposed_restoration_days'] * 24 == 72
    assert all(value is None for value in observations['unverified_in_inspected_records'].values())

    assert shortages(BASIC_DELIVERIES, 72) == {24: (0, 0), 48: (0, 0), 72: (0, 0)}
    assert 84 not in shortages(BASIC_DELIVERIES, 83)
    assert shortages(BASIC_DELIVERIES, 90)[84] == (1, 1)
    assert all(loss == (0, 0) for loss in shortages(BASIC_DELIVERIES | EXTENSION, 90).values())
    delayed = shortages({42: BASIC_DELIVERIES[42]} | EXTENSION, 90)
    assert (delayed[72], delayed[84]) == ((2, 1), (0, 0))
    print('Copenhagen reserve passed: public allocations and the authored restoration gap.')


if __name__ == '__main__':
    main()
