"""Test the declared timing, review and severance choices in the worked case."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    heard_with_independent_counsel: bool
    unsupported_part_dismissed: bool
    private_claim_remains_open: bool
    relief_received_before_hearing: bool


def compare(
    available_units: int,
    *,
    review_day: int = 4,
    delivered_day: int = 5,
    independent_review: bool = True,
    private_claim_supported: bool = True,
) -> Result:
    qualified_review = available_units >= 5 and independent_review
    timely_relief = (
        qualified_review
        and available_units >= 6
        and review_day <= delivered_day < 6
    )
    return Result(
        heard_with_independent_counsel=qualified_review,
        unsupported_part_dismissed=qualified_review,
        private_claim_remains_open=private_claim_supported or not qualified_review,
        relief_received_before_hearing=timely_relief,
    )


assert compare(6) == Result(True, True, True, True)
assert compare(5) == Result(True, True, True, False)
assert compare(6, review_day=12, delivered_day=13) == Result(True, True, True, False)
assert compare(6, independent_review=False) == Result(False, False, True, False)
assert compare(6, private_claim_supported=False) == Result(True, True, False, True)

print('With six funded units, the unsupported demand ends and the genuine claim remains reviewable.')
print('With five units or late delivery, the court result does not preserve the public hearing.')
