"""Reproduce the constructed due-date and payment-state comparisons."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Payment:
    payer: str
    currency: str
    due: int
    amount: int


opening = (
    Payment("treasury", "L", 1, 8),
    Payment("health", "F", 2, 4),
    Payment("debt", "F", 3, 3),
)
cash = (
    Payment("treasury", "L", 0, 8),
    Payment("health", "F", 0, 4),
    Payment("debt", "F", 0, 2),
    Payment("debt", "F", 4, 1),
)


def funding_gaps(obligations, sources):
    """Allocate capacity up to the obligation; prove no receipt or partial acceptance."""
    consumed = {}
    gaps = []
    for obligation in sorted(obligations, key=lambda line: line.due):
        key = (obligation.payer, obligation.currency)
        balance = sum(
            source.amount
            for source in sources
            if (source.payer, source.currency) == key and source.due <= obligation.due
        ) - consumed.get(key, 0)
        allocated = min(obligation.amount, balance)
        consumed[key] = consumed.get(key, 0) + allocated
        gaps.append(obligation.amount - allocated)
    return gaps


assert funding_gaps(opening, cash) == [0, 0, 1]
domestic_issue = Payment("debt", "N", 0, 10)
assert funding_gaps(opening, cash + (domestic_issue,)) == [0, 0, 1]
delivered_fx = Payment("debt", "F", 3, 1)
assert funding_gaps(opening, cash + (delivered_fx,)) == [0, 0, 0]
external_account = Payment("treasury", "F", 0, 8)
assert funding_gaps(opening[:1], (external_account,)) == [8]
later_wage = Payment("treasury", "L", 5, 2)
assert funding_gaps(opening + (later_wage,), cash) == [0, 0, 1, 2]


def authority_for_release(*, currency_law, appropriation, readiness):
    return currency_law and appropriation and readiness


assert authority_for_release(currency_law=True, appropriation=True, readiness=True)
for withheld in ("currency_law", "appropriation", "readiness"):
    qualifications = dict(currency_law=True, appropriation=True, readiness=True)
    qualifications[withheld] = False
    assert not authority_for_release(**qualifications)

wage = 2
emergency_advance = 1


def payroll_status(final, *, settlement_access, alternate_funded, covered_deposit, meal_slot):
    replay = wage if final is False and alternate_funded else 0
    discharged = wage if final is True else replay
    insured_claim = final is True and not settlement_access and covered_deposit
    wage_accessible = (final is True and settlement_access) or replay == wage
    return (wage - discharged, insured_claim, wage_accessible, meal_slot)


assert payroll_status(None, settlement_access=False, alternate_funded=True,
                      covered_deposit=False, meal_slot=True) == (2, False, False, True)
assert payroll_status(True, settlement_access=False, alternate_funded=False,
                      covered_deposit=True, meal_slot=False) == (0, True, False, False)
assert payroll_status(False, settlement_access=False, alternate_funded=False,
                      covered_deposit=False, meal_slot=True) == (2, False, False, True)
assert payroll_status(False, settlement_access=False, alternate_funded=True,
                      covered_deposit=False, meal_slot=False) == (0, False, True, False)
assert emergency_advance < wage

print("Opening gaps are 0 L payroll, 0 F import and 1 F debt; only timely F cures the debt gap.")
print("Authorization, appropriation and readiness are separate. Final wage credit, deposit insurance and an actual meal can diverge.")
