def remaining_interpreting_needs(needed, shared, independent):
    return max(0, needed - shared - independent)


def verified_correction(interpreted, recipient_updated, due_service_received):
    return interpreted and recipient_updated and due_service_received


def verify():
    routine_blocks_released = 6 - 4
    assert routine_blocks_released == 2
    assert remaining_interpreting_needs(2, 1, 0) == 1
    assert remaining_interpreting_needs(2, 1, 1) == 0
    assert not verified_correction(True, False, False)
    assert not verified_correction(True, True, False)
    assert verified_correction(True, True, True)
    print('Two released navigation blocks do not supply the missing interpreter. Correction needs the receiving service as well.')


if __name__ == '__main__':
    verify()
