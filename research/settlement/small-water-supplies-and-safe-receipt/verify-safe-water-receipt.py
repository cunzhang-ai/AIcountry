def verify_delivery(
    settled_cash, school_funding, tenant_funding, review_funding,
    school_accepted, tenant_accepted, independent_review_available,
):
    assert min(school_funding, tenant_funding, review_funding) >= 0
    assert school_funding + tenant_funding + review_funding <= settled_cash
    return (
        school_funding >= 3 and school_accepted,
        tenant_funding >= 4 and tenant_accepted,
        review_funding >= 1 and independent_review_available,
    )


def next_supply_cost(school_return_qualified, tenants_return_qualified):
    return 3 * (not school_return_qualified) + 4 * (not tenants_return_qualified)


def verify():
    assert verify_delivery(8, 3, 4, 1, True, True, True) == (True, True, True)
    assert verify_delivery(8, 3, 4, 1, True, False, True) == (True, False, True)
    assert verify_delivery(7, 3, 4, 0, True, True, True) == (True, True, False)
    assert verify_delivery(8, 3, 4, 1, True, True, False) == (True, True, False)
    assert verify_delivery(0, 0, 0, 0, True, True, True) == (False, False, False)
    assert verify_delivery(4, 0, 4, 0, True, True, True) == (False, True, False)
    assert next_supply_cost(False, False) == 7
    assert next_supply_cost(True, False) == 4
    assert next_supply_cost(False, True) == 3
    assert next_supply_cost(True, True) == 0
    print('Eight funds the first deliveries and review when both routes accept.')
    print('Seven is due again before recovery if neither independent return qualifies.')


if __name__ == '__main__':
    verify()
