"""Check the stated evidence arithmetic, service windows and exit exposure."""

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Window:
    supply: int
    protected: int
    optional_power: int
    optional_water: int
    water_available_after_protection: int

    def qualifies(self) -> bool:
        return (
            self.protected + self.optional_power <= self.supply
            and self.optional_water <= self.water_available_after_protection
        )


def uncovered_exit_cost(committed_cost, realized_reuse, settled_security):
    return max(0, committed_cost - realized_reuse - settled_security)


edition = Path(__file__).resolve().parents[2] / '2026-11-large-grid-connections-and-paid-capacity'
observations = json.loads((edition / 'observations.json').read_text())['observations']
early, later = (record['amount'] for record in observations)
assert later - early == 84
assert round(100 * (later - early) / early) == 205

assert not Window(10, 6, 8, 2, 3).qualifies()
assert Window(10, 6, 4, 2, 3).qualifies()
assert not Window(14, 6, 8, 4, 3).qualifies()
assert Window(14, 6, 8, 3, 3).qualifies()
assert not Window(10, 6, 4 + 2, 3, 3).qualifies()
assert Window(12, 6, 4 + 2, 3, 3).qualifies()

assert uncovered_exit_cost(12, 3, 8) == 1
assert uncovered_exit_cost(7, 1, 6) == 0
assert uncovered_exit_cost(7, 1, 0) == 6
assert uncovered_exit_cost(7, 0, 6) == 1

print('Ofgem contracted offers rose by 84 GW, about 205% of the earlier queue measure.')
print('A four-unit firm phase fits. The eight-unit firm request does not fit the stressed window.')
print('Flexible use needs both a qualified water limit and headroom for recovery.')
print('The full build leaves one uncovered exit unit. The funded first stage can close its exposure.')
