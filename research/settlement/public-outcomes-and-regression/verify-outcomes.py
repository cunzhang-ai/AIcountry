"""Reconcile reported health endpoints and an authored changing population."""

from fractions import Fraction


def endpoint_gaps():
    # Reported rounded estimates, in tenths of a year.
    most_deprived = (736, 497, 784, 473)
    least_deprived = (819, 678, 851, 663)
    gaps = tuple(least - most for least, most in zip(least_deprived, most_deprived))
    assert gaps == (83, 181, 67, 190)
    print("Wales endpoint gaps (years):", tuple(gap / 10 for gap in gaps))


def compare_access():
    ordinary_before = Fraction(72, 80)
    assisted_before = Fraction(10, 20)
    ordinary_after = Fraction(81, 90)
    assisted_after = Fraction(4, 10)
    before = Fraction(82, 100)
    observed_after = Fraction(85, 100)
    fixed_after = Fraction(80, 100) * ordinary_after + Fraction(20, 100) * assisted_after

    assert ordinary_before == ordinary_after and assisted_after < assisted_before
    assert fixed_after == Fraction(80, 100)
    assert fixed_after < before < observed_after

    missing = 5
    combined_bounds = (Fraction(85, 100 + missing), Fraction(85 + missing, 100 + missing))
    assisted_bounds = (Fraction(4, 10 + missing), Fraction(4 + missing, 10 + missing))
    assert combined_bounds == (Fraction(85, 105), Fraction(90, 105))
    assert assisted_bounds == (Fraction(4, 15), Fraction(9, 15))
    assert combined_bounds[0] < before < combined_bounds[1]
    assert assisted_bounds[0] < assisted_before < assisted_bounds[1]
    print("Observed receipt: 82% to 85%; fixed composition: 82% to 80%.")
    print("Unknown eligible cases leave both the combined and assisted trends unresolved.")
    print(f"All five missing confirmed unserved: {float(combined_bounds[0]):.1%} combined.")


if __name__ == "__main__":
    endpoint_gaps()
    compare_access()
