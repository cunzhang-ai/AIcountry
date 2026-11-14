"""Reconcile the authored capital sources, work windows and care access."""

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Portfolio:
    gross: int
    national: int
    dense_local: int
    remote_local: int
    recurring: int
    ordinary: tuple[int, int]
    road_closure: tuple[int, int]

    def fits_sources(self):
        assert self.gross == self.national + self.dense_local + self.remote_local
        return (
            self.gross <= 12
            and self.national <= 10
            and self.dense_local <= 2
            and self.remote_local <= 1
            and self.recurring <= 6
        )


def uncovered(received, required=(60, 20)):
    return tuple(max(0, need - actual) for actual, need in zip(received, required))


def crews_fit(schedule, available):
    reserved = Counter(schedule.values())
    return all(count <= available.get(window, 0) for window, count in reserved.items())


def main():
    current = Portfolio(0, 0, 0, 0, 0, (60, 12), (60, 12))
    dense = Portfolio(8, 6, 2, 0, 3, (90, 12), (90, 12))
    hub = Portfolio(10, 8, 1, 1, 5, (80, 20), (80, 15))
    phased = Portfolio(12, 10, 1, 1, 6, (68, 20), (68, 20))
    separate = Portfolio(13, 12, 0, 1, 5, (60, 26), (60, 26))

    assert all(p.fits_sources() for p in (current, dense, hub, phased))
    assert not separate.fits_sources()
    assert sum(dense.ordinary) == 102 and sum(phased.ordinary) == 88
    assert uncovered(dense.ordinary) == (0, 8)
    assert uncovered(hub.ordinary) == (0, 0)
    assert uncovered(hub.road_closure) == (0, 5)
    assert uncovered(phased.road_closure) == (0, 0)
    assert uncovered((68, 17)) == (0, 3)
    assert uncovered(phased.ordinary, (70, 20)) == (2, 0)

    remote_gross = 8
    dense_gross = 4
    assert remote_gross + dense_gross == phased.gross
    assert remote_gross // 4 == 2 > phased.remote_local
    assert (remote_gross - phased.remote_local) + (dense_gross - phased.dense_local) == phased.national

    available_crews = {"early": 1, "later": 1}
    phased_schedule = {"remote repair": "early", "dense repair": "later"}
    assert crews_fit(phased_schedule, available_crews)
    accelerated = dict(phased_schedule)
    accelerated["dense repair"] = "early"
    assert not crews_fit(accelerated, available_crews)

    print("Dense expansion reaches 102 total but leaves eight protected remote encounters unmet.")
    print("The hub meets ordinary duties, but road closure leaves five unmet.")
    print("The phased option protects both areas within 12 capital and six recurring units.")
    print("A uniform local match requires two remote units, against one lawfully available.")
    print("Losing local backup leaves three unmet. Higher dense demand leaves two unmet there.")


if __name__ == "__main__":
    main()
