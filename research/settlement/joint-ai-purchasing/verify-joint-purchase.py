"""Check Design291's dated purchases and six concurrent duties."""

from dataclasses import dataclass, replace
from itertools import combinations


REQUIRED = frozenset(('H1', 'H2', 'H3', 'B1', 'B2', 'R1'))


@dataclass(frozen=True)
class Slot:
    worker: str
    qualified_tasks: frozenset
    controller: str
    accepted: bool = True


@dataclass(frozen=True)
class Offer:
    components: tuple[int, ...]
    slots: tuple[Slot, ...]

    @property
    def cost(self):
        return sum(self.components)


def covered(offer, unavailable):
    possible = [
        (slot.worker, task)
        for slot in offer.slots
        if slot.accepted and slot.controller not in unavailable
        for task in sorted(slot.qualified_tasks & REQUIRED)
    ]
    for count in range(len(REQUIRED), 0, -1):
        for assignments in combinations(possible, count):
            workers, tasks = map(set, zip(*assignments))
            if len(workers) == count and len(tasks) == count:
                return tasks
    return set()


def choose(offers, cash, unavailable):
    return [
        name
        for name, offer in offers.items()
        if offer.cost <= cash and covered(offer, unavailable) == REQUIRED
    ]


def main():
    shared = 'common update'

    def slot(task, controller):
        return Slot(task + ' worker', frozenset((task,)), controller)

    first = ('H1', 'H2', 'B1')
    outside = ('H3', 'B2', 'R1')
    primary = tuple(slot(task, shared) for task in first)
    wider = Offer(
        (4, 2),
        tuple(slot(task, shared) for task in sorted(REQUIRED))
        + tuple(slot(task, 'pooled fallback') for task in first + ('R1',)),
    )
    narrow = Offer(
        (3, 2, 3),
        primary
        + tuple(slot(task, 'scoped fallback') for task in first)
        + tuple(slot(task, 'ordinary service ' + task) for task in outside),
    )
    separate = Offer((9,), tuple(slot(task, task + ' root') for task in sorted(REQUIRED)))
    ordinary = Offer((8,), tuple(slot(task, 'ordinary ' + task) for task in sorted(REQUIRED)))
    offers = dict(wider=wider, narrow=narrow, separate=separate, ordinary=ordinary)

    assert [offer.cost for offer in offers.values()] == [6, 8, 9, 8]
    assert covered(wider, set()) == REQUIRED
    assert REQUIRED - covered(wider, {shared}) == {'H3', 'B2'}
    assert choose(offers, 8, {shared}) == ['narrow', 'ordinary']
    assert not choose(offers, 7, {shared})
    assert choose(offers, 9, {shared}) == ['narrow', 'separate', 'ordinary']

    aliased = replace(narrow.slots[3], controller=shared)
    alias_offer = replace(narrow, slots=narrow.slots[:3] + (aliased,) + narrow.slots[4:])
    assert REQUIRED - covered(alias_offer, {shared}) == {'H1'}
    duplicate = replace(narrow.slots[-1], worker=narrow.slots[3].worker)
    double_booked = replace(narrow, slots=narrow.slots[:-1] + (duplicate,))
    assert len(covered(double_booked, {shared})) == 5
    assert REQUIRED - covered(narrow, {shared, 'scoped fallback'}) == set(first)
    print('Joint purchase passed: scope, cash, common controllers and qualified concurrent staffing.')


if __name__ == '__main__':
    main()
