"""Check the authored transport, housing and finance comparison."""
ORIGINAL = set(range(1, 11))
EARLY_FUNDS = 14
REPAIR = 8
FEEDER = 3
HOUSING = 3
EXTENSION = 18
LATER_RECEIPTS = (7, 4)


def usable_original_access(reachable, stable_housing):
    return len(ORIGINAL & reachable & stable_housing)


def check_comparison():
    currently_reachable = {1, 2, 3, 4}
    feeder_reachable = set(range(1, 8))
    extension_reachable = set(range(1, 10))
    displaced = {6, 7, 8, 9}
    assert usable_original_access(currently_reachable, ORIGINAL) == 4
    assert usable_original_access(feeder_reachable, ORIGINAL) == 7
    assert usable_original_access(extension_reachable, ORIGINAL - displaced) == 5
    assert usable_original_access(extension_reachable, ORIGINAL) == 9

    assert REPAIR + FEEDER + HOUSING == EARLY_FUNDS
    assert EXTENSION > EARLY_FUNDS
    extension_gap = EXTENSION + HOUSING - EARLY_FUNDS
    assert extension_gap == 7
    assert [max(0, extension_gap - receipt) for receipt in LATER_RECEIPTS] == [0, 3]
    # These receipts arrive after the deadline. They can repay separately
    # authorized debt, but do not increase the funds available before it.
    assert EARLY_FUNDS < EXTENSION + HOUSING
    assert EARLY_FUNDS + 7 == EXTENSION + HOUSING


if __name__ == "__main__":
    check_comparison()
    print("The 14-unit option reaches seven original households. The unfunded bare extension reaches five after displacement.")
    print("The protected extension needs seven early units. Weak later receipts leave three of that principal uncovered.")
