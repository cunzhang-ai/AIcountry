"""Check timely reservations, independent prerequisites and protected slots."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    room_hold_expiry: float = 3
    care_hold_expiry: float = 4
    transport_hold_expiry: float = 5
    common_scope: bool = True
    consent: bool = True
    inspection_needed: bool = False
    inspection_done: bool = False
    transfer_needed: bool = False
    transfer_authorized: bool = False
    transfer_funds: int = 0
    transfer_workers: int = 0

    def qualifies(self, confirmations):
        deadlines = (self.room_hold_expiry, self.care_hold_expiry, self.transport_hold_expiry)
        return (
            len(confirmations) == len(deadlines)
            and max(confirmations) < min(deadlines)
            and self.common_scope
            and self.consent
            and (not self.inspection_needed or self.inspection_done)
            and (
                not self.transfer_needed
                or self.transfer_authorized and self.transfer_funds >= 1 and self.transfer_workers >= 1
            )
        )


on_time = (2, 2, 2)
assert 2 + 3 + 2 == 7
assert Route().qualifies(on_time)
assert not Route().qualifies((2, 3.5, 2))
assert not Route().qualifies((2, 2))
assert not Route(common_scope=False).qualifies(on_time)
assert not Route(consent=False).qualifies(on_time)
assert not Route(inspection_needed=True).qualifies(on_time)
assert Route(inspection_needed=True, inspection_done=True).qualifies(on_time)
assert not Route(transfer_needed=True).qualifies(on_time)
assert not Route(transfer_needed=True, transfer_funds=1, transfer_workers=1).qualifies(on_time)
assert Route(transfer_needed=True, transfer_authorized=True,
             transfer_funds=1, transfer_workers=1).qualifies(on_time)


def second_call(remaining_funds, accepted_workers, origin_commitments):
    return remaining_funds >= 1 and accepted_workers > origin_commitments


assert not second_call(0, 1, 0)
assert not second_call(1, 1, 1)
assert second_call(1, 2, 1)
# A released route can still miss a service deadline at the receiving end.
def timely_receipt(route, confirmations, room_arrival, care_receipt):
    if not route.qualifies(confirmations):
        return False, False
    return room_arrival <= 6, care_receipt <= 7


assert timely_receipt(Route(), on_time, 6, 7) == (True, True)
assert timely_receipt(Route(), on_time, 6, 8) == (True, False)
assert timely_receipt(Route(), (2, 3.5, 2), 6, 7) == (False, False)
print("Common confirmation, independent safety, uncovered authority and second call verified.")
