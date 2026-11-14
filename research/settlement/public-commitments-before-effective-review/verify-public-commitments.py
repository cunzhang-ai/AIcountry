"""Check the working-day and execution rules in the constructed lease case."""

WAIT_WORKING_DAYS = 10
STANDING_ALLOCATION = 5
PREPARATION_ALLOCATION = 2


def first_release_day(usable_notice, *, sector_wait_through=0, court_hold_through=0):
    if usable_notice is None:
        return None
    return max(
        usable_notice + WAIT_WORKING_DAYS,
        sector_wait_through,
        court_hold_through,
    ) + 1


def covered_release_allowed(day, first_day, *, authorized):
    return authorized and first_day is not None and day >= first_day


def preparation_allowed(cost, *, reversible, exclusive_control):
    return cost <= PREPARATION_ALLOCATION and reversible and not exclusive_control


def executed_hold(*, primary_received, alternate_received, transfer_occurred):
    return (primary_received or alternate_received) and not transfer_occurred


def standing_shortfall(*, due, settled):
    return due - min(settled, STANDING_ALLOCATION)


def main():
    base = first_release_day(3)
    assert base == 14
    assert not covered_release_allowed(14, first_release_day(None), authorized=True)
    assert first_release_day(3, sector_wait_through=15) == 16
    assert first_release_day(8) == 19
    assert not covered_release_allowed(6, base, authorized=True)
    assert not covered_release_allowed(14, base, authorized=False)
    assert covered_release_allowed(14, base, authorized=True)

    order = first_release_day(3, court_hold_through=17)
    assert order == 18
    assert not covered_release_allowed(14, order, authorized=True)
    assert executed_hold(
        primary_received=False, alternate_received=True, transfer_occurred=False
    )
    assert not executed_hold(
        primary_received=False, alternate_received=False, transfer_occurred=True
    )
    assert not executed_hold(
        primary_received=True, alternate_received=False, transfer_occurred=True
    )

    assert preparation_allowed(2, reversible=True, exclusive_control=False)
    assert not preparation_allowed(4, reversible=False, exclusive_control=True)
    assert not preparation_allowed(2, reversible=True, exclusive_control=True)
    assert standing_shortfall(due=5, settled=5) == 0
    assert standing_shortfall(due=5, settled=0) == 5
    print("Public commitments: usable notice, parallel clocks, actual hold and paid duties passed.")


if __name__ == "__main__":
    main()
