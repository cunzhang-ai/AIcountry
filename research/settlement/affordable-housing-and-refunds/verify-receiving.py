"""Reconcile the public lines and exercise the separate authored lease conditions."""

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import json


observations_file = (
    Path(__file__).resolve().parents[2]
    / "2026-11-affordable-housing-and-refund-exposure"
    / "observations.json"
)
observations = json.loads(observations_file.read_text())
accounts = {name: Decimal(amount) for name, amount in observations["demand_driven_transfers"].items()}
lost_receipts = accounts["budget_receipts"] - accounts["outturn_receipts"]
lower_expense = accounts["budget_expense"] - accounts["outturn_expense"]
assert (lost_receipts, lower_expense) == (Decimal("27.3"), Decimal("6.1"))
assert lost_receipts - lower_expense == Decimal("21.2")
assert accounts["reported_net_overspend"] - (lost_receipts - lower_expense) == Decimal("0.1")
assert accounts["budget_central_reimbursement_receipts"] - accounts[
    "outturn_central_reimbursement_receipts"
] == Decimal("27.2")
assert observations["other_social_services_appropriation"]["matched_housing_first_net_cost"] is None

allocation = observations["social_allocation_2025"]
return_share = Decimal(100 * allocation["units_returned"]) / allocation[
    "units_received_excluding_named_municipal_route"
]
assert return_share.quantize(Decimal("0.1")) == Decimal("20.6")
assert allocation["paired_cohort_sustained_tenancies"] is None


@dataclass(frozen=True)
class Offer:
    housing_charges: int
    usable_resources: int
    initial_aid: int
    after_expiry_aid: int
    upfront_cash: int
    prior_commitment: bool


def qualify(offer):
    return (
        not offer.prior_commitment
        and offer.housing_charges <= offer.usable_resources + offer.initial_aid
        and offer.housing_charges <= offer.usable_resources + offer.after_expiry_aid
    )


def can_open(offers, effective_vote, cash_on_time):
    return (
        effective_vote
        and all(qualify(offer) for offer in offers)
        and sum(offer.upfront_cash for offer in offers) <= cash_on_time
    )


a = Offer(4, 4, 0, 0, 2, False)
b = Offer(7, 5, 2, 0, 3, False)
c = Offer(3, 3, 0, 0, 2, True)
continued_b = Offer(7, 5, 2, 2, 3, False)
cleared_c = Offer(3, 3, 0, 0, 2, False)
assert not can_open((a, b, c), True, 7)
assert not can_open((a, b), True, 7)
assert not can_open((a, c), True, 7)
assert not can_open((a,), False, 7)
assert can_open((a,), True, 4)
assert not can_open((a, continued_b), True, 4)
assert can_open((a, continued_b), True, 5)
assert can_open((a, continued_b, cleared_c), True, 7)

print("Housing receiving passed. The account residual, affordability boundary, prior claim and cash timing remain distinct.")
