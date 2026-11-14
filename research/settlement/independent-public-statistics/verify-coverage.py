"""Check the authored coverage break, budget date and bounded use."""

from dataclasses import dataclass, replace
from fractions import Fraction


@dataclass(frozen=True)
class CoverageCheck:
    lower: int
    upper: int
    receipt_day: int
    cost: int
    independent: bool = True
    safe_and_qualified: bool = True


def qualified_rate(population, observed, unmet, check, statistical_cash, vote_day):
    missing = population - observed
    lower, upper = 0, missing
    if (
        check is not None
        and check.independent
        and check.safe_and_qualified
        and check.receipt_day <= vote_day
        and 1 + check.cost <= statistical_cash
    ):
        assert 0 <= check.lower <= check.upper <= missing
        lower, upper = check.lower, check.upper
    return Fraction(unmet + lower, population), Fraction(unmet + upper, population)


def main():
    threshold = Fraction(8, 100)
    prior_rate = Fraction(90, 1000)
    check = CoverageCheck(34, 44, 3, 4)

    def budget_evidence(coverage_check, cash=5):
        return qualified_rate(1000, 800, 48, coverage_check, cash, 4)

    assert Fraction(48, 800) < threshold
    partial = budget_evidence(None)
    assert partial == (Fraction(48, 1000), Fraction(248, 1000))
    assert partial[0] <= threshold < partial[1]

    lower, upper = budget_evidence(check)
    assert (lower, upper) == (Fraction(82, 1000), Fraction(92, 1000))
    assert lower > threshold
    assert lower <= prior_rate <= upper
    assert budget_evidence(check, 4) == partial
    assert budget_evidence(replace(check, receipt_day=5)) == partial
    assert budget_evidence(replace(check, independent=False)) == partial
    assert budget_evidence(replace(check, safe_and_qualified=False)) == partial
    assert budget_evidence(replace(check, lower=20, upper=32))[1] == threshold
    assert budget_evidence(replace(check, receipt_day=4)) == (lower, upper)
    print('Statistics coverage passed: denominator, independent receipt, budget date and threshold.')


if __name__ == '__main__':
    main()
