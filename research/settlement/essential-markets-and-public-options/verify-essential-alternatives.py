"""Check the constructed continuity routes and scope of a durable source."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    startup_cost: int
    recurring_cost: int
    first_slots: int
    second_slots: int

    def qualifies(self, startup_funds, recurring_funds):
        return (
            self.startup_cost <= startup_funds
            and self.recurring_cost <= recurring_funds
            and min(self.first_slots, self.second_slots) >= 2
        )


same_broker = Route(0, 1, 1, 1)
cooperative = Route(1, 2, 2, 2)
cooperative_origin_conflict = Route(1, 2, 2, 1)
direct = Route(2, 3, 2, 2)

assert not same_broker.qualifies(2, 3)
assert cooperative.qualifies(2, 3)
assert not cooperative_origin_conflict.qualifies(2, 3)
assert direct.qualifies(2, 3)
assert not direct.qualifies(1, 3)
assert not direct.qualifies(2, 2)

# Lower price cannot replace a missed call. In the healthy branch a cheaper
# independent route qualifies alongside the directly staffed public offer.
assert cooperative.recurring_cost < direct.recurring_cost

# A transaction filing test is distinct from the qualified operator test.
assert sum((180, 170, 140)) < 500
assert sum((180, 170, 165)) >= 500
def gateway_filing(routes, observed_months, funded_alternate, effective_at_binding):
    return 1 <= routes <= 2 and observed_months >= 12 and not funded_alternate and effective_at_binding


assert gateway_filing(2, 12, False, True)
assert not gateway_filing(2, 12, False, False)
assert not gateway_filing(2, 12, True, True)
assert not gateway_filing(3, 12, False, True)

print("Genuinely independent cover costs less. Concurrent origin loss changes the qualified option.")
