"""Check lawful settlement states and their separate cash requirements."""

A_DUE, B_DUE = 60, 50
OPENING_A, OPENING_B = 15, 15
MATCH = min(A_DUE, B_DUE)
RESIDUAL = A_DUE - MATCH
BRIDGE_TO_B = B_DUE - OPENING_B
closing_matched = (OPENING_A - RESIDUAL, OPENING_B + RESIDUAL)
closing_sequential = (OPENING_A + B_DUE - A_DUE, OPENING_B + A_DUE - B_DUE)

assert MATCH == 50 and RESIDUAL == 10
assert A_DUE - OPENING_A == 45 and BRIDGE_TO_B == 35
assert OPENING_B + BRIDGE_TO_B == B_DUE
assert closing_matched == closing_sequential == (5, 25)
assert A_DUE + B_DUE - RESIDUAL == 100


def gross_still_due(match_state, residual_paid=False):
    if match_state == "uncertain":
        return None
    if match_state == "not discharged":
        return A_DUE, B_DUE
    assert match_state == "final"
    return (0 if residual_paid else RESIDUAL), 0


assert gross_still_due("uncertain") is None
assert gross_still_due("not discharged") == (60, 50)
assert gross_still_due("final") == (10, 0)
assert gross_still_due("final", residual_paid=True) == (0, 0)
assert RESIDUAL - (OPENING_A - 6) == 1  # Protected readiness is outside the match.
print("Gross routes, reciprocal discharge, residual finality and protected capacity checked.")


def qualifies(*, authorized, mature, uncontested, compatible, exclusive,
              cash_after_protected_work):
    return (
        authorized and mature and uncontested and compatible and exclusive
        and cash_after_protected_work >= RESIDUAL
    )


eligible = dict(authorized=True, mature=True, uncontested=True, compatible=True,
                exclusive=True, cash_after_protected_work=15)
assert qualifies(**eligible)
for field in ("authorized", "mature", "uncontested", "compatible", "exclusive"):
    assert not qualifies(**(eligible | {field: False}))
assert not qualifies(**(eligible | {"cash_after_protected_work": 9}))
print("Ineligible matches and insufficient cash after protected work remain outside release.")
