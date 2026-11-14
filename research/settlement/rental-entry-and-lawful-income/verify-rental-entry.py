"""Reproduce the authored rental entry and payment boundaries."""


def timely_lets(qualified_units, inspection_slots, usable_cash, public_cost):
    return min(qualified_units, inspection_slots, usable_cash // public_cost)


applicants = 12
advertised, unavailable, unsuitable = 10, 3, 2
possible = advertised - unavailable - unsuitable
assert possible == 5

rent, binding_public_share, verification = 10, 6, 1
household_share = rent - binding_public_share
per_let = binding_public_share + verification
envelope = 21
assert household_share == 4
assert 3 * per_let == envelope
assert possible * per_let == 35
assert timely_lets(possible, 3, envelope, per_let) == 3
assert applicants - possible == 7
assert possible - 3 == 2
assert applicants - timely_lets(possible, 3, envelope, per_let) == 9
assert timely_lets(possible, 2, envelope, per_let) == 2
assert envelope - 2 * per_let == 7
assert timely_lets(possible, 5, envelope, per_let) == 3
print("Rental entry: lawful split liability, qualified stock, inspection and timed cash passed.")
