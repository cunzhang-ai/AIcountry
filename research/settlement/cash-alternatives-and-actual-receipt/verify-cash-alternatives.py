"""Verify the authored cash, coverage and funding comparisons."""

def coverage(payments):
    return sum(payments), sum(value >= 6 for value in payments), sum(value >= 4 for value in payments)


def main():
    repair = [6, 6, 6, 4]
    universal_others = 8 * 4
    assert coverage([6, 6, 0, 0]) == (12, 2, 2)
    assert coverage(repair) == (22, 3, 4)
    for payments, expected in ((repair, (54, 3, 4)), ([6, 6, 0, 4], (48, 2, 3))):
        total, full, base = coverage(payments)
        assert (total + universal_others, full, base) == expected
    assert coverage([6, 6, 6, 0]) == (18, 3, 3)

    committed = (4 * 6 + 5, 12 * 4 + 4 * 2 + 4)
    assert committed == (29, 60)
    first, later = 40, 20
    assert committed[0] <= first < committed[1] <= first + later
    print("Cash alternatives: proof, payment, protected balance and dated funding passed.")


if __name__ == "__main__":
    main()
