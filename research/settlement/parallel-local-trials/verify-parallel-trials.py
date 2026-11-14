"""Check the declared budgets, windows and independent trial authorities."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Option:
    name: str
    water: tuple[int, int]
    cost: int
    permits: frozenset[str]
    restoration: bool = False


def ready(option, available, cash, approved, permits, *, restored=True):
    return (
        option.name in approved
        and option.permits <= permits
        and cash >= option.cost
        and (not option.restoration or restored)
        and all(
            use == 0 or (quantity is not None and use <= quantity)
            for use, quantity in zip(option.water, available)
        )
    )


def main():
    original = Option('A and B', (7, 0), 5, frozenset(('A', 'B')))
    narrow = Option('narrow A and B', (6, 0), 4, frozenset(('narrow A', 'B')))
    sequence = Option('A then B', (3, 4), 5, frozenset(('A', 'B')), restoration=True)
    a = Option('A only', (3, 0), 2, frozenset(('A',)))
    b = Option('B only', (4, 0), 3, frozenset(('B',)))
    ordinary = Option('ordinary', (0, 0), 0, frozenset())
    options = (original, narrow, sequence, a, b, ordinary)
    approvals = {option.name for option in options}
    permits = {'A', 'narrow A', 'B'}
    resource = (6, 6)

    assert ready(a, resource, 4, approvals, permits)
    assert ready(b, resource, 4, approvals, permits)
    assert not ready(original, resource, 5, approvals, permits)
    assert ready(narrow, resource, 4, approvals, permits)
    assert not ready(narrow, resource, 4, {'A only', 'B only'}, permits)
    assert not ready(narrow, resource, 4, approvals, {'A', 'B'})
    assert not ready(narrow, (5, 6), 4, approvals, permits)
    assert not ready(narrow, (None, 6), 4, approvals, permits)
    assert ready(ordinary, (None, 6), 4, approvals, permits)
    assert not ready(sequence, resource, 4, approvals, permits)
    assert ready(sequence, resource, 5, approvals, permits)
    assert not ready(sequence, resource, 5, approvals, permits, restored=False)
    assert not ready(sequence, (6, 3), 5, approvals, permits)
    print('Parallel trials passed: combined limit, exact scope, paid sequence and refreshed evidence.')


if __name__ == '__main__':
    main()
