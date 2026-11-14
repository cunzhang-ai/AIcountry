"""Reproduce the authored two-period gross budget and firm service checks."""

PERIOD_ONE_CAP = 100
PERIOD_TWO_CAP = 80
CUMULATIVE_CAP = 180
PROTECTED_PEAK = 12
# Incremental cost, remaining gross emissions, firm delivered MW.
PACKAGES = {
    "retire": (0, 4, 9),
    "keep": (4, 12, 12),
    "repair and reserve": (8, 6, 12),
    "independent substitutes": (9, 5, 12),
}


def feasible(cash, observed_gross, lost_repair_mw=0):
    return [
        name for name, (cost, extra_gross, firm_mw) in PACKAGES.items()
        if cost <= cash and observed_gross + extra_gross <= PERIOD_ONE_CAP
        and firm_mw - (lost_repair_mw if name == "repair and reserve" else 0)
        >= PROTECTED_PEAK
    ]


def second_period_headroom(first_actual, second_used=0):
    return min(PERIOD_TWO_CAP - second_used,
               CUMULATIVE_CAP - first_actual - second_used)


if __name__ == "__main__":
    assert feasible(8, 94) == ["repair and reserve"]
    assert feasible(9, 94) == ["repair and reserve", "independent substitutes"]
    assert feasible(7, 94) == []
    assert feasible(8, 94, lost_repair_mw=1) == []
    assert feasible(9, 96) == []

    assert second_period_headroom(98) == 80
    assert second_period_headroom(106) == 74
    assert second_period_headroom(106, 75) == -1
    assert second_period_headroom(106, 74) == 0
    assert 106 > PERIOD_ONE_CAP
    print("At 8 units only repair and reserve passes. At 7 no package passes both tests.")
    print("After 106 gross, next usable headroom is 74; using 75 leaves a 1-unit excess.")
    print("Correcting observed emissions to 96 reopens all listed firm options.")
