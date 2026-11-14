"""Reproduce Design290's authored transport and useful-time comparison."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Trip:
    deadline: int
    duration: int
    arrival_supported: bool = True
    passenger_accepted: bool = True
    wheelchair_positions: int = 1


@dataclass(frozen=True)
class Vehicle:
    ready: int
    cost: int
    controllers: frozenset
    wheelchair_positions: int = 1
    operational: bool = True


def can_receive(trip, vehicle, available_cash):
    return all((
        vehicle.operational,
        trip.arrival_supported,
        trip.passenger_accepted,
        trip.wheelchair_positions <= vehicle.wheelchair_positions,
        vehicle.ready + trip.duration <= trip.deadline,
        vehicle.cost <= available_cash,
    ))


def independent(first, second):
    return first.controllers.isdisjoint(second.controllers)


def compare(evacuation, voting, standby, backup, cash, reset_delay):
    assert cash >= standby.cost
    received = set()
    remaining_cash = cash - standby.cost
    if can_receive(evacuation, standby, cash):
        received.add('E')
        next_ready = standby.ready + evacuation.duration + reset_delay
        subsequent = replace(standby, ready=next_ready, cost=0)
        if can_receive(voting, subsequent, remaining_cash):
            received.add('V')
        elif backup and independent(standby, backup) and can_receive(voting, backup, remaining_cash):
            received.add('V')
    elif can_receive(voting, standby, cash):
        received.add('V')
    elif backup and independent(standby, backup) and can_receive(voting, backup, remaining_cash):
        received.add('V')
    return received


def main():
    evacuation = Trip(deadline=20, duration=16)
    voting = Trip(deadline=28, duration=7)
    standby = Vehicle(0, 4, frozenset({'north road', 'crew 1', 'dispatch 1'}))
    backup = Vehicle(17, 3, frozenset({'south road', 'crew 2', 'dispatch 2'}))
    assert compare(evacuation, voting, standby, None, 4, reset_delay=14) == {'E'}
    assert compare(evacuation, voting, standby, backup, 7, reset_delay=14) == {'E', 'V'}
    assert compare(evacuation, voting, standby, backup, 4, reset_delay=14) == {'E'}
    assert compare(evacuation, voting, standby, None, 4, reset_delay=4) == {'E', 'V'}
    dedicated = replace(backup, cost=4)
    assert compare(evacuation, voting, standby, dedicated, 8, reset_delay=14) == {'E', 'V'}
    failed_standby = replace(standby, operational=False)
    assert compare(evacuation, voting, failed_standby, dedicated, 8, reset_delay=14) == {'V'}

    common = replace(backup, controllers=backup.controllers | {'dispatch 1'})
    assert compare(evacuation, voting, standby, common, 7, reset_delay=14) == {'E'}
    no_receiver = replace(evacuation, arrival_supported=False)
    assert compare(no_receiver, voting, standby, backup, 7, reset_delay=14) == {'V'}
    assert not can_receive(replace(evacuation, wheelchair_positions=2), standby, 4)
    assert not can_receive(replace(evacuation, passenger_accepted=False), standby, 4)

    later = Trip(deadline=34, duration=9)
    assert not can_receive(later, replace(standby, ready=30, cost=0), 0)
    assert can_receive(later, replace(standby, ready=25, cost=0), 0)
    print('Accessible dispatch passed: useful arrival, separate routes, cash and next call.')


if __name__ == '__main__':
    main()
