"""Reproduce the transcribed opening quarter and constructed release test."""

from decimal import Decimal


def total(*values):
    return sum(map(Decimal, values), Decimal(0))


def main():
    opening, close = map(Decimal, ("161.496380", "227.615418"))
    assert opening - Decimal("178") == Decimal("-16.503620")
    assert total("15", "41", "34", "20") - Decimal("109") == 1
    assert total("65", "20", "12", "13") - Decimal("109") == 1
    assert total("7.3", "9.7", "4.3") - Decimal("21.2") == Decimal("0.1")
    assert total("9.0", "8.4", "6.9") == Decimal("24.3")
    assert total("-39.9", "-24.3") == Decimal("-64.2")
    assert close - opening == Decimal("66.119038")
    assert close - opening - Decimal("64.2") == Decimal("1.919038")

    minimum = 4
    first = 12 + 3 - 10
    assert first - minimum == 1
    assert minimum - (first - 5) == 4
    after_preparation = first - 1
    second = after_preparation + 7 - 5
    assert second - minimum == 2
    assert 4 - (second - minimum) == 2
    second_without_refinancing = after_preparation - 5
    assert minimum - second_without_refinancing == 5
    assert second_without_refinancing == -1
    print("Opening quarter: source residuals and two-window release constraints passed.")


if __name__ == "__main__":
    main()
