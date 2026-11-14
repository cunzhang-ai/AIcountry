"""Check resident-level access and public funding in the constructed case."""

PEOPLE = frozenset(range(6))
ORDINARY_SHOPPERS = frozenset(range(4))
DELIVERY_RECIPIENTS = PEOPLE - ORDINARY_SHOPPERS


def outcome(cash_recipients, delivery_offers, *, budget, delivery_cost,
            shoppers=ORDINARY_SHOPPERS, prioritized_delivery=None):
    # The lists represent identified people, not interchangeable cash or slots.
    assert cash_recipients <= PEOPLE and delivery_offers <= PEOPLE - shoppers
    committed_cash = len(cash_recipients)
    assert committed_cash <= budget
    # A shortage comparison assumes a lawful order, not an executable priority rule.
    qualified_slots = (budget - committed_cash) // delivery_cost
    delivered = delivery_offers if prioritized_delivery is None else prioritized_delivery
    assert delivered <= delivery_offers and len(delivered) <= qualified_slots
    received = (shoppers & cash_recipients) | delivered
    return committed_cash + delivery_cost * len(delivered), PEOPLE - received


assert outcome(frozenset(), frozenset(), budget=8, delivery_cost=2) == (0, PEOPLE)
assert outcome(PEOPLE, frozenset(), budget=8, delivery_cost=2) == (6, DELIVERY_RECIPIENTS)
assert outcome(ORDINARY_SHOPPERS, DELIVERY_RECIPIENTS, budget=8, delivery_cost=2) == (8, set())
assert outcome(PEOPLE, DELIVERY_RECIPIENTS, budget=8, delivery_cost=1) == (8, set())
assert outcome(PEOPLE, DELIVERY_RECIPIENTS, budget=7, delivery_cost=1,
               prioritized_delivery={4}) == (7, {5})
assert outcome(PEOPLE, frozenset(), budget=8, delivery_cost=1) == (6, DELIVERY_RECIPIENTS)
assert outcome(PEOPLE, frozenset(), budget=6, delivery_cost=1, shoppers=PEOPLE) == (6, set())
assert len(ORDINARY_SHOPPERS & {0, 1, 4, 5}) == 2  # Payment counts alone conceal who can shop.
assert 4 + 2 == 5 + 1 == 6  # Separate household and public cost shares.
assert (4 + 2 * 6, 6 + 2 * 6) == (16, 18)  # Gross invoices before copays.


def qualifies_ordinary_joint_route(*, start_cash, recurring_cash, timely_acceptance):
    return start_cash >= 3 and recurring_cash >= 6 + 1 and timely_acceptance


assert qualifies_ordinary_joint_route(start_cash=3, recurring_cash=7, timely_acceptance=True)
assert not qualifies_ordinary_joint_route(start_cash=2, recurring_cash=8, timely_acceptance=True)
assert not qualifies_ordinary_joint_route(start_cash=3, recurring_cash=7, timely_acceptance=False)
assert 6 + 2 > 7

original_b, updated_b = 100, 120
deposit = 1500
original_coverage = min(deposit, 12 * original_b)
crystallized_coverage = original_coverage
live_coverage = min(deposit, 12 * updated_b)
assert crystallized_coverage == 1200 and live_coverage == 1440
previously_unused_headroom = 200
assert live_coverage - original_coverage - previously_unused_headroom == 40
assert tuple(b - (80 - b // 5) // 2 for b in (original_b, updated_b)) == (70, 92)

print("Four people obtain food with cash alone. Six receive it when additional slots qualify.")
print("At seven units one temporary slot is uncovered. A qualified joint route fits only with separate start cash and timely receiving.")
print("The separate national price change adds 240 of live deposit exposure and a 40 headroom gap.")
