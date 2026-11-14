"""Check dated verification and distinct execution in the constructed exercise."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Remedy:
    person: str
    deadline: int
    required_amount: int


remedies = (
    Remedy("A", 12, 2),
    Remedy("B", 18, 3),
    Remedy("C", 24, 1),
)


def receipts(*, evidence_ready, executed, usable_at):
    return {
        item.person
        for item in remedies
        if item.person in evidence_ready
        and executed.get(item.person, 0) == item.required_amount
        and usable_at.get(item.person, float("inf")) <= item.deadline
    }


available_blocks = 2
all_people = {item.person for item in remedies}
separate_evidence = {item.person for item in remedies[:available_blocks]}
shared_evidence = all_people if available_blocks >= 2 else set()
funded_amounts = {"A": 2, "B": 3, "C": 1}
actual_receipt = {"A": 11, "B": 17, "C": 23}

assert receipts(evidence_ready=separate_evidence, executed=funded_amounts,
                usable_at=actual_receipt) == {"A", "B"}
assert receipts(evidence_ready=shared_evidence, executed=funded_amounts,
                usable_at=actual_receipt) == all_people
assert receipts(evidence_ready=shared_evidence, executed=funded_amounts | {"C": 0},
                usable_at=actual_receipt) == {"A", "B"}
assert receipts(evidence_ready=shared_evidence, executed=funded_amounts,
                usable_at=actual_receipt | {"B": 19}) == {"A", "C"}
assert receipts(evidence_ready={"C"}, executed=funded_amounts,
                usable_at=actual_receipt) == {"C"}

# Cash for the first benefit was fully used. Credit and restricted cash are not reusable.
next_a_due = 2
remaining_a_cash = 2 - funded_amounts["A"]
assert remaining_a_cash == 0
for alternate_cash, independent_slot, receiver_accepts, delivered in (
    (0, True, True, False),
    (2, False, True, False),
    (2, True, False, False),
    (2, True, True, True),
):
    assert (remaining_a_cash + alternate_cash >= next_a_due
            and independent_slot and receiver_accepts) == delivered

print("Separate evidence checks reach two original deadlines. A qualified shared check can reach three.")
print("Missing funding, late execution or inaccessible evidence still defeats the affected remedy.")
