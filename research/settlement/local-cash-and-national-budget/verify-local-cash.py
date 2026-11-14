"""Check transcribed budget arithmetic and the separate payment example."""

from decimal import Decimal


def main():
    assert 20_949 - 20_700 == 249
    assert Decimal("467.3") - Decimal("111.5") == Decimal("355.8")
    movements = map(Decimal, ("-355.8", "-110.4", "-34.0", "66.1", "8.4", "2.0"))
    displayed_bridge = sum(movements, Decimal("1135.5"))
    assert displayed_bridge == Decimal("711.8")
    assert Decimal("710.8") - displayed_bridge == Decimal("-1.0")
    assert Decimal("710.8") - 700 == Decimal("10.8")

    local_available, due, final_allowed = 4, 9, 6
    authorized_advance = 5
    assert due - local_available == 5
    assert local_available + authorized_advance == due
    assert final_allowed - authorized_advance == 1
    local_own_cost = due - final_allowed
    assert local_own_cost + final_allowed == due
    print("Local cash: displayed residual, timely advance and net settlement passed.")


if __name__ == "__main__":
    main()
