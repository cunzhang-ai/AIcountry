"""Check the constructed election and opening cash comparison."""

TOTAL_SETTLED = 20
RESTRICTED = 4
ORDINARY_DUE = 9
VERIFIED_MAINTENANCE = 5
POSSIBLE_CALL = 3
OPTIONAL_EXPANSION = 4
LATE_RECEIPT_DAY = 8
LATE_RECEIPT_AMOUNT = 3


def general_cash(day):
    late_receipt = LATE_RECEIPT_AMOUNT if day >= LATE_RECEIPT_DAY else 0
    return TOTAL_SETTLED - RESTRICTED + late_receipt


opening_use = ORDINARY_DUE + VERIFIED_MAINTENANCE
assert general_cash(7) - ORDINARY_DUE == 7
assert general_cash(7) - opening_use == 2
assert general_cash(7) - opening_use < OPTIONAL_EXPANSION
assert OPTIONAL_EXPANSION - (general_cash(7) - opening_use) == 2

adverse_use = opening_use + POSSIBLE_CALL
assert general_cash(6) - adverse_use == -1
assert general_cash(7) - adverse_use == -1
assert general_cash(8) - adverse_use == 2

first_ballot = 0
verified_working_day = -3
publication_working_day = verified_working_day + 2
assert publication_working_day == -1 < first_ballot

print("Election fiscal comparison passed: dated changes, restricted cash and first-week duties.")
