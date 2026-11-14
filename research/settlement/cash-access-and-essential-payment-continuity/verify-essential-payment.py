def funded_capacity(opening_provision, accepted_commitments):
    assert all(cost >= 0 for cost in accepted_commitments)
    remaining = opening_provision - sum(accepted_commitments)
    assert remaining >= 0
    return remaining


def shortfall(available_provision, due_commitments):
    return max(0, sum(due_commitments) - available_provision)


def timely_delivery(funded, accepting_provider, in_useful_time):
    return funded and accepting_provider and in_useful_time


def verify():
    public_remaining = funded_capacity(9, [5])
    assert public_remaining == 4
    assert shortfall(public_remaining, [3, 5]) == 4
    assert shortfall(public_remaining + 4, [3, 5]) == 0
    assert funded_capacity(public_remaining, [3]) == 1
    assert not timely_delivery(True, False, True)
    assert not timely_delivery(True, True, False)
    assert timely_delivery(True, True, True)
    print('The second day needs four more public units and an accepting provider before the deadline.')


if __name__ == '__main__':
    verify()
