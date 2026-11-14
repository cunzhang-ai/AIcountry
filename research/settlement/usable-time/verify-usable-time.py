"""Check the authored joint time windows and public cost comparison."""

from dataclasses import dataclass


A = frozenset((9, 12, 17, 20))
B = frozenset((9, 10, 17, 18))
REVIEWS = (frozenset((9,)), frozenset((12,)))
LIVE = frozenset((17, 18))
REPLY = frozenset((12, 17))


@dataclass(frozen=True)
class Offer:
    cost: int
    staffed_reply: bool = False
    accepted_relief: bool = False


def review_and_participation(offer, hours, *, fragmented=False):
    if fragmented and offer.accepted_relief:
        hours = hours | {18}
    reviews = tuple(slot for slot in REVIEWS if slot <= hours)
    modes = (LIVE, REPLY) if offer.staffed_reply else (LIVE,)
    can_deliberate = any(
        mode <= hours and mode.isdisjoint(review)
        for review in reviews
        for mode in modes
    )
    return bool(reviews), can_deliberate


def main():
    assert len(A) == len(B) == 4
    common = Offer(3)
    supported = Offer(4, staffed_reply=True)
    relief = Offer(5, accepted_relief=True)

    assert review_and_participation(common, A, fragmented=True) == (True, False)
    assert review_and_participation(common, B) == (True, True)
    assert review_and_participation(supported, A, fragmented=True) == (True, True)
    assert review_and_participation(supported, B) == (True, True)
    assert review_and_participation(relief, A, fragmented=True) == (True, True)
    assert review_and_participation(Offer(5), A, fragmented=True) == (True, False)
    assert review_and_participation(Offer(4), A, fragmented=True) == (True, False)
    assert review_and_participation(supported, A - {9}, fragmented=True) == (True, False)
    assert review_and_participation(supported, A - {9, 12}, fragmented=True) == (False, False)
    assert [offer for offer in (common, supported, relief) if offer.cost <= 4] == [
        common, supported,
    ]
    print('Usable time passed: equal totals, conflicting windows, lawful formats and funded relief.')


if __name__ == '__main__':
    main()
