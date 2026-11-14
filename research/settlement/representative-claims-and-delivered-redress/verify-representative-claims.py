#!/usr/bin/env python3
"""Check the constructed scope, recovery and time protections."""

members, outsiders = 10, 3
same_loss = 2
earlier_received = 2 * same_loss
earlier_promised_only = same_loss
established = members * same_loss
to_distribute = established - earlier_received
returned = 2 * same_loss
new_received = to_distribute - returned
total_received = earlier_received + new_received

assert members + outsiders == 13
assert (established, to_distribute) == (20, 16)
assert to_distribute - earlier_promised_only == 14  # Incorrect if used as payable amount.
assert (new_received, total_received, established - total_received) == (12, 16, 4)
assert established - total_received == returned


def protected_days(original_remaining: int) -> int:
    return max(original_remaining, 60)


assert protected_days(15) == 60
assert protected_days(75) == 75

print("Ten opt-ins; three outsiders retain their cases. Sixteen units sent, twelve newly received, four still due.")
print("A narrowing order preserves 60 days in the first timely case and 75 in the second.")
