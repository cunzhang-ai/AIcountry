"""Reconcile due and received units in the authored award transfer."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Receipt:
    duty: str
    day: int
    amount: int
    source: str


DUTIES = {"benefit": (1, 4), "travel": (1, 2), "care": (1, 3), "review": (2, 1)}


def audit(receipts):
    assert all(receipt.duty in DUTIES for receipt in receipts)
    timely = 0
    for duty, (deadline, due) in DUTIES.items():
        timely_amount = sum(
            receipt.amount
            for receipt in receipts
            if receipt.duty == duty and receipt.day <= deadline
        )
        timely += min(timely_amount, due)
    gross = sum(receipt.amount for receipt in receipts)
    return timely, gross


def main():
    on_time = [
        Receipt("benefit", 1, 4, "ordinary"),
        Receipt("travel", 1, 2, "linked service"),
        Receipt("care", 1, 3, "care service"),
        Receipt("review", 2, 1, "independent review"),
    ]
    others = [receipt for receipt in on_time if receipt.duty != "benefit"]
    assert audit(on_time) == (10, 10)
    assert audit([r for r in on_time if r.duty != "travel"]) == (8, 8)
    assert audit([r for r in on_time if r.duty not in {"travel", "review"}]) == (7, 7)

    late_ordinary = Receipt("benefit", 2, 4, "ordinary")
    assert audit(others + [late_ordinary]) == (6, 10)
    advance = Receipt("benefit", 1, 4, "authorized continuity advance")
    assert audit(others + [advance, late_ordinary]) == (10, 14)
    confirmed_failure = Receipt("benefit", 1, 4, "verified ordinary alternate")
    assert audit(others + [confirmed_failure]) == (10, 10)

    original_filing = -12
    review_day = 2
    increase_decided_day = 4
    increase_paid_day = 5
    increase = 2
    assert original_filing < 1 < review_day < increase_decided_day < increase_paid_day
    assert audit(on_time)[1] + increase == 12

    print("Complete transfer meets 10 units of original duties; missing linked proof leaves 8.")
    print("Dropping the pending review as well leaves 7.")
    print("Late ordinary payment without an advance meets 6 on time.")
    print("With an authorized advance, 10 are timely and gross public cost is 14 before reconciliation.")
    print("The later award increase is separately paid from its lawful date.")


if __name__ == "__main__":
    main()
