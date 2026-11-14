"""Check the authored monetary choice against actual receipt and dated funds."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Offer:
    domestic_cost: int
    readiness_blocks: int
    second_import_usable: bool = False
    second_household_usable: bool = False
    extra_local_lot: bool = False

    def qualifies(self, minimum_remaining_stock=1):
        if self.domestic_cost > 2 or self.readiness_blocks > 2:
            return False
        accepted_imports = 1 + int(self.second_import_usable)
        local_stock = 1 + int(self.extra_local_lot)
        used_local_stock = min(local_stock, 2 - accepted_imports)
        return (
            accepted_imports + used_local_stock == 2
            and local_stock - used_local_stock >= minimum_remaining_stock
            and self.second_household_usable
        )


def medicine_receipt(accepted_imports, local_stock):
    return min(2, accepted_imports + local_stock)


ordinary = Offer(2, 2, extra_local_lot=True)
independent = Offer(2, 2, second_import_usable=True, second_household_usable=True)
own_currency = Offer(2, 2)
ordinary_with_restored_access = Offer(1, 2, second_household_usable=True, extra_local_lot=True)
correlated_alternate = Offer(2, 2, second_import_usable=False, second_household_usable=True)

assert not ordinary.qualifies()
assert independent.qualifies()
assert not own_currency.qualifies()
assert ordinary_with_restored_access.qualifies()
assert correlated_alternate.qualifies(minimum_remaining_stock=0)
assert not correlated_alternate.qualifies()  # The only physical reserve is consumed.
assert medicine_receipt(accepted_imports=0, local_stock=1) == 1

ordinary_payrolls = (8, 8)
separate_standby = 8
assert sum(ordinary_payrolls) + separate_standby == 24
assert sum(ordinary_payrolls) - separate_standby < sum(ordinary_payrolls)

insured_due = 4
legal_headroom = 4
usable_draw = 3
assert min(legal_headroom, usable_draw) == insured_due - 1

first_wage_due = 1
failure_confirmed = 3
assert failure_confirmed > first_wage_due
assert medicine_receipt(accepted_imports=2, local_stock=1) == 2

print("Independent receiving protects the second call. Insurance and wages have their own timing gaps.")
