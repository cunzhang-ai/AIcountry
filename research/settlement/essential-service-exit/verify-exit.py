"""Reproduce the ordered amount and a distinct authored service budget."""

import json
from pathlib import Path


def ordered_refund():
    records = Path(__file__).resolve().parents[2] / "2026-11-essential-service-exit-and-recovery"
    record = json.loads((records / "observations.json").read_text())
    certified = sum(record["certified_periods"])
    assert certified == record["certified_profit"] == 252590152
    adjustments = record["retrenchment_adjustment"] + sum(record["empowerment_adjustments"])
    overlap = record["prior_judgment_principal"] + record["interest_to_terminal_profit_date"]
    assert overlap == 528994505
    ordered = certified + adjustments - overlap - record["work_not_performed_claim"]
    assert ordered == record["ordered_adjusted_profit_refund"] == 81286177
    later_overlap = record["prior_judgment_proved_claim_including_later_interest"]
    assert certified + adjustments - later_overlap - record["work_not_performed_claim"] != ordered
    assert record["actual_refund_collected"] is None
    print("ZAR 81,286,177 ordered after period-specific adjustments. Actual collection remains unknown.")


def reachable_receipt(alternate, residual, ordinary_proof, residual_proof):
    alternate_receipt = alternate if ordinary_proof else 0
    residual_receipt = residual if residual_proof else 0
    return alternate_receipt + residual_receipt


def operating_cash_by(day, receipts):
    return sum(amount for receipt_day, amount in receipts if receipt_day <= day)


def authored_choice():
    award = 100
    alternate, residual = 70, 30
    assert alternate + residual == award
    assert reachable_receipt(alternate, 0, True, False) == 70
    assert reachable_receipt(alternate, residual, True, True) == 100
    assert reachable_receipt(alternate, residual, False, False) == 0
    assert reachable_receipt(alternate, residual, True, False) == 70

    successor, independent_verifier = 5, 2
    whole_incumbent, residual_incumbent = 10, 6
    split_cost = successor + independent_verifier + residual_incumbent
    assert split_cost == 13
    assert successor + independent_verifier + whole_incumbent == 17
    delayed_operating_receipts = ((4, 5), (10, 6), (15, 2))
    assert operating_cash_by(4, delayed_operating_receipts) == successor
    due_day_cash = operating_cash_by(10, delayed_operating_receipts)
    assert split_cost - due_day_cash == 2
    assert split_cost - operating_cash_by(15, delayed_operating_receipts) == 0

    new_operator_acceptance = 4 + 20
    assert new_operator_acceptance == 24 < 30 < 35
    refund_claim, refund_receipt_day, refund_collected = 8, 36, 2
    assert refund_receipt_day > 35
    assert refund_claim - refund_collected == 6
    print("A 70/30 split reaches all 100 only with independent proof, actual funding and accepted routes.")
    print("The split needs 13 by day 10, leaving a two-unit early gap when cash arrives on day 15.")
    print("Two later recovery units leave six outstanding and cannot fund earlier delivery.")


if __name__ == "__main__":
    ordered_refund()
    authored_choice()
