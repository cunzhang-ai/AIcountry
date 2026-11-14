"""Check the authored budget and keep lived outcomes distinct from capacity."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    funds: int
    qualified_blocks: int

    def covers(self, requirement):
        return (
            self.funds >= requirement.funds
            and self.qualified_blocks >= requirement.qualified_blocks
        )


@dataclass(frozen=True)
class Motion:
    opening: Window
    next_window: Window
    independent: bool = True

    def qualifies(self, available):
        return (
            self.independent
            and available.opening.covers(self.opening)
            and available.next_window.covers(self.next_window)
        )


available = Motion(Window(8, 5), Window(6, 4))
repair = Motion(Window(5, 3), Window(3, 2))
preparation = Motion(Window(7, 4), Window(4, 3))
paid_release = Motion(Window(8, 5), Window(6, 5))
shared_shortcut = Motion(Window(7, 4), Window(5, 4), independent=False)

assert repair.qualifies(available)
assert preparation.qualifies(available)
assert not paid_release.qualifies(available)
assert not shared_shortcut.qualifies(available)
assert not paid_release.qualifies(Motion(Window(8, 5), Window(7, 4)))
assert paid_release.qualifies(Motion(Window(8, 5), Window(6, 5)))

# Money in the resident's control works only with timely accessible supply.
def achieved(controlled_money, usable_supply, lawful_direct_delivery):
    return lawful_direct_delivery or (controlled_money and usable_supply)


assert achieved(True, True, False)
assert not achieved(True, False, False)
assert not achieved(False, True, False)
assert achieved(False, False, True)

# An increase in unpaid work consumes that person's nominal paid release.
nominal_release = 2
additional_unpaid_care = 2
assert nominal_release - additional_unpaid_care == 0

# A paid-hour reduction has to be usable at the actual pickup cutoff.
required_release = (18 * 60 + 10) - (16 * 60 + 20)
weekly_reduction = 60
assert required_release - weekly_reduction // 5 == 98
assert required_release - weekly_reduction == 50

print("Essential repair and paid preparation fit. Starting paid release requires a separate next-window block.")
