"""Continue the opening case and compare the year-two payment windows."""

import runpy
from pathlib import Path


def main():
    prior = Path(__file__).resolve().parents[1] / "joined-opening-budget-and-release"
    ledger = runpy.run_path(str(prior / "verify-joined-opening.py"))
    transfer, balances = ledger["Transfer"], ledger["balances"]
    opening = {"Treasury": 1, "Local": 0, "Pension": 0, "Operator": 0}

    def window(cash, name, receipts, central_due, service_due):
        transfers = [transfer(f"{name}-{payer}", payer, due) for payer, due in service_due.items()]
        external_net = {payer: -due for payer, due in service_due.items()}
        external_net["Treasury"] = receipts - central_due
        return balances(cash, external_net, transfers)

    first_year = window(opening, "R", 18, 9, {"Local": 3, "Pension": 3, "Operator": 2})
    assert first_year == opening | {"Treasury": 2}
    early_due = {"Local": 2, "Pension": 2, "Operator": 1}
    late_due = {"Local": 3, "Pension": 2, "Operator": 2}

    def year_two(early_receipts, late_receipts, early_due_extra=0, late_due_extra=0):
        early = window(first_year, "A", early_receipts, 8 + early_due_extra, early_due)
        late = window(early, "B", late_receipts, 8 + late_due_extra, late_due)
        return early["Treasury"], late["Treasury"]

    assert year_two(12, 18) == (1, 4)
    assert year_two(12, 18, 1, 2) == (0, 1)
    assert year_two(12, 18, 4, 2) == (-3, -2)
    assert year_two(9, 21) == (-2, 4)
    assert year_two(9 + 3, 21, late_due_extra=4) == (1, 3)
    assert year_two(9 + 3, 18, late_due_extra=4) == (1, 0)
    assert year_two(9, 21, early_due_extra=-3, late_due_extra=4) == (1, 3)
    print("Second year: same payers, renewal timing and repeat-delay stress passed.")


if __name__ == "__main__":
    main()
