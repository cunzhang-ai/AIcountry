"""Check the constructive counterexample and the qualified funding boundary."""

def test_shared_dispatch():
    due = 20
    before_a = before_b = 16
    transferred, released = 4, 2
    pilot_a = min(due, before_a + transferred + released)
    exposed_b = before_b - transferred
    assert (pilot_a, exposed_b) == (20, 12)
    assert (pilot_a - before_a) - (exposed_b - before_b) == 8
    assert pilot_a + exposed_b == before_a + before_b == 32
    third_before, third_known, third_unknown = 18, 15, 5
    combined_before = before_a + before_b + third_before
    combined_known = pilot_a + exposed_b + third_known
    assert (combined_known - combined_before, combined_known + third_unknown - combined_before) == (-3, 2)


def test_corrected_schedule():
    continuing_a, restored_b = 18, 16
    restoration, independent_review, price = 2, 1, 3
    base = restoration + independent_review
    for cash, accepted, requested, expected in (
        (8, 2, 2, 18),
        (9, 1, 2, 18),
        (9, 1, 1, 19),
        (9, 2, 2, 20),
    ):
        qualifies = accepted >= requested and cash >= base + requested * price
        assert continuing_a + (requested if qualifies else 0) == expected
        assert restored_b == 16


if __name__ == "__main__":
    test_shared_dispatch()
    test_corrected_schedule()
    print("Shared dispatch: eight apparent relative gains, zero combined change, and a separate funded repair.")
