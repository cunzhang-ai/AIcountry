"""Check the constructed funding and essential-cost accounts."""

base_resources = (106, 106, 113)
base_prices = (110, 112, 112)
supplements = (4, 6, 0)
execution_cost = 2
programme_cost = sum(supplements) + execution_cost


def essential_gaps(*, received, shifted_costs):
    return tuple(
        max(0, price + shift - available - grant)
        for price, shift, available, grant in zip(
            base_prices, shifted_costs, base_resources, received, strict=True
        )
    )


no_grants = (0, 0, 0)
unchanged_prices = (0, 0, 0)
assert essential_gaps(received=no_grants, shifted_costs=unchanged_prices) == (4, 6, 0)

charge_burden = (3, 5, 2)
assert sum(charge_burden) + 2 == programme_cost == 12
charge_gaps = essential_gaps(received=supplements, shifted_costs=charge_burden)
assert charge_gaps == (3, 5, 1)
assert sum(charge_gaps) + programme_cost == 21
assert essential_gaps(received=supplements, shifted_costs=unchanged_prices) == (0, 0, 0)
assert essential_gaps(received=supplements, shifted_costs=(0, 2, 0)) == (0, 2, 0)
# An unlawful charge is a cash loss until the refund actually arrives.
assert essential_gaps(received=supplements, shifted_costs=(0, 0, 2)) == (0, 0, 1)
assert essential_gaps(received=supplements, shifted_costs=(0, 0, 0)) == (0, 0, 0)


def qualifies_at_cutoff(*, receipts, available_margin, shifted_costs):
    return (
        receipts + available_margin >= programme_cost
        and not any(essential_gaps(received=supplements, shifted_costs=shifted_costs))
    )


assert qualifies_at_cutoff(receipts=12, available_margin=0, shifted_costs=unchanged_prices)
assert not qualifies_at_cutoff(receipts=9, available_margin=0, shifted_costs=unchanged_prices)
assert qualifies_at_cutoff(receipts=9, available_margin=3, shifted_costs=unchanged_prices)
assert not qualifies_at_cutoff(receipts=12, available_margin=0, shifted_costs=(0, 2, 0))

print("The balanced 12-unit charge leaves essential gaps of 3, 5 and 1.")
print("The owner-side alternative covers the basket only with timely cash and qualified incidence.")
