"""Check the constructed service, mandate and billing comparison."""

OLD_CHARGE = 6
PREMATURE_CHARGE = 5
PRIOR_DISPUTE = 4
OVERLAP_COST = 2
ALTERNATE_COST = 3


def route_for_alert(*, authorized, new_usable, old_usable, alternate_usable):
    if authorized and new_usable:
        return "new"
    if old_usable:
        return "old"
    if alternate_usable:
        return "alternate"
    return "unserved"


for authorized, new, old, alternate, expected in (
    (True, False, True, True, "old"),
    (True, False, False, True, "alternate"),
    (True, False, False, False, "unserved"),
    (True, True, True, True, "new"),
    (False, True, True, True, "old"),
):
    assert route_for_alert(
        authorized=authorized, new_usable=new, old_usable=old, alternate_usable=alternate
    ) == expected

charged = OLD_CHARGE + PREMATURE_CHARGE
refunded = charged - OLD_CHARGE
assert refunded == PREMATURE_CHARGE == 5
current_subscription_after_refund = charged - refunded
assert (current_subscription_after_refund, PRIOR_DISPUTE) == (6, 4)
assert OVERLAP_COST + ALTERNATE_COST == 5

print("Provider switching comparison passed: scope, verified receiving, joint failure and billing.")
