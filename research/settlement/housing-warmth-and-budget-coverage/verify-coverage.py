"""Reproduce an income-gate diagnostic and conservative overlap bounds."""

from decimal import Decimal as D
from itertools import product
import json
from pathlib import Path

EDITION = (
    Path(__file__).resolve().parents[2] / '2026-11-housing-warmth-and-budget-coverage'
)
PERCENT = D(100)
ROUNDING = D('0.05')


def observation(code, **coordinates):
    data = json.loads((EDITION / f'{code}.json').read_text(), parse_float=D)
    assert data['source'] == 'ESTAT' and data['extension']['id'].lower() == code
    selection = {'freq': 'A', 'unit': 'PC', 'time': '2024', **coordinates}
    assert set(selection) == set(data['id'])
    offset = 0
    for name, size in zip(data['id'], data['size'], strict=True):
        position = data['dimension'][name]['category']['index'][selection[name]]
        offset = offset * size + position
    assert not data.get('status', {}).get(str(offset)), (code, selection)
    return D(data['value'][str(offset)])


def interval(point):
    return max(D(0), point - ROUNDING), min(PERCENT, point + ROUNDING)


def weighted_range(poverty, below, above):
    values = [
        (p * b + (PERCENT - p) * a) / PERCENT
        for p, b, a in product(poverty, below, above)
    ]
    return min(values), max(values)


def intersect(first, second):
    overlap = max(first[0], second[0]), min(first[1], second[1])
    assert overlap[0] <= overlap[1], (first, second)
    return overlap


def percent_outside(poverty, above, total):
    outside = weighted_range(poverty, (D(0), D(0)), above)
    return (
        PERCENT * outside[0] / total[1],
        PERCENT * outside[1] / total[0],
    )


def as_percent_interval(bounds):
    scale = D('0.01')
    return [
        str(bounds[0].quantize(scale, rounding='ROUND_FLOOR')),
        str(bounds[1].quantize(scale, rounding='ROUND_CEILING')),
    ]


def compare(geo):
    poverty_rate = observation(
        'ilc_li02', geo=geo, statinfo='MED_EI', rskpovth='B_60', age='TOTAL', sex='T'
    )
    groups = ('TOTAL', 'B_60', 'A_60')
    housing = [
        observation('ilc_lvho07a', geo=geo, rskpovth=group, age='TOTAL', sex='T')
        for group in groups
    ]
    warmth = [
        observation('sdg_07_60', geo=geo, rskpovth=group, hhcomp='TOTAL')
        for group in groups
    ]

    poverty = interval(poverty_rate)
    housing_total, housing_below, housing_above = map(interval, housing)
    warmth_total, warmth_below, warmth_above = map(interval, warmth)
    housing_total = intersect(
        housing_total, weighted_range(poverty, housing_below, housing_above)
    )
    warmth_total = intersect(
        warmth_total, weighted_range(poverty, warmth_below, warmth_above)
    )

    union_by_group = []
    for housing_group, warmth_group in (
        (housing_below, warmth_below), (housing_above, warmth_above)
    ):
        union_by_group.append((
            max(housing_group[0], warmth_group[0]),
            min(PERCENT, housing_group[1] + warmth_group[1]),
        ))
    union_range = intersect(
        weighted_range(poverty, *union_by_group),
        (max(housing_total[0], warmth_total[0]), min(PERCENT, housing_total[1] + warmth_total[1])),
    )
    return {
        'poverty_percent': str(poverty_rate),
        'housing_percent_total_below_above': list(map(str, housing)),
        'warmth_percent_total_below_above': list(map(str, warmth)),
        'housing_affected_above_threshold_share_percent': as_percent_interval(
            percent_outside(poverty, housing_above, housing_total)
        ),
        'warmth_affected_above_threshold_share_percent': as_percent_interval(
            percent_outside(poverty, warmth_above, warmth_total)
        ),
        'either_indicator_population_share_percent': as_percent_interval(union_range),
    }


result = {geo: compare(geo) for geo in ('DK', 'EU27_2020')}
denmark_range = result['DK']['either_indicator_population_share_percent']
people_per_ten_thousand = [int(D(bound) * 100) for bound in denmark_range]
slots = 1600
result['constructed_denmark_intake'] = {
    'reference_population': 10000,
    'available_slots': slots,
    'possible_people_with_either_indicator': people_per_ten_thousand,
    'possible_unserved_if_all_seek_one_slot': [
        max(0, affected - slots) for affected in people_per_ten_thousand
    ],
}
assert result['constructed_denmark_intake']['possible_unserved_if_all_seek_one_slot'] == [0, 304]
assert result['DK']['housing_percent_total_below_above'] == ['14.6', '65.6', '7.8']
assert result['DK']['warmth_percent_total_below_above'] == ['4.4', '7.8', '4.0']
assert D(result['DK']['housing_affected_above_threshold_share_percent'][0]) > D(46)
assert D(result['DK']['warmth_affected_above_threshold_share_percent'][0]) > D(78)
assert D(result['EU27_2020']['either_indicator_population_share_percent'][0]) > D('10.8')
print(json.dumps(result, indent=2))
