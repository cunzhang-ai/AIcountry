"""Check the constructed cash, authorization and receiving branches."""

MINIMUM = 1
opening = 2
early_receipts, later_receipts = 12, 18
early_due, later_due = 13, 15


def balances(rephased=0, costs=(0, 0), delayed=0, draw=0, recovered=0, backstop=0):
    early_cost, later_cost = costs
    early = opening + early_receipts + rephased - early_due - early_cost - delayed + draw
    financing_cost = 1 if draw else 0
    late = early + later_receipts - rephased - later_due - later_cost + recovered + backstop
    return early, late - draw - financing_cost


def qualifies(path):
    return all(balance >= MINIMUM for balance in path)


assert balances() == (1, 4)
assert balances(costs=(1, 2)) == (0, 1)
assert balances(rephased=1) == (2, 4)
assert balances(rephased=1, costs=(1, 2)) == (1, 1)
assert balances(rephased=1, costs=(2, 4)) == (0, -2)
assert balances(rephased=1, costs=(4, 2)) == (-2, -2)
assert balances(delayed=3, draw=3, recovered=3) == (1, 3)
assert balances(delayed=3, draw=3) == (1, 0)
# Price the same lawful draw and the independently assigned late cash.
assert balances(rephased=1, delayed=3, draw=3) == (2, 0)
phase = {"rephased": 1, "costs": (1, 2)}
stress = phase | {"delayed": 3, "draw": 3}
assert balances(**stress, recovered=3) == (1, 0)
assert balances(**stress) == (1, -3)
assert balances(**stress, recovered=3, backstop=1) == (1, 1)
assert balances(**stress, backstop=4) == (1, 1)
assert not qualifies(balances(**stress, backstop=3))
phase_ready = all(qualifies(path) for path in (
    balances(**phase),
    balances(**stress, recovered=3, backstop=1),
    balances(**stress, backstop=4),
))


def release(*, cash, p_votes, w_votes, p_receiver, w_receiver):
    if cash and p_votes and p_receiver:
        return "P"
    if cash and w_votes and w_receiver:
        return "W"
    return "R"


positive = {"cash": phase_ready,
            "p_votes": True, "w_votes": True, "p_receiver": True, "w_receiver": True}
assert release(**positive) == "P"
assert release(**(positive | {"p_receiver": False})) == "W"
assert release(**(positive | {"p_receiver": False, "w_votes": False})) == "R"
assert release(**(positive | {"cash": False})) == "R"
assert release(**(positive | {"p_receiver": False, "w_receiver": False})) == "R"
assert release(**(positive | {"p_votes": False, "w_votes": False})) == "R"

# Verify the late reserve by what it can lawfully fund in the same stress.
proposed_refit_reserve = 4
required_access_room = 2
eligible_backstop = proposed_refit_reserve - required_access_room
assert balances(**stress, backstop=eligible_backstop) == (1, -1)
assert qualifies(balances(**stress, recovered=3, backstop=1))
assert release(**(positive | {"cash": qualifies(
    balances(**stress, backstop=eligible_backstop))})) == "R"
repair_stress = {"rephased": 1, "delayed": 3, "draw": 2}
assert balances(**repair_stress) == (1, 0)
assert qualifies(balances(**repair_stress, backstop=1))
new_unrestricted_source = 2
assert qualifies(balances(**stress, backstop=eligible_backstop + new_unrestricted_source))

receiving = ("timely", "late", "omitted")
assert sum(state != "omitted" for state in receiving) == 2
assert sum(state == "timely" for state in receiving) == 1
assert sum(state != "timely" for state in receiving) == 2
print("Four-payer continuation, rephasing, source-service conflict, exact release and receiving branches verified.")
