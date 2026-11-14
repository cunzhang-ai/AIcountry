"""Reproduce the authored partial-amendment votes and conditions."""


def passes_assembly_route(yes, no):
    return yes + no > 0 and yes > no


def passes_petition_route(yes, no):
    return yes + no > 0 and 5 * yes >= 3 * (yes + no)


def dependent_effect(approved, prerequisite_operative_by_deadline, own_lawful_date):
    return approved and prerequisite_operative_by_deadline and own_lawful_date


access = passes_assembly_route(700, 300)
appointments = passes_petition_route(590, 410)
review_service = passes_assembly_route(550, 450)
assert (access, appointments, review_service) == (True, False, True)
assert passes_petition_route(600, 400)
assert not passes_petition_route(0, 0)
assert not passes_assembly_route(500, 500)
assert dependent_effect(review_service, True, True)
assert not dependent_effect(review_service, False, True)
assert not dependent_effect(review_service, True, False)
assert not dependent_effect(False, True, True)
print("Separate constitutional votes: independent approval and declared lawful dependencies passed.")
