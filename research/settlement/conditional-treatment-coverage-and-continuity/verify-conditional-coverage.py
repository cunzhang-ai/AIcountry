"""Reproduce reported NHS activity and the illustrative two-window coverage test."""

from dataclasses import dataclass
from decimal import Decimal
import json
from pathlib import Path


@dataclass(frozen=True)
class Offer:
    starts: int
    early_cash: int
    later_cash: int
    qualified_start_slots: int
    accepted_later_slots: int

    def qualifies(self) -> bool:
        return (
            self.early_cash >= 2 + 3 * self.starts
            and self.later_cash >= 1 + 2 * self.starts
            and self.qualified_start_slots >= self.starts
            and self.accepted_later_slots >= self.starts
        )


edition = (
    Path(__file__).resolve().parents[2] / '2026-11-conditional-treatment-coverage-and-continuity'
)
data = json.loads((edition / 'observations.json').read_text())
interim = sum(data['interim_funding_notifications'])
managed = sum(data['managed_access_notifications'])
drug_cost = (
    Decimal(data['interim_funding_drug_cost_gbp_millions'])
    + Decimal(data['managed_access_drug_cost_gbp_millions'])
)
recommendation_share = (
    100 * Decimal(data['recommended_for_routine_commissioning_in_referred_population'])
    / data['reappraised_managed_access_treatments']
)
assert (interim, managed, interim + managed) == (1180, 2083, 3263)
assert drug_cost == Decimal('86.80')
assert f'{recommendation_share:.1f}' == '87.2'

assert Offer(2, 9, 5, 2, 2).qualifies()
assert not Offer(3, 9, 5, 3, 3).qualifies()
assert not Offer(2, 9, 4, 2, 2).qualifies()
assert not Offer(2, 9, 5, 2, 1).qualifies()
assert Offer(1, 9, 4, 2, 1).qualifies()

print(f'NHS data: {interim} interim and {managed} managed-access notifications, £{drug_cost}m reported drug cost.')
print(f'Of the reappraised group, {recommendation_share:.1f}% were recommended for routine commissioning.')
print('The two-person offer needs five later units and two accepted later slots as well as early cash.')
