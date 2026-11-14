"""Verify selected reported lines and a separate constructed cash window."""


def main():
    assert 11_283 - 6_151 - 3_680 == 1_452
    cash_change = 1_912 - 1_634 - 279
    assert cash_change == -1 and 12 + cash_change == 11
    assert 9_522 - 1_208 == 8_314
    assert 9_209 - 9_127 == 82
    available = 4 + 2 + 2
    assert 9 - available == 1
    assert available + 1 == 9
    remaining_contract_payment = 3 - 1
    assert remaining_contract_payment - 2 - 2 == -2
    print("Enterprise cash: reported accounts and two protected payment windows passed.")


if __name__ == "__main__":
    main()
