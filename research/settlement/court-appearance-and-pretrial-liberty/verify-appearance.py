from decimal import Decimal


def warrant_can_issue(required, known, feasible, evasion_evidence, necessary):
    return all((required, known, feasible, evasion_evidence, necessary))


def operational_result(assistance_accepted, interpretation, independent_review,
                       first_desk_day, second_desk_day):
    hearing_ready = all((assistance_accepted, interpretation, independent_review))
    desks_confirmed_before_check = all(
        day is not None and day < 4 for day in (first_desk_day, second_desk_day)
    )
    return hearing_ready, desks_confirmed_before_check


def funded_desks(available_units):
    hearing_units = 3
    execution_units = max(0, available_units - hearing_units)
    return tuple(3 if execution_units >= desk else None for desk in (1, 2))


def verify():
    assert not warrant_can_issue(True, True, False, False, False)
    assert warrant_can_issue(True, True, True, True, True)
    assert not warrant_can_issue(True, True, True, False, True)
    assert not warrant_can_issue(True, False, True, True, True)
    assert not warrant_can_issue(True, True, True, True, False)

    assert operational_result(True, True, True, *funded_desks(5)) == (True, True)
    assert operational_result(True, True, True, *funded_desks(4)) == (True, False)
    assert operational_result(True, True, True, 3, 4) == (True, False)
    assert operational_result(False, True, True, 3, 3) == (False, True)

    assert 2811 + 2898 == 5709
    assert Decimal('20.7') - Decimal('17.6') == Decimal('3.1')
    assert Decimal('6.6') - Decimal('5.2') == Decimal('1.4')
    print('A feasible new hearing and a withdrawn warrant are separate results.')
    print('The comparison preserves a warranted second case without automatic remand.')


if __name__ == '__main__':
    verify()
