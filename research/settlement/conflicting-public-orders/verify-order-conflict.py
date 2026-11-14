"""Check declared routes under two overlapping public execution orders."""

from dataclasses import dataclass, replace


SHARED_TRIPS = {'A': (50, 90), 'B': (50, 80)}
ORIGINAL_DUE = {'A': 100, 'B': 80}


@dataclass(frozen=True)
class Execution:
    available_cash: int
    reserve_minute: int = 35
    decision_minute: int = 45
    judge_count: int = 3
    affirmative_votes: int = 2
    substitute_accepted: bool = True
    hearing_accepted: bool = True
    hearing_independent: bool = True
    transport_safe: bool = True
    prior_authority_for_a: bool = False


def resolve(execution):
    if (
        execution.available_cash >= 4
        and execution.reserve_minute <= 35
        and execution.substitute_accepted
        and execution.transport_safe
    ):
        return 'ordinary alternate', {'A': SHARED_TRIPS['A'][1], 'B': 80}

    if (
        execution.available_cash >= 2
        and execution.decision_minute <= 45
        and execution.judge_count == 3
        and execution.affirmative_votes >= 2
        and execution.hearing_accepted
        and execution.hearing_independent
        and execution.transport_safe
    ):
        return 'scoped variation', {'A': SHARED_TRIPS['A'][1], 'B': 80}

    if execution.prior_authority_for_a and execution.transport_safe:
        return 'existing authority', {'A': SHARED_TRIPS['A'][1]}

    return 'unresolved conflict', {}


def main():
    assert max(start for start, end in SHARED_TRIPS.values()) < min(
        end for start, end in SHARED_TRIPS.values()
    )
    reference = Execution(4)
    narrow = replace(reference, available_cash=2)
    for case, expected in ((reference, 'ordinary alternate'), (narrow, 'scoped variation')):
        route, receipts = resolve(case)
        assert route == expected
        assert receipts.keys() == ORIGINAL_DUE.keys()
        assert all(receipts[key] <= ORIGINAL_DUE[key] for key in receipts)

    assert resolve(replace(reference, reserve_minute=36))[0] == 'scoped variation'
    assert resolve(replace(narrow, decision_minute=46))[1] == {}
    assert resolve(replace(narrow, judge_count=2))[1] == {}
    assert resolve(replace(narrow, affirmative_votes=1))[1] == {}
    assert resolve(replace(narrow, hearing_accepted=False))[1] == {}
    assert resolve(replace(narrow, hearing_independent=False))[1] == {}
    assert resolve(replace(reference, transport_safe=False))[1] == {}
    partial = resolve(replace(narrow, available_cash=1, prior_authority_for_a=True))
    assert partial == (
        'existing authority', {'A': 90}
    )
    assert ORIGINAL_DUE.keys() - partial[1].keys() == {'B'}
    assert resolve(replace(narrow, available_cash=1)) == ('unresolved conflict', {})
    print('Order conflict passed: shared assignment, exact means, original deadlines and retained claims.')


if __name__ == '__main__':
    main()
