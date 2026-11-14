"""Check Design295's authored payment and specific public act."""

from dataclasses import dataclass, replace


PAYMENT = 2
PLACEMENT = 3
CONFIRMATION_DUE = 6
RECEIVING_DUE = 8


@dataclass(frozen=True)
class Execution:
    cost: int
    confirmation_hour: int
    receiving_hour: int
    authorized: bool = True
    operative_order: bool = True
    fixed_act: bool = True
    independent_access: bool = True
    access_starts: int = 4
    access_expires: int = 6
    staffed_separately: bool = True
    receiver_accepts: bool = True
    resident_accepts: bool = True
    stayed: bool = False


def delivered(cash, route, payment_ready=True):
    result = set()
    if payment_ready and cash >= PAYMENT:
        result.add('A')
    cash -= PAYMENT
    if all((
        cash >= PLACEMENT + route.cost,
        route.authorized,
        route.operative_order,
        route.fixed_act,
        route.independent_access,
        route.access_starts <= route.confirmation_hour < route.access_expires,
        route.confirmation_hour <= CONFIRMATION_DUE,
        route.confirmation_hour <= route.receiving_hour <= RECEIVING_DUE,
        route.staffed_separately or 'A' not in result,
        route.receiver_accepts,
        route.resident_accepts,
        not route.stayed,
    )):
        result.add('B')
    return result


def main():
    payment_only = Execution(0, 5, 8, authorized=False)
    substitute = Execution(1, 5, 8)
    ordinary_deputy = Execution(2, 5, 8)

    assert delivered(5, payment_only) == {'A'}
    assert delivered(5, substitute) == {'A'}
    assert delivered(6, substitute) == {'A', 'B'}
    assert delivered(7, ordinary_deputy) == {'A', 'B'}
    assert delivered(6, ordinary_deputy) == {'A'}

    failed_routes = (
        replace(substitute, operative_order=False),
        replace(substitute, fixed_act=False),
        replace(substitute, independent_access=False),
        replace(substitute, access_starts=6),
        replace(substitute, access_expires=5),
        replace(substitute, staffed_separately=False),
        replace(substitute, receiver_accepts=False),
        replace(substitute, resident_accepts=False),
        replace(substitute, stayed=True),
        replace(substitute, confirmation_hour=7, access_expires=8),
        replace(substitute, receiving_hour=9),
    )
    assert all(delivered(6, route) == {'A'} for route in failed_routes)
    assert delivered(6, substitute, payment_ready=False) == {'B'}
    assert delivered(5, substitute, payment_ready=False) == set()
    print('Specific orders passed: scoped authority, distinct staffing, timely receipt and expiry.')


if __name__ == '__main__':
    main()
