"""Reconcile the selected NHS extracts and the separate authored comparison."""

import json
from pathlib import Path


def read_extract():
    path = (
        Path(__file__).resolve().parents[2]
        / "2026-11-maintenance-and-service-continuity"
        / "observed-site-returns.json"
    )
    return json.loads(path.read_text())["periods"]


def compare_observations():
    periods = read_extract()
    sites = {
        period: {row["site_code"]: row for row in value["sites"]}
        for period, value in periods.items()
    }
    earlier, later = sites["2023/24"], sites["2024/25"]
    assert earlier.keys() == later.keys() == {"RGT01", "REF12"}
    expected = {
        "RGT01": (208_559_408, 234_751_502, 26_192_094, 18_000_000),
        "REF12": (51_612_567, 45_424_756, -6_187_811, 6_187_511),
    }
    for code in sorted(earlier):
        before, after = earlier[code], later[code]
        for field in ("trust_code", "site_name", "method", "surveyed_gia_band"):
            assert before[field] == after[field]
        levels = ("high", "significant", "moderate", "low")
        opening = sum(before[level] for level in levels)
        closing = sum(after[level] for level in levels)
        investment = after["investment_critical"] + after["investment_noncritical"]
        assert (opening, closing, closing - opening, investment) == expected[code]
        print(f"{code}: reported backlog {opening:,} to {closing:,}; investment {investment:,}.")


def compare_authored_options():
    early_cash, later_cash = 8, 10
    required_visits, required_hearings = 12, 8
    portfolios = {
        "defer and expand": (4, 9 + 3, 9, 6),
        "repair with continuity": (5 + 1, 2, 12, 8),
        "early replacement": (9, 2, 12, 8),
        "phased funded exit": (7, 4, 12, 8),
    }
    feasible = [
        name
        for name, (early, late, visits, hearings) in portfolios.items()
        if early <= early_cash and late <= later_cash
        and visits >= required_visits and hearings >= required_hearings
    ]
    assert feasible == ["repair with continuity", "phased funded exit"]
    _, _, visits, hearings = portfolios["defer and expand"]
    assert (required_visits - visits, required_hearings - hearings) == (3, 2)
    assert portfolios["repair with continuity"][0] + portfolios["defer and expand"][0] == 10 > early_cash
    early_crews = 1
    crews_needed = {"repair with continuity": 1, "discretionary expansion": 1}
    assert all(crews <= early_crews for crews in crews_needed.values())
    assert sum(crews_needed.values()) > early_crews

    opening, newly_due, newly_found, repriced, completed, closed = (10, 3, 2, 1, 4, 1)
    assert opening + newly_due + newly_found + repriced - completed - closed == 11
    print("Repair and funded exit fit. Deferral misses three visits and two hearings in the declared loss.")
    print("Matched backlog rises from ten to eleven after work, discovery, repricing and lawful closure.")


if __name__ == "__main__":
    compare_observations()
    compare_authored_options()
