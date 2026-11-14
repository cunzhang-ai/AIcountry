"""Reproduce the authored two-cohort affordability and failure comparison."""

BRIDGE = 3
ADULT_CONTINUATION = 5
LOCAL_PAIR = 8
DISTANT_PAIR = 9
QUALIFIED_HOME_SUPPORT = 4


def payable_packages(budget, local_available=True, sunk_local_payment=0,
                     safe_return_established=False):
    options = {"distant pair": DISTANT_PAIR}
    if local_available:
        options["local pair"] = LOCAL_PAIR
    if safe_return_established:
        options["safe return"] = QUALIFIED_HOME_SUPPORT
    continuing_cost = BRIDGE + ADULT_CONTINUATION + sunk_local_payment
    return {
        option: continuing_cost + cost
        for option, cost in options.items()
        if continuing_cost + cost <= budget
    }


if __name__ == "__main__":
    assert payable_packages(16) == {"local pair": 16}
    assert payable_packages(17) == {"distant pair": 17, "local pair": 16}
    assert payable_packages(15) == {}
    assert payable_packages(16, local_available=False) == {}
    assert payable_packages(17, local_available=False) == {"distant pair": 17}
    assert payable_packages(24, local_available=False, sunk_local_payment=8) == {}
    assert payable_packages(25, local_available=False, sunk_local_payment=8) == {
        "distant pair": 25
    }
    assert payable_packages(12) == {}
    assert payable_packages(12, safe_return_established=True) == {"safe return": 12}
    print("Complete local package: 16. Qualified distant package: 17.")
    print("Replacement after unrecoverable payment: 25. Qualified safe return: 12.")
