def paid_route(uses_personal_data, consent, prohibited_basis, variant_inspectable,
               *, directly_provided=True):
    lawful_source = not uses_personal_data or (consent and directly_provided)
    return lawful_source and not prohibited_basis and variant_inspectable


def correction_day(funds, original_evidence=True, independent_execution=True):
    if funds < 2 + 2 + 1 or not original_evidence or not independent_execution:
        return None
    return 5


def verify():
    assert paid_route(False, False, False, True)
    assert not paid_route(True, True, True, True)
    assert not paid_route(True, False, False, True)
    assert not paid_route(True, True, False, False)
    assert paid_route(True, True, False, True)
    assert not paid_route(True, True, False, True, directly_provided=False)

    day = correction_day(5)
    assert day > 4 and day <= 6
    assert correction_day(4) is None
    assert correction_day(5, original_evidence=False) is None
    assert correction_day(5, independent_execution=False) is None
    print('Context can continue; prohibited profile-based placement cannot.')
    print('A day 5 correction reaches a day 6 opportunity and misses day 4.')


if __name__ == '__main__':
    verify()
