"""Reproduce the source boundaries and compare two dated budget windows."""

import json
from pathlib import Path
from runpy import run_path

RESEARCH = Path(__file__).resolve().parents[2]
source_tools = run_path(str(RESEARCH / "settlement/matched-national-work/reconcile-2025.py"))
read = source_tools["read"]
source_cell = source_tools["source_cell"]
labour_scope = source_tools["labour_scope"]


def check_sources():
    fiscal = RESEARCH / "2026-11-observed-government-baseline/original-sources"
    work = RESEARCH / "2026-11-matched-national-work-and-first-budget/original-sources"
    expense = read(fiscal / "OFF3-2025.json")["dataset"]
    purposes = read(fiscal / "OFF29-2025.json")["dataset"]
    labour = read(work / "NABB69-2025.json")["dataset"]

    def expenditure(kind, payer="TOTAL"):
        return source_cell(expense, UI=kind, SEKTOR=payer, ContentsCode="OFF3", Tid="2025")

    assert sum(
        source_cell(purposes, FUNKTION=str(purpose), ContentsCode="OFF29", Tid="2025")
        for purpose in range(1, 11)
    ) == expenditure("1.17") == 1472839
    assert sum(expenditure(kind) for kind in (
        "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.13", "1.14"
    )) == expenditure("1.17")
    for category, observed, regional, municipal, residual in (
        ("1.1", 442275, 84739, 230854, 0),
        ("1.2", 263400, 55671, 107354, 0),
        ("1.4", 38589, 28097, 9952, 0),
        ("1.7.2", 445197, 3809, 330364, -1),
    ):
        assert expenditure(category) == observed
        assert (expenditure(category, "R"), expenditure(category, "K")) == (regional, municipal)
        assert sum(expenditure(category, payer) for payer in ("S", "F", "R", "K")) == observed + residual

    assert labour_scope(labour, "SALH_DC", "VMEMO") == 1191239
    assert labour_scope(labour, "SALH_DC", "V86000") == 317975
    assert labour_scope(labour, "SALH_DC", "V87880") == 399986


def compare_motions(second_cash):
    """Each motion specifies gross use and separate independent review slots."""
    ordinary_cash, ordinary_review = 12, 2
    repair = 3
    motions = {
        "retain and repair": ((repair, 1), (repair, 0)),
        "phase": ((repair + 2, 1), (repair + 4, 1)),
        "accelerate": ((repair + 6, 2), (repair + 2, 0)),
        "accelerate with shared setup": ((repair + 6 - 2 + 1, 2), (repair + 2, 0)),
    }
    result = {}
    for motion, windows in motions.items():
        available_review = 4 if motion == "accelerate with shared setup" else 3
        limits = ((20, available_review), (second_cash, 3))
        result[motion] = [
            (
                max(0, ordinary_cash + cash - cash_limit),
                max(0, ordinary_review + review - review_limit),
            )
            for (cash, review), (cash_limit, review_limit) in zip(windows, limits)
        ]
    return result


def check_motions():
    ordinary = compare_motions(second_cash=20)
    stress = compare_motions(second_cash=18)
    assert ordinary == {
        "retain and repair": [(0, 0), (0, 0)],
        "phase": [(0, 0), (0, 0)],
        "accelerate": [(1, 1), (0, 0)],
        "accelerate with shared setup": [(0, 0), (0, 0)],
    }
    assert stress == {**ordinary, "phase": [(0, 0), (1, 0)]}
    assert (20 - (21 - 2), 3 - 4) == (1, -1)
    assert 20 - (21 + 1) == -2
    assert 20 + 17 == 17 + 19 + 1


if __name__ == "__main__":
    check_sources()
    check_motions()
    print(json.dumps({"ordinary": compare_motions(20), "cash delay": compare_motions(18)}, indent=2))
