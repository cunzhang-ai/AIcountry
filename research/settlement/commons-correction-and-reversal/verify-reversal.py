"""Check the hypothetical correction's separate acts and capacity."""

from itertools import combinations


pending_defective = 12
already_deducted = 8
stopped_at_controller = 11
verified_lawful = 5

new_deductions = pending_defective - stopped_at_controller
assert new_deductions == 1
deductions_requiring_review = already_deducted + new_deductions
assert deductions_requiring_review == 9
assert deductions_requiring_review - 7 == 2
assert verified_lawful == 5

affected_bookings = 6
confirmed_repaired_bookings = 5
intersection_people = 4
assert affected_bookings - confirmed_repaired_bookings == 1
assert deductions_requiring_review + affected_bookings - intersection_people == 11

remedial_dispatch = {"block-d"}
next_ordinary_dispatch = {"block-d"}
additional_accepted = {"block-next"}
assert len(remedial_dispatch | next_ordinary_dispatch) < 2
assert len(remedial_dispatch | additional_accepted) == 2

both_need = set(range(intersection_people))
deduction_people = set(range(deductions_requiring_review))
booking_people = both_need | {9, 10}
joint_received = {
    len(set(paid) & set(trips) & both_need)
    for paid in combinations(deduction_people, 7)
    for trips in combinations(booking_people, 5)
}
assert joint_received == {1, 2, 3, 4}

due_to_exit = {"continuity": 3, "resident restoration": 2, "closeout": 1}
cash_on_time = 5
assert sum(due_to_exit.values()) - cash_on_time == 1

next_peak = 6
lead_weeks = 4
assert next_peak - lead_weeks == 2
assert 4 + lead_weeks > next_peak

print("Stops, timely joint receipt, gross exit funds and the last commissioning date checked.")
