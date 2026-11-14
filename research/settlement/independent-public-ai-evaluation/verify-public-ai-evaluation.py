"""Check the constructed service qualification comparison."""


def meets_case_criteria(standard_correct: int, protected_correct: int) -> bool:
    overall_floor = 90
    protected_count = 20
    protected_error_limit = 2
    return (
        standard_correct + protected_correct >= overall_floor
        and protected_count - protected_correct <= protected_error_limit
    )


def trial_is_staffed(verification_hours: int, protected_hours: int) -> bool:
    return verification_hours >= 3 and protected_hours >= 5


if __name__ == "__main__":
    assert not meets_case_criteria(80, 16)
    assert not meets_case_criteria(80, 14)
    assert meets_case_criteria(72, 18)
    assert meets_case_criteria(80, 18)
    assert trial_is_staffed(3, 5)
    assert not trial_is_staffed(3, 4)
    assert not trial_is_staffed(4, 4)
    print("Higher aggregate scores cannot override protected-scope and paid-capacity gates.")
