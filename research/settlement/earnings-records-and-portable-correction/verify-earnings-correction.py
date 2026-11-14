"""Check covered earnings, actual remittance and matched wage receipt."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Payment:
    event: str
    day: int
    worker_gross: int = 0
    withheld: int = 0
    insurance_cash: int = 0
    treasury_recovery: int = 0


def ledger(events, through_day, covered_gross):
    received = {}
    for event in events:
        if event.day <= through_day:
            assert event.event not in received or received[event.event] == event
            received[event.event] = event
    entries = received.values()
    worker_gross = sum(entry.worker_gross for entry in entries)
    assert worker_gross <= covered_gross
    return (
        covered_gross - worker_gross,
        sum(entry.worker_gross - entry.withheld for entry in entries),
        sum(entry.insurance_cash for entry in entries),
        sum(entry.treasury_recovery for entry in entries),
    )


def main():
    covered = 120
    original = Payment('earlier pay', -10, 60, 6)
    advance = Payment('advance', 7, 40, 4, 4)
    backing = Payment('credit transfer', 10, insurance_cash=3)
    last_pay = Payment('remainder', 20, 20, 2, 2)
    arrears = Payment('late original deduction', 30, insurance_cash=6)
    recovery = Payment('treasury recovery', 30, treasury_recovery=40)
    events = (original, advance, backing, last_pay, arrears, recovery)

    assert (150 - covered, (150 - covered) // 10) == (30, 3)
    assert (150 - original.worker_gross) // 10 == 9
    assert ledger(events, 0, covered) == (60, 54, 0, 0)
    assert ledger(events, 7, covered) == (20, 90, 4, 0)
    assert ledger(events, 10, covered) == (20, 90, 7, 0)
    assert ledger(events, 20, covered) == (0, 108, 9, 0)
    assert ledger(events, 30, covered) == (0, 108, 15, 40)
    assert ledger(events + (advance,), 7, covered) == (20, 90, 4, 0)
    assert ledger((original, backing), 10, covered) == (60, 54, 3, 0)
    assert ledger((original, advance, backing), 20, covered) == (20, 90, 7, 0)
    print('Earnings correction passed: covered work, additional credit and actual matched receipts.')


if __name__ == '__main__':
    main()
