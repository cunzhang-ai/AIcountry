"""Check the illustrative public enterprise cash and reserve comparison."""

maintenance_cost = 12
service_cost = 100 + maintenance_cost + 8
outside_receipts = 25 + 5
compensation = service_cost - outside_receipts
paid_compensation = 70
commercial_loss = 30
reserve = 25
earlier_priority_call = 15


def allocate_reserve(usable_reserve, earlier_due, later_due):
    earlier_paid = min(usable_reserve, earlier_due)
    later_paid = min(usable_reserve - earlier_paid, later_due)
    return earlier_paid, later_paid, later_due - later_paid


assert compensation == 90
transit_gap = service_cost - outside_receipts - paid_compensation
assert transit_gap == 20
assert transit_gap == compensation - paid_compensation
assert earlier_priority_call + transit_gap == 35
assert earlier_priority_call + transit_gap > reserve
assert allocate_reserve(reserve, earlier_priority_call, transit_gap) == (15, 10, 10)
assert allocate_reserve(reserve + 10, earlier_priority_call, transit_gap) == (15, 20, 0)
assert allocate_reserve(reserve, earlier_priority_call, transit_gap + commercial_loss) == (15, 10, 40)

# Deferring upkeep creates a nominal surplus while the full offer still lacks cash.
cash_with_partial_bridge = outside_receipts + paid_compensation + 10
assert service_cost - maintenance_cost <= cash_with_partial_bridge < service_cost
print("Public enterprise comparison passed: net cost, dated cash, priority and shared reserve.")
