"""Check the scope, paid work and usable receipts in the constructed case."""

known_awards = {name: 2 for name in "ABCDE"}
estate_due = 2
paid_blocks = 5
protected_blocks = 3  # Urgent D, uncertain C and independent outside-roster search F.
available_blocks = paid_blocks - protected_blocks


def first_receipts(work, *, confidential_route):
    assert len(work) <= available_blocks
    received = {"D"}
    for release in work:
        assert received.isdisjoint(release)
        if release == {"E"} and not confidential_route:
            continue  # The attempted contact consumed its allocation.
        received.update(release)
    return sum(known_awards[name] for name in received)


assert sum(known_awards.values()) + estate_due == 12
assert first_receipts(({"A"}, {"B"}), confidential_route=True) == 6
assert first_receipts(({"A"}, {"E"}), confidential_route=True) == 6
assert first_receipts(({"A", "B"},), confidential_route=True) == 6
assert first_receipts(({"A", "B"}, {"E"}), confidential_route=True) == 8
assert first_receipts(({"A", "B"}, {"E"}), confidential_route=False) == 6


def later_outcome(*, proves_nonpayment, estate_authority, cash, release_blocks):
    established = [
        amount for amount, proved in (
            (known_awards["C"], proves_nonpayment), (estate_due, estate_authority)
        ) if proved
    ]
    used = 0
    for amount in established[:release_blocks]:
        if used + amount <= cash:
            used += amount
    return used, sum(established) - used


assert later_outcome(proves_nonpayment=False, estate_authority=False, cash=4, release_blocks=2) == (0, 0)
assert later_outcome(proves_nonpayment=True, estate_authority=True, cash=4, release_blocks=2) == (4, 0)
assert later_outcome(proves_nonpayment=True, estate_authority=True, cash=4, release_blocks=1) == (2, 2)
assert later_outcome(proves_nonpayment=True, estate_authority=True, cash=2, release_blocks=2) == (2, 2)

print("Separate releases reach three people and 6. A qualified batch and safe route reach four and 8.")
print("Open proofs stay outside later payable totals until qualified; cash and release blocks limit actual payment.")
