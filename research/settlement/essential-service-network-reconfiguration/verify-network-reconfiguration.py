"""Compare essential-service receipt and dated spending in the constructed case."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Window:
    independent_demand: int
    access_dependent_demand: int
    hub_places: int
    local_places: int
    accessible_round_trips: int
    cost: int

    @property
    def demand(self):
        return self.independent_demand + self.access_dependent_demand

    @property
    def receipt(self):
        independent = min(self.independent_demand, self.hub_places)
        local = min(self.access_dependent_demand, self.local_places)
        trips = min(
            self.access_dependent_demand - local,
            self.accessible_round_trips,
            self.hub_places - independent,
        )
        return independent + local + trips

    @property
    def protects_floor(self):
        return self.receipt == self.demand and self.cost <= 14


def with_standby(window, *, independent, timely):
    if independent and timely:
        return replace(window, local_places=window.local_places + 1)
    return window


def main():
    repair = (
        Window(0, 10, 0, 12, 0, 14),
        Window(0, 12, 0, 12, 0, 14),
    )
    hub = (
        Window(6, 4, 12, 0, 2, 11),
        Window(8, 4, 12, 0, 1, 10),
    )
    hybrid = (
        Window(6, 4, 8, 4, 0, 14),
        Window(8, 4, 8, 4, 0, 11),
    )

    assert all(window.protects_floor for window in repair + hybrid)
    assert [window.receipt for window in hub] == [8, 9]
    assert all(window.cost <= 14 and not window.protects_floor for window in hub)
    assert sum(window.cost for window in repair) - sum(window.cost for window in hybrid) == 3

    higher_local_need = Window(8, 5, 8, 4, 0, 11)
    higher_total_need = Window(0, 13, 0, 12, 0, 14)
    assert higher_local_need.receipt == higher_total_need.receipt == 12
    assert not higher_local_need.protects_floor
    assert not higher_total_need.protects_floor

    local_loss = Window(6, 4, 8, 3, 0, 14)
    assert local_loss.receipt == 9 and not local_loss.protects_floor
    # The first-window cost already includes paid standby and activation.
    restored = with_standby(local_loss, independent=True, timely=True)
    assert restored.protects_floor and restored.cost == local_loss.cost == 14
    assert not with_standby(local_loss, independent=False, timely=True).protects_floor
    assert not with_standby(local_loss, independent=True, timely=False).protects_floor
    print("Service networks: dated cost, access, increased demand and fallback passed.")


if __name__ == "__main__":
    main()
