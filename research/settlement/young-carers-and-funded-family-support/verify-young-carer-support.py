def receive(care_budget, education_budget, *, morning_on_time=True,
            morning_accepted=True, evening_on_time=True,
            learning_accepted=True):
    morning = care_budget >= 4 and morning_on_time and morning_accepted
    evening = care_budget >= 7 and evening_on_time
    learning = education_budget >= 2 and learning_accepted
    return morning, evening, learning


def verify():
    assert receive(0, 2) == (False, False, True)
    assert receive(7, 0) == (True, True, False)
    assert receive(7, 2) == (True, True, True)
    assert receive(7, 2, morning_on_time=False) == (False, True, True)
    assert receive(7, 2, morning_accepted=False) == (False, True, True)
    assert receive(7, 2, learning_accepted=False) == (True, True, False)
    assert receive(7 - 4 - 3, 0) == (False, False, False)
    print('Seven funds both care tasks. Two separately funded units restore learning.')
    print('A late or unaccepted visit leaves that duty open, even with cash.')


if __name__ == '__main__':
    verify()
