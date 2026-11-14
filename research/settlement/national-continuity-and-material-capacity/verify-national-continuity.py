"""Verify the authored joint operating constraints and the late-loss branch."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    cash: int
    review: int
    dispatch: int
    independent_channels: int = 2

    def gaps(self, limit):
        actual = (self.cash, self.review, self.dispatch, self.independent_channels)
        available = (limit.cash, limit.review, limit.dispatch, limit.independent_channels)
        return tuple(max(0, need - cap) for need, cap in zip(actual, available))


ordinary = (Window(20, 3, 5), Window(20, 3, 5))
adverse = (Window(20, 3, 4), Window(18, 3, 4))
repair = (Window(15, 3, 3), Window(15, 2, 3))
phased = (Window(17, 3, 3), Window(19, 3, 5))
faster = (Window(20, 4, 5), Window(17, 2, 3))
local = (Window(17, 3, 3), Window(18, 3, 4))
clear = (0, 0, 0, 0)


def compare(offer, limits):
    return tuple(need.gaps(cap) for need, cap in zip(offer, limits))


assert compare(repair, adverse) == (clear, clear)
assert compare(phased, ordinary) == (clear, clear)
assert compare(phased, adverse) == (clear, (1, 0, 1, 0))
assert compare(faster, adverse) == ((0, 1, 1, 0), clear)
assert faster[0].gaps(Window(20, 4, 4)) == (0, 0, 1, 0)
assert compare(local, adverse) == (clear, clear)
assert local[1].gaps(Window(18, 3, 4, independent_channels=1)) == (0, 0, 0, 1)
assert phased[1].gaps(Window(18, 3, 5)) == (1, 0, 0, 0)
assert phased[1].gaps(Window(19, 3, 4)) == (0, 0, 1, 0)
assert phased[1].gaps(Window(19, 3, 5)) == clear


# A binding cost and inaccessible booked slot survive the failed offer.
replacement_with_binding_uses = Window(19 + 1, 3, 5 + 1)
assert replacement_with_binding_uses.gaps(adverse[1]) == (2, 0, 2, 0)


def later_disposition(authority, accepted, binding):
    if authority and accepted:
        return "qualified route"
    return "due; remedy continues" if binding else "hold optional start"


assert later_disposition(True, False, False) == "hold optional start"
assert later_disposition(True, False, True) == "due; remedy continues"
print("Joint first and second windows, physical and independent capacity, and open claims verified.")
