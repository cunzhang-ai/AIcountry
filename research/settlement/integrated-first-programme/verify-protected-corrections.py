"""Apply Design294's authored protected correction to the existing fixture."""

import json
from pathlib import Path


CASE = json.loads(Path(__file__).with_name('case.json').read_text())
VECTORS = ('national', 'local', 'work')
ZERO = {'national': (0, 0, 0), 'local': (0, 0, 0), 'foreign': 0, 'work': (0, 0, 0)}
K = {**ZERO, 'national': (1, 1, 0), 'local': (0, 1, 0), 'work': (0, 1, 0)}
R = {**ZERO, 'national': (1, 2, 0), 'local': (2, 3, 0), 'work': (2, 1, 0)}
Q = {**ZERO, 'national': (0, 1, 0)}
Q_CAPACITY = {**ZERO, 'work': (0, 1, 0)}


def combine(first, second, direction=1):
    return {
        **{
            axis: tuple(left + direction * right for left, right in zip(first[axis], second[axis]))
            for axis in VECTORS
        },
        'foreign': first['foreign'] + direction * second['foreign'],
    }


def need(measures, extra_review):
    total = K if 'E' in measures else ZERO
    for measure in measures:
        total = combine(total, CASE['measures'][measure])
    return combine(total, Q) if extra_review else total


def gap(needed, available):
    residual = combine(needed, available, -1)
    return {
        **{axis: tuple(max(0, part) for part in residual[axis]) for axis in VECTORS},
        'foreign': max(0, residual['foreign']),
    }


def qualified(package, available, approved, accepted, advance, *, correction_ready, review_ready):
    measures = set(package) - {'Q'}
    extra_review = 'Q' in package
    limits = combine(available, Q_CAPACITY) if extra_review else available
    housing_ready = all(
        cash + own >= due for cash, own, due in zip(
            advance, CASE['measures']['H']['local'], CASE['housing_local_gross_due'],
        )
    )
    required_acceptance = set(package) | ({'K'} if 'E' in measures else set())
    return (
        correction_ready and package in approved
        and required_acceptance <= accepted
        and (not extra_review or review_ready)
        and ('H' not in measures or housing_ready)
        and gap(need(measures, extra_review), limits) == ZERO
    )


def main():
    reference = combine(CASE['paths']['reference'], R, -1)
    weaker = combine(CASE['paths']['weaker'], R, -1)
    assert reference == {
        'national': (6, 10, 6), 'local': (3, 6, 5), 'foreign': 2, 'work': (2, 2, 2),
    }
    assert weaker == {
        'national': (3, 8, 6), 'local': (1, 5, 5), 'foreign': 1, 'work': (0, 1, 2),
    }
    approved = {'', 'EP', 'EH', 'EPH', 'E', 'P', 'H', 'EQ'}
    accepted = {'E', 'P', 'H', 'K', 'Q'}
    advance = CASE['housing_advance']

    def ready(package, envelope, *, votes=approved, receipt=advance, correction=True, review=True):
        return qualified(
            package, envelope, votes, accepted, receipt,
            correction_ready=correction, review_ready=review,
        )

    assert ready('EP', reference)
    assert ready('P', reference) and ready('H', reference)
    assert not ready('H', reference, receipt=(0, 3, 2))
    assert not ready('EH', reference)
    assert not ready('EPH', reference)
    assert not ready('EP', weaker)
    assert not ready('P', weaker) and not ready('H', weaker)
    assert not ready('E', weaker)
    assert gap(need('E', False), weaker) == {**ZERO, 'work': (0, 1, 0)}
    assert ready('', weaker)
    assert ready('EQ', weaker)
    assert not ready('EQ', weaker, review=False)
    assert not ready('EQ', weaker, votes={'EP'})
    assert not ready('EQ', weaker, correction=False)
    assert not qualified(
        'EQ', weaker, approved, accepted - {'K'}, advance,
        correction_ready=True, review_ready=True,
    )

    housing = need('H', False)
    after_binding = combine(reference, housing, -1)
    assert not ready('EP', after_binding)
    assert gap(housing, weaker) == {
        **ZERO, 'local': (1, 0, 0), 'work': (2, 0, 0),
    }
    assert CASE['housing_local_gross_due'][0] - weaker['local'][0] == 3
    print('Protected budget passed: exact narrower choices, paid review and post-binding shortfalls.')


if __name__ == '__main__':
    main()
