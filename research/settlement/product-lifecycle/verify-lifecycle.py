"""Reproduce the authored product service, due funding and material balances."""

COHORT = 100
REPAIR_COST = 2
NEW_COST = 5
TREATMENT_COST = 1


def service_within_window(repairs, replacements):
    return min(COHORT, repairs + replacements)


def full_service_cost(repairs):
    return repairs * REPAIR_COST + (COHORT - repairs) * (NEW_COST + TREATMENT_COST)


if __name__ == "__main__":
    assert service_within_window(60, 40) == COHORT
    assert full_service_cost(0) == 600
    assert full_service_cost(60) == 360
    assert full_service_cost(60) + 100 == 460 < full_service_cost(0)
    assert full_service_cost(60) + 240 == full_service_cost(0)
    assert COHORT - service_within_window(35, 50) == 15
    assert COHORT - service_within_window(0, 50) == 50

    owner_repair = 40 * REPAIR_COST
    funded_replacement = 40 * NEW_COST
    producer_due = 20 * REPAIR_COST + 40 * TREATMENT_COST
    assert owner_repair + funded_replacement + producer_due == 360
    assert producer_due == 80
    assert producer_due - (60 + 20) == 0
    assert producer_due - (60 + 15) == 5

    # Continuing use, recovered output, treated residue, loss, unresolved.
    qualified_domestic = (60, 24, 12, 4, 0)
    export_without_receipt = (60, 12, 6, 2, 20)
    assert sum(qualified_domestic) == sum(export_without_receipt) == 100
    assert qualified_domestic[1] - export_without_receipt[1] == 12
    print("600 versus 360. Loss of parts leaves 15 users without service.")
    print("Producer duty 80. Assurance 60 and bridge 15 leave 5 unpaid.")
    print("Unverified export leaves 20 kg unresolved and only 12 kg recovered.")
