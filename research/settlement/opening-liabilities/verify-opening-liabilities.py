"""Reproduce Design292's constructed opening-cash paths."""

from dataclasses import dataclass


DECISION_DAY = 5
EXISTING_DUES = 3 + 2
CHOICES = {'ordinary duties': 0, 'preparation': 1, 'retrofit': 3}


@dataclass(frozen=True)
class Exposure:
    claim: str
    call_day: int
    amount: int | None


@dataclass(frozen=True)
class Funding:
    receipt_day: int
    amount: int
    actually_received: bool = True
    usable_for_choice: bool = True


def exposure_by_day(reports):
    distinct = {}
    for report in reports:
        prior = distinct.setdefault(report.claim, report)
        if prior != report:
            raise ValueError(f'Conflicting reports for {report.claim}')
    relevant = [report.amount for report in distinct.values() if report.call_day <= DECISION_DAY]
    if None in relevant:
        return None
    return sum(relevant)


def usable_balance(sources):
    return sum(
        source.amount
        for source in sources
        if source.receipt_day <= DECISION_DAY
        and source.actually_received
        and source.usable_for_choice
    )


def priced_choices(sources, reports):
    exposure = exposure_by_day(reports)
    if exposure is None:
        return None
    cash = usable_balance(sources)
    return [
        choice for choice, cost in CHOICES.items()
        if EXISTING_DUES + exposure + cost <= cash
    ]


def main():
    reported = Exposure('underlying guarantee', 5, 4)
    same_claim = Exposure('underlying guarantee', 5, 4)
    assert exposure_by_day((reported, same_claim)) == 4
    assert exposure_by_day((reported, Exposure('independent guarantee', 5, 2))) == 6
    try:
        exposure_by_day((reported, Exposure('underlying guarantee', 5, 5)))
    except ValueError:
        pass
    else:
        raise AssertionError('Inconsistent reports must remain unresolved')

    reference = (Funding(0, 11),)
    assert priced_choices(reference, ()) == list(CHOICES)
    assert priced_choices(reference, (reported, same_claim)) == ['ordinary duties', 'preparation']
    assert priced_choices(reference, (reported, Exposure('additional claim', 5, None))) is None
    assert priced_choices(reference, (reported, Exposure('independent guarantee', 5, 2))) == [
        'ordinary duties',
    ]
    weak = (Funding(0, 9),)
    assert priced_choices(weak, (reported,)) == ['ordinary duties']
    assert priced_choices(weak + (Funding(20, 3, actually_received=False),), (reported,)) == [
        'ordinary duties',
    ]
    assert priced_choices(weak + (Funding(20, 3),), (reported,)) == ['ordinary duties']
    restricted = Funding(4, 3, usable_for_choice=False)
    assert priced_choices(weak + (restricted,), (reported,)) == ['ordinary duties']
    assert priced_choices(weak + (Funding(4, 1),), (reported,)) == [
        'ordinary duties', 'preparation',
    ]
    print('Opening liabilities passed: distinct claims, cash dates, unknown exposure and exact choices.')


if __name__ == '__main__':
    main()
