"""Check an authored award, exclusive releases and safe receipt."""

from dataclasses import dataclass


AWARD = 120
ALREADY_USABLE = 45
PREVIOUS_INSTRUCTION = 50
ORDINARY_FLOAT = 75
BRIDGE_LIMIT = 20


@dataclass(frozen=True)
class Release:
    authority: int
    available_cash: int
    proof_accepted: bool = True

    @property
    def usable(self):
        return min(self.authority, self.available_cash) if self.proof_accepted else 0


def eligible_release(previous_cancellation_confirmed):
    unavailable = 0 if previous_cancellation_confirmed else PREVIOUS_INSTRUCTION
    return AWARD - ALREADY_USABLE - unavailable


def reconcile(*points, cancelled=False, bridge=0):
    assert sum(point.authority for point in points) <= eligible_release(cancelled)
    assert 0 <= bridge <= BRIDGE_LIMIT
    usable_principal = ALREADY_USABLE + sum(point.usable for point in points)
    return usable_principal, AWARD - usable_principal, usable_principal + bridge


def main():
    assert reconcile() == (45, 75, 45)
    assert eligible_release(False) == 25
    assert ALREADY_USABLE + PREVIOUS_INSTRUCTION + 75 == 170
    assert reconcile(Release(25, ORDINARY_FLOAT)) == (70, 50, 70)
    assert reconcile(Release(25, ORDINARY_FLOAT), bridge=20) == (70, 50, 90)
    assert reconcile(Release(75, ORDINARY_FLOAT), cancelled=True) == (120, 0, 120)
    assert reconcile(Release(75, 25), cancelled=True) == (70, 50, 70)
    assert reconcile(Release(25, 25), Release(50, 50), cancelled=True) == (120, 0, 120)
    assert reconcile(Release(25, 25), Release(50, 50, False), cancelled=True) == (70, 50, 70)

    try:
        reconcile(Release(75, ORDINARY_FLOAT))
    except AssertionError:
        pass
    else:
        raise AssertionError("Unconfirmed cancellation allowed a second release")

    print("Of 120 due, 45 usable and 50 unconfirmed leave 25 safe to release.")
    print("An unguarded copy can release 170; the separate 20 bridge leaves 50 principal unresolved.")
    print("Confirmed cancellation and staffed cash can deliver all 120.")
    print("An exclusive national alternate needs both accepted proof and actual cash.")


if __name__ == "__main__":
    main()
