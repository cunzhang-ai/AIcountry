"""Check separately staffed urgent assistance and relief in the constructed case."""

from dataclasses import dataclass, replace

LATEST_START = 3
ALTERNATE_COST = 3


@dataclass(frozen=True)
class Assignment:
    lawyer: str
    qualified: bool = True
    conflicted: bool = False
    accepted: bool = True

    @property
    def usable(self):
        return self.qualified and not self.conflicted and self.accepted


def prepared_count(assignments):
    # One lawyer can take only one of these simultaneous assignments.
    return len({assignment.lawyer for assignment in assignments if assignment.usable})


def funded_alternate(assignment, payments):
    timely_cash = sum(amount for hour, amount in payments if hour <= LATEST_START)
    return assignment if timely_cash >= ALTERNATE_COST else replace(assignment, accepted=False)


def preserved_before(deadline, *, ordered, executed_at):
    return ordered and executed_at is not None and executed_at <= deadline


def main():
    shared = Assignment("shared")
    alternate = Assignment("alternate")
    conflicted = Assignment("ordinary", conflicted=True)
    assert prepared_count([conflicted, shared, shared]) == 1
    assert prepared_count([shared, funded_alternate(alternate, [(3, 3)])]) == 2
    assert prepared_count([shared, funded_alternate(alternate, [(3, 2), (4, 1)])]) == 1
    unavailable = replace(alternate, accepted=False)
    assert prepared_count([shared, funded_alternate(unavailable, [(3, 3)])]) == 1

    assert preserved_before(7, ordered=True, executed_at=7)
    assert not preserved_before(7, ordered=True, executed_at=8)
    assert not preserved_before(8, ordered=True, executed_at=None)
    assert not preserved_before(8, ordered=False, executed_at=None)
    print("Urgent civil assistance: conflicts, paid alternate and actual relief passed.")


if __name__ == "__main__":
    main()
