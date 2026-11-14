"""Reproduce the authored net-source, debt and liquidity checks."""

standing = (6, 6, 6, 6)
bridge_draw = (6, 0, 0, 0)
principal = (0, 3, 3, 0)
principal_source = (0, 3, 3, 0)
interest = (0, 1, 1, 0)

assert sum(bridge_draw) == sum(principal) == 6
assert sum(interest) == 2
assert principal_source == principal
assert 3 + 2 + 1 == standing[0]
assert (3 + 2 + 1) - 2 + 2 == standing[0]  # Internal backing eliminated.
required = tuple(
    services + fee + debt - dedicated - draw
    for services, fee, debt, dedicated, draw in zip(
        standing, interest, principal, principal_source, bridge_draw
    )
)
assert required == (0, 7, 7, 6)
assert (7 - 1 - 1 + 3, 6 - 1 - 1 + 3) == (8, 7)
assert (10 - 2, 9 - 2) == (8, 7)

choices = {"R": (0, 0), "V": (8, 4), "M": (8, 7), "P": (8, 7), "H": (6 + 2, 5 + 2)}
results = {
    choice: [tuple(net - due for due in required[1:]) for net in net_paths]
    for choice, net_paths in choices.items()
}
assert results["R"] == [(-7, -7, -6), (-7, -7, -6)]
assert results["V"] == [(1, 1, 2), (-3, -3, -2)]
assert results["M"] == results["P"] == results["H"] == [(1, 1, 2), (0, 0, 1)]


assert tuple(6 - due for due in required[1:]) == (-1, -1, 0)
assert tuple(
    services + fee + debt - draw
    for services, fee, debt, draw in zip(standing, interest, principal, bridge_draw)
) == (0, 10, 10, 6)  # If the dedicated principal source fails.


def settlement(early, later, reserve):
    early_gap = max(0, 4 - early)
    draw = min(reserve, early_gap)
    later_surplus = max(0, later - 3)
    restoration = min(later_surplus, draw)
    return early_gap - draw, reserve - draw + restoration


assert settlement(4, 3, 0) == (0, 0)
assert settlement(3, 4, 0) == (1, 0)
assert settlement(3, 4, 1) == (0, 1)
assert settlement(3, 3, 1) == (0, 0)
assert settlement(3, 3, 0) == (1, 0)
# Separate portfolio case, expressed in tenths to keep exact arithmetic.
short_year_one = 30 + 20 - 8
fixed_year_one = 30 + 20 - 12
short_year_two = short_year_one + 10 - 20 - (200 - 150)
fixed_year_two = fixed_year_one + 10 - 12
assert (short_year_one, fixed_year_one) == (42, 38)
assert (short_year_two, fixed_year_two) == (-18, 36)
assert 10 - short_year_two == 28
assert fixed_year_two + 10 - 12 - 100 == -66
assert 12 - 10 == 2  # Permanent gap even when no principal is due.
print("Four-year source and repayment paths, due dates and the second reserve call verified.")
