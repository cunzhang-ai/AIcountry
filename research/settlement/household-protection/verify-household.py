"""Check the declared household comparison, using constructed inputs."""

from dataclasses import dataclass, replace


HEAT_DUE = 8
CARE_DUE = 10
DISPATCH_FUNDS_DUE = 6
RENEW_BY = 20
BOOKING_END = 24


@dataclass(frozen=True)
class Route:
    place: str
    warmth_at: int
    care_place: str
    care_at: int
    early_cost: int
    total_cost: int
    through: int
    works: bool = True
    consent: bool = True
    arrival: int = 0


def check_start(route, early_cash, total_cash):
    gaps = []
    if not route.works or max(route.warmth_at, route.arrival) > HEAT_DUE:
        gaps.append('warmth unavailable by deadline')
    if route.care_place != route.place or not route.arrival <= route.care_at <= CARE_DUE:
        gaps.append('care unavailable at receiving place by deadline')
    if route.through < CARE_DUE:
        gaps.append('receiving ends before both needs can be covered')
    if route.early_cost > early_cash or route.total_cost > total_cash:
        gaps.append('insufficient usable cash')
    if not route.consent:
        gaps.append('resident did not agree')
    return gaps


def cash_at_dispatch(ordinary_cash, advance, received_at, authorized):
    if authorized and received_at is not None and received_at <= DISPATCH_FUNDS_DUE:
        return ordinary_cash + advance
    return ordinary_cash


def check_handoff(
    ready_at, resumed_care, *,
    renewed_at=None, renewal_through=None, renewal_accepted=False,
):
    if resumed_care and ready_at <= BOOKING_END:
        return 'verified return on original stay'
    if (
        renewal_accepted and renewed_at is not None and renewed_at <= RENEW_BY
        and renewal_through is not None and renewal_through > BOOKING_END
    ):
        if resumed_care and ready_at <= renewal_through:
            return 'verified return through extension'
        return 'continue protection and recheck before extension ends'
    return 'uncovered from hour 24'


def main():
    home = Route('home', 7, 'home', 9, 3, 3, 36, works=False)
    room = Route('room', 7, 'home', 9, 2, 4, 24, arrival=7)
    joined = replace(room, care_place='room', early_cost=5, total_cost=8)
    later_move = Route('new home', 34, 'new home', 35, 5, 8, 36, arrival=34)

    assert not check_start(replace(home, works=True), 4, 8)
    assert check_start(home, 5, 8) == ['warmth unavailable by deadline']
    assert check_start(room, 5, 8) == ['care unavailable at receiving place by deadline']
    assert check_start(replace(joined, arrival=9), 5, 8) == [
        'warmth unavailable by deadline',
    ]
    assert not check_start(joined, 5, 8)
    assert check_start(joined, 4, 8) == ['insufficient usable cash']
    assert check_start(joined, 5, 7) == ['insufficient usable cash']
    assert not check_start(joined, cash_at_dispatch(4, 1, 6, True), 8)
    assert check_start(joined, cash_at_dispatch(4, 1, 7, True), 8) == [
        'insufficient usable cash',
    ]
    assert check_start(joined, cash_at_dispatch(4, 1, 6, False), 8) == [
        'insufficient usable cash',
    ]
    assert check_start(replace(joined, consent=False), 5, 8) == [
        'resident did not agree',
    ]
    assert check_start(later_move, 5, 8) == [
        'warmth unavailable by deadline',
        'care unavailable at receiving place by deadline',
    ]

    assert check_handoff(23, True) == 'verified return on original stay'
    assert check_handoff(28, True) == 'uncovered from hour 24'
    extension = dict(renewed_at=20, renewal_through=36, renewal_accepted=True)
    assert check_handoff(28, True, **extension) == 'verified return through extension'
    assert check_handoff(28, False, **extension) == (
        'continue protection and recheck before extension ends'
    )
    assert check_handoff(28, True, **(extension | {'renewed_at': 25})) == (
        'uncovered from hour 24'
    )
    assert check_handoff(28, True, **(extension | {'renewal_accepted': False})) == (
        'uncovered from hour 24'
    )
    print('Household comparison passed: same-site care, dated cash, consent, renewal and return.')


if __name__ == '__main__':
    main()
