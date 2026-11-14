"""Check declared permit loss, gross currency and two receipt windows."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Alternate:
    permission: str
    foreign_cost: int
    domestic_cost: int
    receipt_day: int = 23
    authorized: bool = True
    accepted: bool = True


def qualified_delivery(
    route, *, suspended=('common permit',), deposit=6,
    refund_amount=3, refund_day=30, gross_limit=13,
):
    refund_in_time = refund_amount if refund_day <= 8 else 0
    usable_foreign = 12 - deposit + refund_in_time
    first = 4
    if (
        route.permission in suspended
        or route.foreign_cost > usable_foreign
        or deposit + route.foreign_cost > gross_limit
        or 2 + route.domestic_cost > 3
        or route.receipt_day > 25
        or not route.authorized
        or not route.accepted
    ):
        return first, 0
    return first, 4


def main():
    same = Alternate('common permit', 6, 0)
    spot = Alternate('independent permit', 7, 0)
    reserved = Alternate('independent permit', 6, 1)
    domestic = Alternate('independent materials', 2, 3)

    assert qualified_delivery(same) == (4, 0)
    assert qualified_delivery(same, suspended=()) == (4, 4)
    assert qualified_delivery(spot) == (4, 0)
    assert qualified_delivery(reserved) == (4, 4)
    assert qualified_delivery(domestic) == (4, 0)
    assert qualified_delivery(spot, refund_amount=1, refund_day=8) == (4, 4)
    assert qualified_delivery(spot, refund_amount=1, refund_day=9) == (4, 0)
    assert qualified_delivery(spot, refund_day=8, gross_limit=12) == (4, 0)
    assert qualified_delivery(spot, deposit=3) == (4, 4)
    assert qualified_delivery(replace(reserved, permission='common permit')) == (4, 0)
    assert qualified_delivery(replace(reserved, receipt_day=26)) == (4, 0)
    assert qualified_delivery(replace(reserved, accepted=False)) == (4, 0)
    assert qualified_delivery(replace(reserved, authorized=False)) == (4, 0)
    print('Import continuity passed: common permission, usable currency, gross cap and second receipt.')


if __name__ == '__main__':
    main()
