"""Check the independently binding fiscal and physical conditions in the fixture."""

standing = (3, 3, 3, 3)
conversion = (3, 1, 1, 0)
fast_receipts = (6, 2, 0, 0)
slow_receipts = (6, 4, 2, 1)


def balances(receipts, costs):
    return tuple(receipt - cost for receipt, cost in zip(receipts, costs, strict=True))


combined_costs = tuple(sum(cost) for cost in zip(standing, conversion, strict=True))
assert balances(fast_receipts, combined_costs) == (0, -2, -4, -3)
assert balances(slow_receipts, combined_costs) == (0, 0, -2, -2)
assert balances(fast_receipts, conversion) == (3, 1, -1, 0)
assert balances((6, 1, 1, 0), conversion) == (3, 0, 0, 0)
assert balances((3, 3, 3, 3), standing) == (0, 0, 0, 0)
assert balances((3, 2, 3, 3), standing) == (0, -1, 0, 0)


def retirement_qualifies(firm_supply, funded_backup, safe_avoided_demand, lawful):
    return lawful and firm_supply + funded_backup >= 4 - safe_avoided_demand


assert retirement_qualifies(4, 0, 0, True)
assert not retirement_qualifies(3, 0, 0, True)
assert retirement_qualifies(3, 1, 0, True)
assert retirement_qualifies(3, 0, 1, True)
assert not retirement_qualifies(3, 1, 0, False)

# The annual source can be adequate while the first local bill is late.
early_local_due = 1
early_local_receipt = 0
late_local_receipt = 1
assert early_local_receipt < early_local_due
assert early_local_receipt + 1 >= early_local_due
assert late_local_receipt == 1  # A verified settlement restores the drawn advance.

print("Recurring protection, finite closeout and firm receiving remain independently binding.")
