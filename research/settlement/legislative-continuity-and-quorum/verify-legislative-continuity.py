#!/usr/bin/env python3
"""Check fixed thresholds, separate attendance and the original fiscal clock."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Sitting:
    present: int
    yes: int

    @property
    def quorate(self) -> bool:
        return self.present >= 51

    @property
    def passes(self) -> bool:
        return self.quorate and self.yes >= 51


assert not Sitting(43, 41).quorate
assert Sitting(52, 49).quorate and not Sitting(52, 49).passes
assert Sitting(53, 51).passes
assert not Sitting(52, 50).passes

full_seats, vacant, accepted_successors = 100, 51, 4
assert full_seats - vacant == 49
assert full_seats - vacant + accepted_successors == 53
assert full_seats // 2 + 1 == 51

standing, bridge = 8, 2


def authorized_operations(day: int) -> int:
    assert day >= 1
    return standing + (bridge if day <= 90 else 0)


assert authorized_operations(1) == 10
assert authorized_operations(90) == 10
assert authorized_operations(91) == 8
assert authorized_operations(120) == 8

print("43 present cannot vote; 52 present and 49 assents cannot pass; 53 present and 51 assents can.")
print("Frozen succession restores occupied seats without lowering 51; bridge operations end before day 91.")
