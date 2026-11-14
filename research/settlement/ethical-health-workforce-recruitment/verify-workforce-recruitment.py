"""Check staffing and costs in the constructed two-system comparison."""


def service_shifts(
    moves: int,
    *,
    domestic_return: int = 0,
    added_origin_shifts: int = 0,
) -> tuple[int, int]:
    return 8 + domestic_return + moves, 9 + added_origin_shifts - moves


def can_release_stage(planned_moves: int, verified_origin_shifts: int) -> bool:
    return service_shifts(planned_moves, added_origin_shifts=verified_origin_shifts)[1] >= 9


if __name__ == "__main__":
    assert service_shifts(2) == (10, 7)
    assert service_shifts(0, domestic_return=2) == (10, 9)
    assert service_shifts(0) == (8, 9)
    assert 6 + 4 == 10
    assert not can_release_stage(2, 1)
    assert can_release_stage(2, 2)
    assert service_shifts(2, added_origin_shifts=2) == (10, 9)
    assert service_shifts(1, added_origin_shifts=2) == (9, 10)
    print("Paired staffing depends on verified origin protection and actual voluntary receiving.")
