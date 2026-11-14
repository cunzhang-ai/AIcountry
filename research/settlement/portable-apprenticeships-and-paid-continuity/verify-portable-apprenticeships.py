def unmet_practice(required, compatible_blocks, protected_blocks, standby_blocks):
    assert compatible_blocks >= protected_blocks >= 0
    available = compatible_blocks - protected_blocks + standby_blocks
    return max(0, required - available)


def verify():
    assert unmet_practice(2, 3, 2, 0) == 1
    assert unmet_practice(2, 3, 2, 1) == 0

    first_window_training = 3 + 2 + 2
    first_window_settlement = 7
    wage_claim_owned_by_learner = 1
    assert first_window_training == first_window_settlement
    assert first_window_training + wage_claim_owned_by_learner > first_window_settlement

    second_window_training = 6
    second_window_settlement = 5
    assert second_window_training - second_window_settlement == 1
    assert unmet_practice(2, 3, 2, 0) == 1
    print('Both apprentices can continue in the first window only with independent cover. The next window lacks one lawful unit.')


if __name__ == '__main__':
    verify()
