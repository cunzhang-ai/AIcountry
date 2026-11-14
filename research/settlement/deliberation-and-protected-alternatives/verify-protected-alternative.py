"""Check support, finite timing and paid exact dispositions in a constructed case."""

SEATS = 24
REPORT_DAY = 80
REPORT_DEADLINE = 90
STANDING_SUPPORT = 3
SUPPORT_PER_TEXT = 2


def qualifies(supporters, *, exact_text, complete):
    return exact_text and complete and len(set(supporters)) * 4 >= SEATS


def completed_dispositions(*, funds, ordinary_votes, alternate_votes):
    deadline = min(REPORT_DAY, REPORT_DEADLINE) + 60
    paid_capacity = max(0, (funds - STANDING_SUPPORT) // SUPPORT_PER_TEXT)
    timely = {text for day, text in ordinary_votes + alternate_votes if day <= deadline}
    return min(paid_capacity, len(timely & {"main", "feeder"}))


def main():
    people = list(range(6))
    assert qualifies(people + [0, 0, 0, 0], exact_text=True, complete=True)
    assert not qualifies(people[:5] + [0], exact_text=True, complete=True)
    assert not qualifies(people, exact_text=False, complete=True)
    assert not qualifies(people, exact_text=True, complete=False)
    assert min(REPORT_DAY, REPORT_DEADLINE) + 60 == 140

    ordinary = [(120, "main"), (120, "merged")]
    assert completed_dispositions(funds=7, ordinary_votes=ordinary, alternate_votes=[]) == 1
    timely_alternate = [(139, "feeder")]
    assert completed_dispositions(funds=7, ordinary_votes=ordinary, alternate_votes=timely_alternate) == 2
    assert completed_dispositions(funds=6, ordinary_votes=ordinary, alternate_votes=timely_alternate) == 1
    assert completed_dispositions(funds=7, ordinary_votes=ordinary, alternate_votes=[(141, "feeder")]) == 1
    print("Protected alternatives: unique support, exact texts, paid capacity and original deadline passed.")


if __name__ == "__main__":
    main()
