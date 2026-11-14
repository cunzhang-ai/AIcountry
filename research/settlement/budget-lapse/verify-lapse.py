"""Reproduce the authored Day 91 payment case, without predicting service receipt."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Payment:
    day: int
    line: str
    amount: int
    route: str


DUE = {
    "disability": (91, 4),
    "appeal": (91, 3),
    "water": (91, 2),
    "bridge_hire": (92, 2),
}


def receipts(
    *,
    closeout_enacted=True,
    ordinary_appeal_blocked=False,
    shared_appeal_rail_failed=False,
    water_correction_day=None,
    hire_verified_day=92,
    hire_earned_day=90,
):
    settled = [
        Payment(91, "disability", 4, "standing"),
        Payment(91, "water", 1, "standing"),
    ]

    # One judgment and one restricted balance, even with two eligible signers.
    if not shared_appeal_rail_failed:
        route = "B19 substitute" if ordinary_appeal_blocked else "standing"
        settled.append(Payment(91, "appeal", 3, route))

    hire_payment_day = max(DUE["bridge_hire"][0], hire_verified_day)
    if closeout_enacted and hire_earned_day <= 90 and 91 <= hire_payment_day <= 120:
        settled.append(Payment(hire_payment_day, "bridge_hire", 2, "closeout"))

    if water_correction_day is not None:
        assert water_correction_day >= 91
        settled.append(Payment(water_correction_day, "water", 1, "new appropriation"))

    return settled


def audit(payments):
    by_line = {}
    for line, (due_day, amount) in DUE.items():
        line_receipts = [receipt for receipt in payments if receipt.line == line]
        paid = sum(receipt.amount for receipt in line_receipts)
        timely = sum(receipt.amount for receipt in line_receipts if receipt.day <= due_day)
        assert 0 <= timely <= paid <= amount
        by_line[line] = (timely, amount - timely, amount - paid)
    assert all(receipt.line in by_line for receipt in payments)
    return tuple(sum(column) for column in zip(*by_line.values()))


def main():
    cases = {
        "separate closeout": ({}, (10, 1, 1)),
        "no closeout authority": ({"closeout_enacted": False}, (8, 3, 3)),
        "selective withholding": ({"ordinary_appeal_blocked": True}, (10, 1, 1)),
        "shared rail failure": (
            {"ordinary_appeal_blocked": True, "shared_appeal_rail_failed": True},
            (7, 4, 4),
        ),
        "late water correction": ({"water_correction_day": 93}, (10, 1, 0)),
        "verification on day 121": ({"hire_verified_day": 121}, (8, 3, 3)),
        "verification on day 120": ({"hire_verified_day": 120}, (8, 3, 1)),
        "work performed after expiry": ({"hire_earned_day": 91}, (8, 3, 3)),
    }
    for case, (parameters, expected) in cases.items():
        actual = audit(receipts(**parameters))
        assert actual == expected, (case, actual, expected)
        print(f"{case}: {actual[0]} timely, {actual[1]} missed by due date, {actual[2]} remaining")

    appeal = [p for p in receipts(ordinary_appeal_blocked=True) if p.line == "appeal"]
    assert appeal == [Payment(91, "appeal", 3, "B19 substitute")]


if __name__ == "__main__":
    main()
