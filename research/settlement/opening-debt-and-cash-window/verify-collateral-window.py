"""Check the separate foreign-currency window and the effect of actual substitution."""

OPENING_FX = 8
DUE_CREDITOR = 3
DUE_IMPORT = 2
PROTECTED_MINIMUM = 1
OPTIONAL_SUPPLIER = 2


def room_at_cutoff(*, margin, adjusted_pledge_value=0, substitute_accepted=False):
    effective_pledge = min(adjusted_pledge_value, margin) if substitute_accepted else 0
    cash_margin = margin - effective_pledge
    return OPENING_FX - DUE_CREDITOR - DUE_IMPORT - PROTECTED_MINIMUM - cash_margin


assert room_at_cutoff(margin=0) == OPTIONAL_SUPPLIER
assert room_at_cutoff(margin=2) == 0
assert room_at_cutoff(margin=2, adjusted_pledge_value=2) == 0
assert room_at_cutoff(margin=2, adjusted_pledge_value=0, substitute_accepted=True) == 0
assert room_at_cutoff(margin=2, adjusted_pledge_value=4 // 2,
                      substitute_accepted=True) == OPTIONAL_SUPPLIER
print("Gross creditor and essential imports, collateral and opening FX cutoff verified.")
