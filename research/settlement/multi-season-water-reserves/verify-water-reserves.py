"""Check stock conservation and qualified supply in a constructed dry-season case."""

from dataclasses import dataclass

PROTECTED_DEMAND = 38
ECOLOGICAL_FLOW = 12
LOSSES = 2
SUCCESSOR_STOCK = 4


@dataclass(frozen=True)
class Supply:
    volume: int = 0
    independent: bool = False
    funded: bool = False
    timely: bool = False
    usable: bool = False

    @property
    def receipt(self):
        if self.independent and self.funded and self.timely and self.usable:
            return self.volume
        return 0


def season(opening, inflow, *, discretionary=0, external=Supply()):
    available = opening + inflow - ECOLOGICAL_FLOW - LOSSES
    assert available >= 0  # The assumed flows and physical losses fit in this case.
    delivered_external = min(external.receipt, PROTECTED_DEMAND)
    delivered_local = min(PROTECTED_DEMAND - delivered_external, available)
    closing = available - delivered_local - discretionary
    assert closing >= 0
    return delivered_local + delivered_external, closing


def main():
    target = PROTECTED_DEMAND + ECOLOGICAL_FLOW + LOSSES + SUCCESSOR_STOCK - 5
    assert target == 51
    assert season(100, 12) == (38, 60)
    assert season(100, 12, discretionary=60 - target) == (38, 51)

    assert season(100, 12, discretionary=25) == (38, 35)
    assert season(35, 5) == (26, 0)
    assert season(51, 5) == (38, 4)

    independent_source = Supply(16, independent=True, funded=True, timely=True, usable=True)
    assert season(35, 5, external=independent_source) == (38, 4)

    assert season(51, 0) == (37, 0)
    backup = Supply(5, independent=True, funded=True, timely=True, usable=True)
    assert season(51, 0, external=backup) == (38, 4)
    for failed_supply in (
        Supply(5, independent=False, funded=True, timely=True, usable=True),
        Supply(5, independent=True, funded=False, timely=True, usable=True),
        Supply(5, independent=True, funded=True, timely=False, usable=True),
        Supply(5, independent=True, funded=True, timely=True, usable=False),
    ):
        assert season(51, 0, external=failed_supply) == (37, 0)
    print("Water reserves: carryover, protected receipt, successor stock and external supply passed.")


if __name__ == "__main__":
    main()
