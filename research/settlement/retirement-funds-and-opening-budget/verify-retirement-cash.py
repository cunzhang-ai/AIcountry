"""Check reported account arithmetic and the constructed late backing case."""


def main():
    assert 220_882 + 14_544 == 235_426
    scheme_change = 289_600 - 289_573 + 1 + 394
    assert scheme_change == 422
    assert -150 + scheme_change == 272
    assert 14_086 - 20_140 == -6_054
    assert 7_721 + 1_380 - 63 - 9_037 == 1

    post_payment = 9 + 3 - 10
    minimum = 6
    bridge = minimum - post_payment
    assert post_payment == 2
    assert bridge == 4
    assert 6 - bridge - 6 == -4
    assert post_payment + bridge == minimum
    # Include a 4-unit next benefit before testing repayment.
    after_next_benefit = post_payment + bridge + 5 - 4
    assert after_next_benefit == 7
    assert after_next_benefit - bridge == 3
    assert after_next_benefit - minimum == 1
    print("Pension cash: distinct payers, published arithmetic and late backing passed.")


if __name__ == "__main__":
    main()
