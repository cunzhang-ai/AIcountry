def qualifies(east_closed, west_closed, work_cost, budget, *,
              accepted_trip, inspection_slots, independent_networks=True):
    access_cost = 2
    return (
        not (east_closed & west_closed)
        and max(west_closed) <= 4
        and work_cost + access_cost <= budget
        and accepted_trip
        and inspection_slots >= 2
        and independent_networks
    )


def verify():
    separate_east = {1, 2, 3, 4}
    shared_east = {1, 2}
    original_west = {2, 3}
    phased_west = {3, 4}
    shared_cost = 9 + 3
    budget = 14
    assert separate_east & original_west == {2, 3}
    assert shared_east & original_west == {2}
    assert 7 + 6 + 3 > budget
    assert not qualifies(shared_east, original_west, shared_cost, budget,
                         accepted_trip=True, inspection_slots=2)
    assert not qualifies(shared_east, {4, 5}, shared_cost, budget,
                         accepted_trip=True, inspection_slots=2)
    assert qualifies(shared_east, phased_west, shared_cost, budget,
                     accepted_trip=True, inspection_slots=2)
    assert not qualifies(shared_east, phased_west, shared_cost, budget - 1,
                         accepted_trip=True, inspection_slots=2)
    assert not qualifies(shared_east, phased_west, shared_cost, budget,
                         accepted_trip=False, inspection_slots=2)
    assert not qualifies(shared_east, phased_west, shared_cost, budget,
                         accepted_trip=True, inspection_slots=1)
    assert not qualifies(shared_east, phased_west, shared_cost, budget,
                         accepted_trip=True, inspection_slots=2,
                         independent_networks=False)
    print('Phasing preserves access only with the paid trip and both independent checks.')
    print('Shared excavation does not qualify a jointly vulnerable operating network.')


if __name__ == '__main__':
    verify()
