"""Reconcile formally reported and verified service dependence in one window."""
REPORTED_WORK = {"income support": 6}
VERIFIED_WORK = REPORTED_WORK | {"education access": 5}
BASE_ROUTE = {"ordinary service group": 8}
INDEPENDENT_ADDITION = {"separate qualified group": 3}


def uncovered(duties, routes):
    capacities = {}
    for group, accepted_slots in routes:
        if group in capacities:
            assert capacities[group] == accepted_slots
        capacities[group] = accepted_slots
    return max(0, sum(duties.values()) - sum(capacities.values()))


def check_common_loss():
    ordinary = tuple(BASE_ROUTE.items())
    independent = tuple(INDEPENDENT_ADDITION.items())
    assert uncovered(REPORTED_WORK, ordinary) == 0
    assert uncovered(VERIFIED_WORK, ordinary) == 3
    assert uncovered(VERIFIED_WORK, ordinary + ordinary) == 3
    assert uncovered(VERIFIED_WORK, ordinary + independent) == 0
    # If new qualified capacity is not accepted, postponing an unrelated launch
    # leaves the original combined workload and actual alternative unchanged.
    assert uncovered(VERIFIED_WORK, ordinary) == 3


if __name__ == "__main__":
    check_common_loss()
    print("The recorded six checks fit. Eleven actual checks leave three due with eight independent slots.")
    print("A duplicate reserve adds nothing. Three distinct accepted slots close the constructed gap.")
