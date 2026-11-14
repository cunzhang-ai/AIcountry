from itertools import combinations


def receipt_day(delays, alternate_stage=None, *, qualified=False, reviewer=True):
    if not reviewer:
        return None
    return 3 + sum(
        delay for stage, delay in delays
        if not (qualified and stage == alternate_stage)
    )


def verify():
    delays = (('records', 2), ('hearing', 2), ('execution', 2))
    deadline = 8

    assert receipt_day(()) == 3
    for subset_size in (1, 2):
        for subset in combinations(delays, subset_size):
            assert receipt_day(subset) == 3 + 2 * subset_size <= deadline

    assert receipt_day(delays) == 9 > deadline
    assert receipt_day(delays, 'execution', qualified=True) == 7 <= deadline
    assert receipt_day(delays, 'execution', qualified=False) == 9
    assert receipt_day(delays, 'execution', qualified=True, reviewer=False) is None

    print('Every pair fits the day 8 deadline, but all three reach ballot production on day 9.')
    print('A lawful independent execution route restores day 7 receipt.')


if __name__ == '__main__':
    verify()
