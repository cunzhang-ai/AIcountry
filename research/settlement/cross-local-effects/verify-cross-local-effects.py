#!/usr/bin/env python3
"""Check the constructed catchment, notice and financing constraints."""

protected_flow = 4
normal_limit = 14 - protected_flow
low_flow_limit = 12 - protected_flow
existing = 5
requested = 3
smaller = 2

assert existing + requested <= normal_limit
assert existing + requested * 2 - normal_limit == 1
assert normal_limit - (existing + smaller * 2) == 1
assert existing <= low_flow_limit < existing + smaller * 2

first_receipt, national_receipt = 0, 8
original_date = min(first_receipt, national_receipt)
assert (original_date + 45, original_date + 90) == (45, 90)

local_funds = 3 + 2
monitoring_due = 2
assert local_funds + monitoring_due == 7
assert local_funds < 7

print("Separate draws appear feasible; the combined request exceeds the limit by one.")
print("The smaller package fits at normal flow but fails at lower flow or with late monitoring funds.")
print("National transfer preserves the original day-45 and day-90 deadlines.")
