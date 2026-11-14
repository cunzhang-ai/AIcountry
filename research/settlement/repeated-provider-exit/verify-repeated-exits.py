"""Check independent capacity and dated costs in the constructed comparison."""

NEEDED_VISITS = 2


def qualified_combined(*, ordinary_standby, independent, origin_floor, recurring, startup,
                       public_receiving=True, cooperative_receiving=True):
    public_slot = int(ordinary_standby and recurring >= 1 and public_receiving)
    cooperative_slot = int(
        independent and origin_floor and cooperative_receiving
        and recurring >= 1 + public_slot and startup >= 1
    )
    return public_slot + cooperative_slot


def qualified_ordinary(*, elected, staff, review, recurring, startup):
    return NEEDED_VISITS if elected and staff and review and recurring >= 3 and startup >= 2 else 0


baseline = dict(ordinary_standby=True, independent=True, origin_floor=True, recurring=3, startup=2)
assert qualified_combined(**baseline) == 2
assert qualified_combined(**(baseline | {"independent": False})) == 1
assert qualified_combined(**(baseline | {"origin_floor": False})) == 1
assert qualified_combined(**(baseline | {"ordinary_standby": False})) == 1
assert qualified_combined(**(baseline | {"public_receiving": False})) == 1
assert qualified_combined(**(baseline | {"cooperative_receiving": False})) == 1
assert qualified_combined(**(baseline | {"public_receiving": False,
                                       "cooperative_receiving": False})) == 0
assert qualified_ordinary(elected=True, staff=True, review=True, recurring=3, startup=2) == 2
assert qualified_ordinary(elected=False, staff=True, review=True, recurring=3, startup=2) == 0
assert qualified_ordinary(elected=True, staff=True, review=True, recurring=3, startup=1) == 0
assert qualified_ordinary(elected=True, staff=True, review=False, recurring=3, startup=2) == 0

print("Qualified independent mutual aid plus public cover reaches both visits.")
print("A shared roster or concurrent origin claim leaves one visit exposed; ordinary public provision needs its own vote and startup cash.")
