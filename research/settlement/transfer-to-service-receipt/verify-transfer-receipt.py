"""Check the published-row arithmetic and constructed deadline."""

from decimal import Decimal as D


def main():
    components = map(D, ("218.6", "-75.3", "102.2", "111.5", "-443.5", "-11.2"))
    net = sum(components)
    assert net == D("-97.7")
    assert (net / 3).quantize(D("0.01")) == D("-32.57")
    assert (D("111.5") / 3).quantize(D("0.01")) == D("37.17")
    draw = -((net - D("-63.7")) - D("355.8") - D("110.4"))
    assert draw == D("500.2")
    additions = D("66.1") + D("8.4") + D("2.0")
    assert D("1134.5") - draw + additions == D("710.8")
    assert D("1135.5") - draw + additions == D("711.8")

    remittance = 15 + 4 - 6
    due = 14
    assert remittance == 13
    assert due - remittance == 1
    for advance_day, expected_timely in ((2, True), (3, False)):
        received_by_due = remittance + int(advance_day <= 2)
        assert (received_by_due >= due) == expected_timely
    print("Transfer: gross-to-net settlement, published opening difference and due date passed.")


if __name__ == "__main__":
    main()
