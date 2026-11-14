"""Check Design289's authored care roster, dated cash and concurrent calls."""

from dataclasses import dataclass, replace
from itertools import combinations


BASE_COST = 6
HOLD_COST = 1
ACTIVATION_COST = 2
LAST_USEFUL_ARRIVAL = 3
PROTECTED = frozenset(('A', 'B'))


@dataclass(frozen=True)
class Reserve:
    worker: str
    reachable: frozenset
    arrival: int = 2
    accepted: bool = True


def assess(calls, reserves, usable_cash):
    ordinary = BASE_COST + HOLD_COST * len(reserves)
    assert ordinary <= usable_cash
    offers = [
        (reserve.worker, resident)
        for reserve in reserves
        if reserve.accepted and reserve.worker not in PROTECTED
        and reserve.arrival <= LAST_USEFUL_ARRIVAL
        for resident in sorted(reserve.reachable & calls)
    ]
    for slots in range(len(calls), 0, -1):
        cost = ordinary + slots * ACTIVATION_COST
        if cost > usable_cash:
            continue
        for assignment in combinations(offers, slots):
            workers, residents = map(set, zip(*assignment))
            if len(workers) == slots and len(residents) == slots:
                return cost, calls - residents
    return ordinary, calls


def main():
    both = frozenset(('C', 'D'))
    one = frozenset(('C',))
    first = Reserve('first', both)
    second = Reserve('second', one)

    assert assess(both, (), 6) == (6, both)
    assert assess(both, (first,), 9) == (9, {'D'})
    assert assess(frozenset(), (first, second), 12) == (8, set())
    assert assess(one, (first, second), 12) == (10, set())
    assert assess(both, (first, second), 12) == (12, set())
    assert len(assess(both, (first, second), 10)[1]) == 1
    assert assess(both, (first, replace(second, worker='first')), 12) == (10, {'D'})
    assert assess(both, (first, replace(second, worker='B')), 12) == (10, {'D'})
    assert assess(both, (first, replace(second, arrival=4)), 12) == (10, {'D'})
    assert assess(both, (first, replace(second, accepted=False)), 12) == (10, {'D'})
    assert BASE_COST + 2 * 3 == 12
    print('Care comparison passed: actual reserve, dated cash, joint calls and protected respite.')


if __name__ == '__main__':
    main()
