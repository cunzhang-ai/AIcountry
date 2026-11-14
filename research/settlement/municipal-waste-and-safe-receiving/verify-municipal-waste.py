def unaccounted_mass(incoming, recovered, disposed, stored):
    return incoming - recovered - disposed - stored


def missed_treatment(new_units, carry, permitted_slots, funded_slots):
    return max(0, new_units + carry - min(permitted_slots, funded_slots))


def verify():
    assert unaccounted_mass(6, recovered=3, disposed=1, stored=2) == 0
    assert unaccounted_mass(6, recovered=3, disposed=1, stored=0) == 2

    assert missed_treatment(4, 0, 3, 3) == 1
    assert missed_treatment(4, 1, 4, 4) == 1
    assert missed_treatment(4, 1, 4, 5) == 1
    assert missed_treatment(4, 1, 5, 4) == 1
    assert missed_treatment(4, 1, 5, 5) == 0

    window_one = {"alternate_receiving": 6, "closure_only": 4}
    window_two = {"alternate_receiving": 4, "closure_only": 4}
    assert window_one["alternate_receiving"] >= 6
    assert window_two["alternate_receiving"] < 5 <= sum(window_two.values())
    print('Three of six dry units are verified recovered, and the second food round needs one more funded and permitted place.')


if __name__ == '__main__':
    verify()
