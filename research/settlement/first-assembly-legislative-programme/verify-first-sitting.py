"""Reproduce the separate operating and scrutiny limits."""

baseline = (7, 12, 6, 3)
limit = (10, 18, 8, 5)
intake = (1, 2, 0, 1)
housing = (3, 5, 2, 2)


def fits(*offers):
    demand = [sum(group) for group in zip(baseline, *offers)]
    return all(use <= ceiling for use, ceiling in zip(demand, limit))


assert fits(intake)
assert fits(housing)
assert not fits(intake, housing)


def docket(*, scrutiny, amended, housing_vote, remedy_vote, intake_vote):
    housing_blocks = 2 + int(amended)
    if scrutiny >= housing_blocks and housing_vote and remedy_vote and fits(housing):
        return "H"
    if scrutiny >= 1 and intake_vote and fits(intake):
        return "I"
    return "standing law"


assert docket(scrutiny=3, amended=False, housing_vote=True,
              remedy_vote=True, intake_vote=True) == "H"
assert docket(scrutiny=2, amended=True, housing_vote=False,
              remedy_vote=True, intake_vote=True) == "I"
assert docket(scrutiny=3, amended=False, housing_vote=True,
              remedy_vote=False, intake_vote=True) == "I"
assert docket(scrutiny=3, amended=False, housing_vote=True,
              remedy_vote=False, intake_vote=False) == "standing law"
assert docket(scrutiny=3, amended=True, housing_vote=True,
              remedy_vote=True, intake_vote=False) == "H"
# Days relative to the start of the financial year.
appointment, final_vote = -90, -14
assert appointment + 30 == -60
assert -150 < appointment and -120 < appointment
assert final_vote - 21 == -35
assert final_vote - 14 == -28
print("Separate scrutiny, funding, exact votes and fallback verified.")
