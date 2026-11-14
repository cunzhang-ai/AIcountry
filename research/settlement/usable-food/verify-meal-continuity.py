"""Check the authored two-window meals and cash schedule."""

from dataclasses import dataclass, replace


NEED = (5, 3)


@dataclass(frozen=True)
class Route:
    ordinary_places: int
    specific_places: int
    dependencies: frozenset[str]


@dataclass(frozen=True)
class Plan:
    early_cost: int
    total_cost: int
    first: tuple[Route, ...]
    second: tuple[Route, ...]
    continuing_if_unfunded: tuple[Route, ...] = ()


def received(routes, unavailable):
    ordinary = specific = 0
    for route in routes:
        if route.dependencies.isdisjoint(unavailable):
            ordinary += route.ordinary_places
            specific += route.specific_places
    return min(ordinary, NEED[0]), min(specific, NEED[1])


def compare(plan, cash, unavailable):
    if cash[0] < plan.early_cost or cash[1] < plan.early_cost:
        return (0, 0), (0, 0)
    first = received(plan.first, unavailable)
    if cash[1] < plan.total_cost:
        return first, received(plan.continuing_if_unfunded, unavailable)
    return first, received(plan.second, unavailable)


def main():
    market = Route(5, 3, frozenset({'shops'}))
    dry_goods = Route(5, 3, frozenset({'home water and cooking'}))
    kitchen = Route(5, 0, frozenset({'kitchen', 'independent water and power', 'kitchen transport'}))
    ready = Route(0, 3, frozenset({'accepted suitable meals', 'ready meal transport'}))
    distributed = replace(ready, ordinary_places=5)

    cash_plan = Plan(4, 4, (market,), (market,))
    ingredients = Plan(5, 5, (dry_goods,), (dry_goods,))
    partial = Plan(7, 7, (kitchen, ready), (kitchen,))
    mixed = Plan(7, 10, (kitchen, ready), (kitchen, ready), (kitchen,))
    separate = Plan(7, 12, (distributed,), (distributed,))

    unavailable = {'shops', 'home water and cooking'}
    assert compare(cash_plan, (7, 10), unavailable) == ((0, 0), (0, 0))
    assert compare(cash_plan, (7, 10), set()) == (NEED, NEED)
    assert compare(ingredients, (7, 10), unavailable) == ((0, 0), (0, 0))
    assert compare(partial, (7, 7), unavailable) == (NEED, (5, 0))
    assert compare(mixed, (7, 10), unavailable) == (NEED, NEED)
    assert compare(mixed, (7, 7), unavailable) == (NEED, (5, 0))
    assert compare(mixed, (6, 12), unavailable) == ((0, 0), (0, 0))
    shared_transport_loss = unavailable | {'ready meal transport'}
    assert compare(mixed, (7, 10), shared_transport_loss) == ((5, 0), (5, 0))
    unsuitable_lot = unavailable | {'accepted suitable meals'}
    assert compare(mixed, (7, 10), unsuitable_lot) == ((5, 0), (5, 0))
    kitchen_loss = unavailable | {'independent water and power'}
    assert compare(mixed, (7, 10), kitchen_loss) == ((0, 3), (0, 3))
    assert compare(separate, (7, 12), kitchen_loss) == (NEED, NEED)
    assert compare(separate, (7, 10), kitchen_loss) == (NEED, (0, 0))
    print('Food continuity passed: timely cash, meal suitability, independent inputs and repeat delivery.')


if __name__ == '__main__':
    main()
