"""Check finite revenue erosion and the separate public asset comparison."""

from fractions import Fraction

standing = 3
finite_cost = (3, 1, 0, 0)
slower_receipts = (6, 6, 4, 0)
faster_receipts = (6, 4, 2, 0)


def after_standing_and_projects(receipts):
    return tuple(revenue - standing - project for revenue, project in zip(receipts, finite_cost))


assert after_standing_and_projects(slower_receipts) == (0, 2, 1, -3)
assert after_standing_and_projects(faster_receipts) == (0, 0, -1, -3)
assert sum(after_standing_and_projects(slower_receipts)[:3]) == standing
assert all(revenue >= project for revenue, project in zip(faster_receipts, finite_cost))

transition = 4
renewal_and_environment = 5
retain_debt = transition + renewal_and_environment
concession_debt = transition - 2
retain_due = Fraction(retain_debt + 1, 2)
concession_due = Fraction(concession_debt + 1, 2)
standing_source = 1
assert retain_due == 5 and concession_due == Fraction(3, 2)
assert standing_source + 4 - retain_due == 0
assert standing_source + 3 - retain_due == -1
assert standing_source + 1 - concession_due == Fraction(1, 2)
assert 6 - transition == 2
assert standing_source - 2 == -1
annual_required, net_general_receipts = 7, 7
additional_earned_backing = 1
assert net_general_receipts - (annual_required + additional_earned_backing) == -1
assert net_general_receipts - annual_required == 0
print("Shrinking tax base, earned backing and separate asset financing verified.")
