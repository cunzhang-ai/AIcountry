"""Check the illustrative repair release and distinct temporary housing."""

TEMPORARY_HOUSING = 6
FIRST_STAGE = 35
SECOND_STAGE = 25
INITIAL_RECEIPT = 40
DISPUTED_BALANCE = 20
MORTGAGE_PRINCIPAL = 80
NOTICE_DAY = 1
PAUSE_DAYS = 30


def repair_gap(cost, usable_cash):
    return max(0, cost - usable_cash)


assert repair_gap(FIRST_STAGE, 0) == 35
assert repair_gap(FIRST_STAGE, INITIAL_RECEIPT) == 0
earmarked_remainder = INITIAL_RECEIPT - FIRST_STAGE
assert earmarked_remainder == 5
assert repair_gap(SECOND_STAGE, earmarked_remainder) == 20
assert repair_gap(SECOND_STAGE, earmarked_remainder + DISPUTED_BALANCE) == 0
assert FIRST_STAGE + SECOND_STAGE == INITIAL_RECEIPT + DISPUTED_BALANCE
assert FIRST_STAGE + SECOND_STAGE + TEMPORARY_HOUSING == 66
assert repair_gap(SECOND_STAGE, earmarked_remainder + TEMPORARY_HOUSING) == 14

expiry_day = NOTICE_DAY + PAUSE_DAYS
assert NOTICE_DAY <= 8 < expiry_day
assert NOTICE_DAY <= 20 < expiry_day
assert expiry_day == 31
assert MORTGAGE_PRINCIPAL > INITIAL_RECEIPT + DISPUTED_BALANCE
print("Disaster repair comparison passed: staged receipt, purpose, shortfall and possession pause.")
