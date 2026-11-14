"""Reproduce the capacity comparisons of the constructed month."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Month:
    first_fx_day: int
    second_fx_day: int
    extra_import_fx: int = 0
    first_lot_accepted: bool = True
    second_lot_accepted: bool = True
    local_reserve_lots: int = 1


def foreign_receipts(month):
    # The second tranche reserves three units for the foreign-law creditor.
    first_lot = month.first_fx_day <= 5 and month.first_lot_accepted
    debt_on_time = month.second_fx_day <= 12
    second_lot_capacity = int(month.second_fx_day <= 23) + month.extra_import_fx
    second_lot = second_lot_capacity >= 4 and month.second_lot_accepted
    missed_lots = 2 - sum((first_lot, second_lot))
    unmet_treatment_lots = max(0, missed_lots - month.local_reserve_lots)
    return debt_on_time, max(0, 4 - second_lot_capacity), unmet_treatment_lots


predecessor = Month(first_fx_day=5, second_fx_day=16)
external = Month(first_fx_day=5, second_fx_day=12)
own_currency = Month(first_fx_day=5, second_fx_day=16)
assert foreign_receipts(predecessor) == (False, 3, 0)
assert foreign_receipts(external) == (True, 3, 0)
assert foreign_receipts(own_currency) == (False, 3, 0)
assert foreign_receipts(Month(6, 16)) == (False, 3, 1)
assert foreign_receipts(Month(5, 16, first_lot_accepted=False)) == (False, 3, 1)
assert foreign_receipts(Month(5, 16, local_reserve_lots=0)) == (False, 3, 1)
assert foreign_receipts(Month(5, 16, extra_import_fx=3)) == (False, 0, 0)
assert foreign_receipts(Month(6, 16, extra_import_fx=3, second_lot_accepted=False)) == (False, 0, 1)

payroll_released = (8, 8)
payroll_received_days = (2, 15)
assert sum(payroll_released) == 16
assert tuple(received <= due for received, due in zip(payroll_received_days, (1, 15))) == (False, True)
assert 8 / 5 < 8 / 4  # Spending power falls even on the timely payroll.
grocery_calls = (1, 1)
grocery_receipts = (1, 0)
assert tuple(due - received for due, received in zip(grocery_calls, grocery_receipts)) == (0, 1)
insurance_due = 6
insurance_usable_funds_at_deadline = 2
arrears = insurance_due - insurance_usable_funds_at_deadline
assert arrears == 4
facility_ceiling, opening_drawn = 7, 3
assert facility_ceiling - opening_drawn == arrears
insured_balance_deadline = 11
draw_arrival = 18
assert draw_arrival > insured_balance_deadline
settled_draw_on_day_18 = 4
assert opening_drawn + settled_draw_on_day_18 == facility_ceiling
assert arrears - settled_draw_on_day_18 == 0

last_fx = 3
energy_invoice = 3
medicine_gap = 3
assert last_fx < energy_invoice + medicine_gap


def eligible_release(allocation, *, elected_authority):
    return allocation if elected_authority else (0, 0)


assert eligible_release((0, 3), elected_authority=False) == (0, 0)
assert eligible_release((0, 3), elected_authority=True) == (0, 3)
# Each option has one real supply gap before the local reserve is applied.
for medicine_allocation, energy_allocation in ((3, 0), (0, 3)):
    assert medicine_allocation + energy_allocation <= last_fx
    energy_received = energy_allocation >= energy_invoice
    for reserve_qualifies in (True, False):
        medicine_received = medicine_allocation >= medicine_gap or reserve_qualifies
        if not medicine_allocation:
            assert medicine_received == reserve_qualifies
        assert (medicine_received and energy_received) == (
            reserve_qualifies and energy_allocation == energy_invoice
        )

print("An independent route changes debt timeliness, not the 3 F medicine funding gap.")
print("One physical reserve covers one missed lot; even funded imports can miss receipt.")
print("First payroll late; second on time; 4 L insured claims remain due at the balance deadline.")
