"""Check the authored first and next-window resource constraints."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    funds: int
    qualified_access_blocks: int

    def covers(self, costs):
        return (
            self.funds >= costs.funds
            and self.qualified_access_blocks >= costs.qualified_access_blocks
        )


def qualifies(requirements, resources):
    return all(
        available.covers(needed)
        for available, needed in zip(resources, requirements, strict=True)
    )


resources = (Window(8, 2), Window(7, 2))
repair = (Window(4, 1), Window(4, 1))
care = (Window(7, 2), Window(7, 2))
learning = (Window(7, 2), Window(6, 2))
both = (Window(11, 3), Window(12, 3))

assert qualifies(repair, resources)
assert qualifies(care, resources)
assert qualifies(learning, resources)
assert not qualifies(both, resources)
assert not qualifies(both, (Window(11, 3), Window(12, 2)))
assert qualifies(both, (Window(11, 3), Window(12, 3)))

# A protected school correction uses an additional block already due.
after_standing_correction = (Window(7, 1), Window(7, 2))
assert qualifies(repair, after_standing_correction)
assert not qualifies(care, after_standing_correction)
assert not qualifies(learning, after_standing_correction)
assert not qualifies(care, (Window(8, 2), Window(6, 2)))
assert qualifies(learning, (Window(8, 2), Window(6, 2)))

def overlaps(first, second):
    return max(first[0], second[0]) < min(first[1], second[1])


def lawful_match(national_text, local_text, verified_day, deadline):
    return national_text == local_text and verified_day <= deadline


assert overlaps((3, 6), (1, 4))
assert overlaps((3, 6), (4, 7))
assert not overlaps((1, 4), (4, 7))
assert sum((2, 2)) == 4 < sum((2, 2, 2))
assert lawful_match("H", "H", 9, 10)
assert not lawful_match("H", "amended H", 9, 10)
assert not lawful_match("H", "H", 11, 10)

print("Both optional starts require distinct capacity. A binding school repair changes the opening choice.")
