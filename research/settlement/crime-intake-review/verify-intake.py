"""Check authored staff capacity and the useful-time evidence boundary."""

EARLY_HOURS = {"burglary": 2, "harassment": 2, "shop": 2}


def allocate_early(order, hours):
    served = set()
    for case in order:
        required = EARLY_HOURS[case]
        if required <= hours:
            served.add(case)
            hours -= required
    return served


def burglary_rescued_by_alternate(review_completed, independent_hours, shares_failed_root):
    return (
        not shares_failed_root
        and independent_hours >= EARLY_HOURS["burglary"]
        and review_completed + EARLY_HOURS["burglary"] < 8
    )


def main():
    quick_outcome = allocate_early(("shop", "harassment", "burglary"), 4)
    assert quick_outcome == {"shop", "harassment"}
    preferred = allocate_early(("harassment", "burglary", "shop"), 4)
    assert preferred == {"harassment", "burglary"}
    later_hours = 2
    assert preferred | allocate_early(("shop",), later_hours) == set(EARLY_HOURS)

    shared_loss = allocate_early(("harassment", "burglary", "shop"), 2)
    assert shared_loss == {"harassment"}
    assert burglary_rescued_by_alternate(4, 2, False)
    assert not burglary_rescued_by_alternate(7, 2, False)
    assert not burglary_rescued_by_alternate(4, 2, True)
    assert not burglary_rescued_by_alternate(4, 0, False)

    original_family = {"AI summary A": "camera original", "AI summary B": "camera original"}
    assert len(set(original_family.values())) == 1
    print("Quick-outcome ordering loses the burglary lead; useful-time ordering serves all three.")
    print("Two hours lost: earlier harassment remains, and review alone cannot preserve burglary evidence.")
    print("Independent timely alternate works; common failure or late review defeats it.")
    print("Two summaries of the same original are one source family.")


if __name__ == "__main__":
    main()
