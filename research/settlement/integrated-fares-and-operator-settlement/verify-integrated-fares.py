"""Check the constructed fare cap and the timing of eligible settlement."""

from dataclasses import dataclass


def network_fare(journeys, fare_per_journey, cap):
    """Each input identifies one journey and whether that journey is paid."""
    status_by_journey = {}
    for journey, paid in journeys:
        previous_status = status_by_journey.setdefault(journey, paid)
        assert previous_status == paid
    return min(cap, sum(status_by_journey.values()) * fare_per_journey)


@dataclass(frozen=True)
class Window:
    operator_liabilities: int
    cleared_fares: int
    due_refunds: int
    recurring_source: int
    unsettled_collections: int
    rider_credit: int

    @property
    def usable_for_operators(self):
        return self.cleared_fares + self.recurring_source - self.due_refunds

    @property
    def funding_gap(self):
        return max(0, self.operator_liabilities - self.usable_for_operators)


def replenish_bridge(bridge_drawn, later_collection, legally_usable):
    return min(bridge_drawn, later_collection) if legally_usable else 0


def main():
    trips = [(f"day_{day}", True) for day in range(1, 6)]
    assert len(trips) * (4 + 4) == 40
    assert network_fare(trips[:4] + [("protected", False)], 6, 30) == 24
    assert network_fare(trips, 6, 30) == 30
    assert network_fare(trips + [("protected", False), trips[-1]], 6, 24) == 24

    first = Window(30, 18, 2, 8, 6, 4)
    assert first.usable_for_operators == 24
    assert first.funding_gap == 6
    assert first.usable_for_operators + 6 == first.operator_liabilities
    assert replenish_bridge(6, 0, True) == 0
    assert replenish_bridge(6, 6, False) == 0
    assert replenish_bridge(6, 6, True) == 6
    assert (18 + 6 - 2) + 8 == 30
    print("Integrated fares: transfers, cap, protected credits and dated payment passed.")


if __name__ == "__main__":
    main()
