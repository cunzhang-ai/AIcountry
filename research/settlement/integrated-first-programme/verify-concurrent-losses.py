"""Compare exact starts and continuing duties on the same first budget."""

from pathlib import Path
from runpy import run_path


baseline = run_path(str(Path(__file__).with_name('verify-protected-corrections.py')))
CASE = baseline['CASE']
ZERO = baseline['ZERO']
R = baseline['R']
combine = baseline['combine']
need = baseline['need']
gap = baseline['gap']
qualified = baseline['qualified']

WATER = {**ZERO, 'national': (2, 2, 0), 'foreign': 1}
CARE = {**ZERO, 'national': (1, 2, 0), 'local': (1, 1, 0), 'work': (1, 0, 0)}
ALTERNATE_COST = {**ZERO, 'national': (1, 1, 0), 'local': (0, 1, 0)}
ALTERNATE_CAPACITY = {**ZERO, 'work': (1, 0, 0)}


def remaining(envelope, *due):
    for duty in due:
        envelope = combine(envelope, duty, -1)
    return envelope


def main():
    reference = CASE['paths']['reference']
    weaker = CASE['paths']['weaker']
    votes = {'', 'E', 'P', 'H', 'EP'}
    accepted = {'E', 'P', 'H', 'K'}
    advance = CASE['housing_advance']

    def ready(package, capacity, *, approved=votes, correction=True):
        return qualified(
            package, capacity, approved, accepted, advance,
            correction_ready=correction, review_ready=False,
        )

    water_only = remaining(reference, R, WATER)
    care_only = remaining(reference, R, CARE)
    both = remaining(reference, R, WATER, CARE)
    assert both == {
        'national': (3, 6, 6), 'local': (2, 5, 5), 'foreign': 1, 'work': (1, 2, 2),
    }
    assert ready('EP', water_only) and ready('EP', care_only)
    assert ready('H', water_only) and not ready('H', care_only)
    assert gap(need('EP', False), both) == {**ZERO, 'national': (1, 1, 0)}
    assert not ready('EP', both)
    assert ready('E', both) and ready('P', both) and ready('', both)
    assert not ready('E', both, approved={'EP'})
    assert not ready('E', both, correction=False)
    assert gap(need('H', False), both) == {**ZERO, 'work': (1, 0, 0)}

    continuing = combine(combine(R, WATER), CARE)
    assert gap(continuing, weaker) == {**ZERO, 'work': (1, 0, 0)}
    assert not ready('', remaining(weaker, continuing), correction=False)

    housing = need('H', False)
    with_provider = combine(both, ALTERNATE_CAPACITY)
    after_housing = remaining(with_provider, housing, ALTERNATE_COST)
    assert gap(combine(housing, ALTERNATE_COST), with_provider) == ZERO
    assert gap(housing, both) == {**ZERO, 'work': (1, 0, 0)}
    assert not ready('E', after_housing) and not ready('P', after_housing)
    gross_housing_due = CASE['housing_local_gross_due'][0]
    local_housing_cash = CASE['measures']['H']['local'][0]
    assert gross_housing_due == local_housing_cash + advance[0]
    assert gross_housing_due - local_housing_cash == 2
    print('Concurrent losses passed: exact choices, continuing gaps and binding housing.')


if __name__ == '__main__':
    main()
