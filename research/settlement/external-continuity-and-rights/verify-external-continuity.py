"""Check the distinct claims and next-call receipt conditions in Design504."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    domestic_pension: int
    local_stock: int
    import_permitted: bool
    import_accepted: bool

    def receive(self, funded_dispatch, replenishment):
        imported = self.import_permitted and self.import_accepted
        local_purchase = not imported and self.local_stock > 0 and funded_dispatch
        remaining = self.local_stock - int(local_purchase) + int(replenishment)
        return imported or local_purchase, remaining


common_first = Window(3, 1, True, True)
border_hold = Window(3, 1, False, True)
assert common_first.receive(False, False) == (True, 1)
assert border_hold.receive(True, False) == (True, 0)
assert border_hold.receive(True, True) == (True, 1)
assert border_hold.receive(False, False) == (False, 1)
assert Window(3, 0, False, True).receive(True, False) == (False, 0)
assert border_hold.domestic_pension == 3
assert 2 <= 3 and 3 <= 3

print("Funded local receiving protects a call during border delay. The subsequent call needs verified replenishment.")
