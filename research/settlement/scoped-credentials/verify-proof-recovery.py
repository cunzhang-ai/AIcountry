"""Reproduce the authored verification capacity and reliance boundaries."""

from collections import Counter

ELECTION_CASES = 20
BENEFIT_CASES = 60
SHARED_RATE = 20
ADDED_COST = {"shared": 4, "independent": 7}


def shared_desk(first_available_hour):
    election = min(ELECTION_CASES, (2 - first_available_hour) * SHARED_RATE)
    benefit = min(BENEFIT_CASES, (4 - first_available_hour) * SHARED_RATE - election)
    return election, benefit


def independent_desk(first_benefit_hour):
    election = min(ELECTION_CASES, 2 * 10)
    benefit = min(BENEFIT_CASES, (4 - first_benefit_hour) * 20)
    return election, benefit


def complete_backups(budget):
    return [name for name, check in (
        ("shared", shared_desk), ("independent", independent_desk)
    ) if ADDED_COST[name] <= budget
        and all(check(start) == (ELECTION_CASES, BENEFIT_CASES) for start in (0, 1))]


def cached_status_usable(hours_since_check, expires_after_hours,
                         known_compromise=False, reserved_act=False):
    return (
        not known_compromise and not reserved_act
        and 0 <= hours_since_check < min(24, expires_after_hours)
    )


if __name__ == "__main__":
    assert shared_desk(0) == (20, 60)
    assert shared_desk(1) == (20, 40)
    assert independent_desk(1) == (20, 60)
    assert complete_backups(7) == ["independent"]
    assert complete_backups(6) == []

    shifts_with_same_worker = Counter(range(0, 2))
    shifts_with_same_worker.update(range(1, 4))
    assert shifts_with_same_worker[1] == 2

    assert cached_status_usable(23, 30)
    assert not cached_status_usable(24, 30)
    assert not cached_status_usable(6, 6)
    assert not cached_status_usable(1, 30, known_compromise=True)
    assert not cached_status_usable(1, 30, reserved_act=True)

    proved_settlement = 8
    proposed_redirect = 40
    current_independent_authority = False
    payable_redirection = proposed_redirect if current_independent_authority else 0
    assert (proved_settlement, payable_redirection) == (8, 0)
    print("Shared desk with access loss: 20 election and 40 benefit checks.")
    print("Independent routes: all 80 checks at 7 added units. None complete at 6.")
    print("Settled 8 retained; unverified redirection of 40 left unexecuted.")
