"""Check cumulative and ordinary filing triggers in the constructed case."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class PriorTarget:
    business: str
    month: int
    turnover_in_t: int
    overlaps: bool = True
    controlled_or_bound: bool = True
    after_commencement: bool = True


def qualifying_turnover(history, current_month):
    targets = {}
    for item in history:
        if (
            current_month - 36 <= item.month <= current_month
            and item.overlaps
            and item.controlled_or_bound
            and item.after_commencement
        ):
            # These test records repeat a business only with the same basis.
            if item.business in targets:
                assert targets[item.business] == item.turnover_in_t
            targets[item.business] = item.turnover_in_t
    return sum(targets.values()), len(targets)


def ordinary_filing(group_turnover, target_turnover):
    return group_turnover >= 10_000 and target_turnover >= 500


def series_filing(group_turnover, current, earlier_targets):
    history = [item for item in earlier_targets if item.business != current.business]
    earlier_turnover, count = qualifying_turnover(history, current.month)
    return (
        current.after_commencement
        and group_turnover >= 10_000
        and count > 0
        and current.turnover_in_t + earlier_turnover >= 500
    )


def main():
    first = PriorTarget("First", 0, 180)
    second = PriorTarget("Second", 12, 170)
    third = PriorTarget("Third", 24, 165)
    group = 10_200

    assert not any(ordinary_filing(group, target.turnover_in_t) for target in (first, second, third))
    assert not series_filing(group, first, [])
    assert not series_filing(group, second, [first])
    assert series_filing(group, third, [first, second])
    assert series_filing(group, third, [first, first, second])
    assert not series_filing(group, third, [first, first])

    for changed_first in (
        replace(first, controlled_or_bound=False),
        replace(first, month=-13),
        replace(first, overlaps=False),
        replace(first, after_commencement=False),
    ):
        assert not series_filing(group, third, [changed_first, second])

    assert series_filing(group, third, [replace(first, month=-12), second])
    assert not series_filing(9_999, third, [first, second])
    assert series_filing(10_000, replace(third, turnover_in_t=150), [first, second])
    simultaneous = [replace(first, month=24), replace(second, month=24), third]
    assert all(series_filing(group, target, simultaneous) for target in simultaneous)
    print("Successive acquisitions: cumulative gate, finite scope and simultaneous commitments passed.")


if __name__ == "__main__":
    main()
