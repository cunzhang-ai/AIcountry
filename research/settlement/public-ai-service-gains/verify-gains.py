"""Reproduce the authored service, work and fallback comparison."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    routine: int
    checking: int
    independent: int
    training_and_fallback: int
    resident_active: int
    non_labor: int
    timely: int
    assisted: int
    urgent: int

    @property
    def paid_hours(self):
        return self.routine + self.checking + self.independent + self.training_and_fallback

    def meets_selected_limits(self, simpler):
        return (
            self.non_labor <= 3
            and self.urgent == 12
            and self.assisted >= simpler.assisted
            and self.timely >= simpler.timely
            and self.resident_active <= simpler.resident_active
        )


def main():
    retained = Route(90, 8, 10, 8, 50, 0, 86, 16, 12)
    simpler = Route(82, 7, 9, 8, 44, 1, 92, 18, 12)
    broad = Route(62, 19, 14, 15, 60, 6, 94, 14, 11)
    bounded = Route(68, 10, 9, 11, 40, 3, 96, 19, 12)

    for route in (retained, simpler, broad, bounded):
        assert 0 <= route.urgent <= 12
        assert 0 <= route.assisted <= 20
        assert max(route.urgent, route.assisted) <= route.timely <= 100

    assert tuple(route.paid_hours for route in (retained, simpler, broad, bounded)) == (
        116, 106, 110, 98
    )
    assert simpler.routine - broad.routine == 20
    assert broad.paid_hours - simpler.paid_hours == 4
    assert broad.resident_active - simpler.resident_active == 16
    assert broad.timely > simpler.timely
    assert not broad.meets_selected_limits(simpler)
    assert bounded.meets_selected_limits(simpler) and simpler.meets_selected_limits(simpler)
    assert bounded.independent == simpler.independent

    available = simpler.paid_hours - bounded.paid_hours
    additional_assisted_hours = 6
    additional_correction_hours = 2
    assert available == additional_assisted_hours + additional_correction_hours == 8
    assert bounded.non_labor - simpler.non_labor == 2

    ordinary_urgent = 9
    independent_fallback = 3
    assert ordinary_urgent + independent_fallback == 12
    assert ordinary_urgent == 9 and 12 - ordinary_urgent == 3

    print("Broad AI saves 20 routine hours, adds four paid hours and adds 16 resident hours.")
    print("Broad timely count grows from 92 to 94, but assisted receipt falls to 14 and one urgent duty is missed.")
    print("Bounded assistance uses eight fewer paid hours and two additional non-labor units.")
    print("Six hours go to assisted work and two to correction or training. No salary saving is booked.")
    print("Independent fallback supplies 12 urgent slots; a shared-root failure supplies only nine.")


if __name__ == "__main__":
    main()
