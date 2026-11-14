"""Compare the constructed change-of-government staffing choices."""


def work_gaps(
    casework_days: int,
    rollout_days: int,
    *,
    total_paid_days: int = 12,
    casework_access: bool = True,
    rollout_access: bool = True,
) -> tuple[int, int]:
    assert min(casework_days, rollout_days) >= 0
    assert casework_days + rollout_days <= total_paid_days
    usable_casework = casework_days if casework_access else 0
    usable_rollout = rollout_days if rollout_access else 0
    return max(0, 8 - usable_casework), max(0, 4 - usable_rollout)


if __name__ == "__main__":
    assert work_gaps(8, 4, casework_access=False) == (8, 0)
    assert work_gaps(8, 0) == (0, 4)
    assert work_gaps(8, 4) == (0, 0)
    assert work_gaps(8, 4, rollout_access=False) == (0, 4)
    for rollout_days in range(5):
        gaps = work_gaps(8 - rollout_days, rollout_days, total_paid_days=8)
        assert sum(gaps) == 4
    print("Career casework and elected rollout need distinct paid time and usable access.")
