"""Check continuing payments and reserved decisions in the constructed handover."""

HOUSING_AWARD = 4


def expansion_can_bind(*, current_authority, exact_approval, conditions_met):
    return current_authority and exact_approval and conditions_met


def award_released(*, binding_award, settlement, exclusive_payer, funds, route_works):
    if binding_award and settlement == "unpaid" and exclusive_payer and route_works:
        return HOUSING_AWARD if funds >= HOUSING_AWARD else 0
    return 0


def receipt_by_deadline(released, *, usable_receipt_at):
    if usable_receipt_at is not None and usable_receipt_at <= 2:
        return released
    return 0


def main():
    assert not expansion_can_bind(current_authority=False, exact_approval=True, conditions_met=True)
    assert not expansion_can_bind(current_authority=True, exact_approval=False, conditions_met=True)
    assert not expansion_can_bind(current_authority=True, exact_approval=True, conditions_met=False)
    assert expansion_can_bind(current_authority=True, exact_approval=True, conditions_met=True)

    unpaid_award = dict(
        binding_award=True, settlement="unpaid", exclusive_payer=True, funds=4, route_works=True
    )
    released = award_released(**unpaid_award)
    assert released == 4
    assert receipt_by_deadline(released, usable_receipt_at=2) == 4
    assert receipt_by_deadline(released, usable_receipt_at=3) == 0
    assert receipt_by_deadline(released, usable_receipt_at=None) == 0
    for missing in ("binding_award", "exclusive_payer", "route_works"):
        assert award_released(**(unpaid_award | {missing: False})) == 0
    assert award_released(**(unpaid_award | {"funds": 3})) == 0
    for status in ("settled", "unknown"):
        assert award_released(**(unpaid_award | {"settlement": status})) == 0
    print("Deferred acts: current authority, continuing duties, independent payment and no replay passed.")


if __name__ == "__main__":
    main()
