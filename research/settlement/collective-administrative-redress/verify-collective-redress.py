"""Check the constructed redress population and receipt accounting."""

operational = set(range(1, 101))
independent = set(range(96, 121))
known = operational | independent
assert len(operational & independent) == 5
assert len(known) == 120
assert len(known - operational) == 20

verified = set(range(1, 9)) | set(range(101, 108))
returned = {105, 106, 107}
alternates_received = {105, 106}
estates = {108, 109}
unresolved = set(range(110, 114))
potential_recoveries = {101, 114, 115, 116, 117}
principal = 50

assert verified | estates | unresolved | potential_recoveries <= known
assert len(verified & operational) * principal == 400
assert len(verified - operational) * principal == 350
assert len(verified) * principal == 750
assert (len(verified) + len(estates)) * principal == 850
assert verified & potential_recoveries == {101}
assert alternates_received <= returned <= verified - operational

first_receipts = verified - returned
assert len(first_receipts) * principal == 600
assert len(verified - first_receipts) * principal == 150
actual_receipts = first_receipts | alternates_received
assert len(actual_receipts) * principal == 700
assert len(verified - actual_receipts) * principal == 50
assert len(actual_receipts) + len(verified - actual_receipts) == len(verified)
assert not estates & actual_receipts
print("Redress comparison passed: roster, lawful principal, returned transfers and open claims.")
