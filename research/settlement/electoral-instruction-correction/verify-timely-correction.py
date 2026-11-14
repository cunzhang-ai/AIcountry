"""Check the authored election correction and its original windows."""

from dataclasses import dataclass, replace


DEADLINES = {**{voter: 60 for voter in range(4)}, **{voter: 120 for voter in range(4, 7)}}
ALREADY_LOST = frozenset((7, 8))


@dataclass(frozen=True)
class Route:
    recipients: frozenset
    arrival: int
    cost: int
    controller: str
    authorized: bool = True
    accepted: bool = True


def timely(routes, available_cash, failed, *, verified):
    if not verified or sum(route.cost for route in routes) > available_cash:
        return set()
    return {
        voter
        for route in routes
        if route.authorized and route.accepted and route.controller not in failed
        for voter in route.recipients & DEADLINES.keys()
        if route.arrival <= DEADLINES[voter]
    }


def main():
    digital = Route(frozenset(range(4, 7)), 20, 1, 'compromised')
    local = Route(frozenset(range(4, 9)), 90, 2, 'local')
    phone = Route(frozenset(range(4)), 45, 3, 'independent phone')
    failed = {'compromised'}

    def reached(routes, cash=5, verified=True):
        return timely(routes, cash, failed, verified=verified)

    assert reached((digital,), 1) == set()
    assert timely((digital,), 1, set(), verified=True) == {4, 5, 6}
    assert reached((local,), 3) == {4, 5, 6}
    assert reached((local, phone)) == set(range(7))
    assert reached((local, phone), 3) == set()
    assert reached((local, phone), verified=False) == set()
    assert reached((local, replace(phone, authorized=False))) == {4, 5, 6}
    assert reached((local, replace(phone, accepted=False))) == {4, 5, 6}
    assert reached((local, replace(phone, controller='compromised'))) == {4, 5, 6}
    assert reached((local, replace(phone, arrival=60))) == set(range(7))
    assert reached((local, replace(phone, arrival=75))) == {4, 5, 6}
    assert reached((local, replace(phone, recipients=phone.recipients | {4}))) == set(range(7))
    assert ALREADY_LOST.isdisjoint(reached((local, phone)))
    print('Electoral correction passed: qualified facts, independent delivery and original deadlines.')


if __name__ == '__main__':
    main()
