#!/usr/bin/env python3
"""Reproduce the constructed deadlines, coverage bounds and budget."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Review:
    scheduled_anniversary: int
    enactment_limit: int
    qualified_finding_receipt: int

    @property
    def first_disposition(self) -> int:
        return min(self.scheduled_anniversary, self.enactment_limit)

    @property
    def response_due(self) -> int:
        return self.qualified_finding_receipt + 30

    @property
    def finding_disposition_due(self) -> int:
        return self.qualified_finding_receipt + 60


review = Review(730, 1000, 700)
assert review.first_disposition == 730
assert review.first_disposition - 60 == 670
assert review.response_due == 730
assert review.finding_disposition_due == 760
assert Review(1100, 1000, 700).first_disposition == 1000

eligible = 100
observed = 80
timely_in_channel = 76
verified_late_outside = 12
unknown_outside = eligible - observed - verified_late_outside
timely_bounds = (timely_in_channel, timely_in_channel + unknown_outside)

assert timely_in_channel / observed == 0.95
assert timely_bounds == (76, 84)
assert 90 - timely_bounds[1] == 6

budget = 10
repair, review_access, staff_overlap, expansion = 6, 2, 2, 4
assert repair + review_access + staff_overlap == budget
assert repair + review_access + staff_overlap + expansion > budget

print("Review day 730 retained; separate finding disposition day 760 if unresolved.")
print("Matched timely repairs 76–84 of 100; repair, scrutiny and overlap fill 10 units.")
