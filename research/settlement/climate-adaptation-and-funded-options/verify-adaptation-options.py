def last_useful_decision(first_failure_year, end_to_end_years):
    return first_failure_year - end_to_end_years


def path_qualifies(decision_year, failure_year, lead_years, settled, required, receiving):
    return (
        decision_year <= last_useful_decision(failure_year, lead_years)
        and settled >= required
        and receiving
    )


def verify():
    leads = [3, 2, 4]
    assert [last_useful_decision(5, years) for years in leads] == [2, 3, 1]
    assert [last_useful_decision(8, years) for years in leads] == [5, 6, 4]
    assert 2 + 1 == 3
    assert path_qualifies(2, 5, 3, 6, 6, True)
    assert not path_qualifies(3, 5, 3, 6, 6, True)
    assert not path_qualifies(3, 5, 2, 6, 8, True)
    assert path_qualifies(3, 5, 2, 8, 8, True)
    assert not path_qualifies(3, 5, 2, 8, 8, False)
    print('Waiting until year 3 misses the regional route. The timely in-place route needs two more settled units and actual receiving.')


if __name__ == '__main__':
    verify()
