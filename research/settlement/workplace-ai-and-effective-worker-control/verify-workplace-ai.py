def reliance_qualifies(authorization, paid_review, care_received, fallback_hours):
    return authorization and paid_review and care_received and fallback_hours >= 4


def correction(verified_original, roster_day, payment_day):
    return (
        verified_original and roster_day < 4,
        verified_original and payment_day < 5,
    )


def verify():
    ordinary = 84 + 16
    claimed = 84 + 6
    shifted = 6 + 4
    worker_proposal = 84 + 8 + 4
    assert ordinary - claimed == 10
    assert claimed + shifted == ordinary
    assert ordinary - worker_proposal == 4
    assert reliance_qualifies(True, True, True, 4)
    assert not reliance_qualifies(False, True, True, 4)
    assert not reliance_qualifies(True, True, False, 4)
    assert not reliance_qualifies(True, True, True, 3)
    assert correction(True, 3, 4) == (True, True)
    assert correction(True, 3, 6) == (True, False)
    assert correction(False, 3, 4) == (False, False)
    print('The claimed ten hours are transferred work. The qualified proposal releases four.')
    print('Independent evidence, roster access and on-time payroll each matter.')


if __name__ == '__main__':
    verify()
