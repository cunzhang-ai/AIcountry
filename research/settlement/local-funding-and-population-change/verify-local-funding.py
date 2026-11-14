"""Reconcile the two-locality funding and cash exercise."""

from fractions import Fraction


def national_residual(fixed, variable, own, other):
    return max(0, fixed + variable - own - other)


def service_shortfall(due, received_local, received_national):
    return max(0, due - received_local - received_national)


def bridge(uncovered, usable_authorized_cash, receipt_day, due_day):
    if receipt_day > due_day:
        return 0
    return min(uncovered, usable_authorized_cash)


def main():
    earlier = (
        national_residual(40, 40, 30, 10),
        national_residual(30, 50, 35, 5),
    )
    qualified = (
        national_residual(40, 30, 28, 10),
        national_residual(30, 70, 39, 5),
    )
    headcount = (earlier[0] * Fraction(75, 100), earlier[1] * Fraction(140, 100))
    assert earlier == (40, 40)
    assert qualified == (32, 56)
    assert headcount == (30, 56)
    assert sum(qualified) == 88
    assert sum(qualified) - 87 == 1

    def due_shortfalls(ridge, port):
        return service_shortfall(20, 12, ridge), service_shortfall(26, 11, port)

    assert due_shortfalls(10, 10) == (0, 5)
    assert due_shortfalls(headcount[0] / 4, headcount[1] / 4) == (Fraction(1, 2), 1)
    assert due_shortfalls(8, 14) == (0, 1)
    assert due_shortfalls(8, 15) == (0, 0)
    retimed_port = (15, 13, 14, 14)
    assert sum(retimed_port) == qualified[1]
    assert service_shortfall(24, 11, retimed_port[1]) == 0
    assert service_shortfall(25, 11, retimed_port[1]) == 1
    for capacity, arrival, expected in ((5, 30, 0), (3, 30, 2), (5, 31, 5)):
        port_bridge = bridge(5, capacity, arrival, 30)
        assert due_shortfalls(10, 10 + port_bridge) == (0, expected)

    assert bridge(5, 10, 30, 30) == 5
    assert 10 + bridge(5, 5, 30, 30) - Fraction(qualified[1], 4) == 1
    assert national_residual(35, 30, 28, 10) == qualified[0] - 5
    print('Local funding passed: fixed costs, annual shares, dated cash and capped advances.')


if __name__ == '__main__':
    main()
