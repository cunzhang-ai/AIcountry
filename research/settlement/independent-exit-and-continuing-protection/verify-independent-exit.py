"""Check that funding, safe choice and service dates qualify independently."""

SECURITY = 220
FIRST_HOUSEHOLD = 120
PUBLIC_ACTIVATION = 80
SEPARATE_OPTION = 10
ACTIVATION = 160


def usable_option(*, prior_authority, independent, suitable, safe_contact,
                  displaced_claim, care_accepted, transport_accepted, living_cash,
                  funded_option, settled_activation):
    usable_activation = SECURITY - FIRST_HOUSEHOLD + PUBLIC_ACTIVATION
    return (
        prior_authority and independent and suitable and safe_contact
        and not displaced_claim and care_accepted and transport_accepted and living_cash
        and usable_activation >= ACTIVATION and funded_option and settled_activation
    )


qualified = dict(
    prior_authority=True, independent=True, suitable=True, safe_contact=True,
    displaced_claim=False, care_accepted=True, transport_accepted=True, living_cash=True,
    funded_option=True, settled_activation=True,
)
assert usable_option(**qualified)
for required, present in qualified.items():
    assert not usable_option(**(qualified | {required: not present}))

assert SECURITY - FIRST_HOUSEHOLD == 100
assert ACTIVATION - (SECURITY - FIRST_HOUSEHOLD) == 60
assert PUBLIC_ACTIVATION - 60 == 20
assert SEPARATE_OPTION + ACTIVATION == 170
assert ACTIVATION + 20 == 180  # Separate reactive offer in the inherited case.


def disposition(*, opt_in, expiry, activation_day, qualified_route):
    if not opt_in or not qualified_route or activation_day > expiry:
        return 10, False
    return 170, True


assert disposition(opt_in=False, expiry=32, activation_day=32, qualified_route=True) == (10, False)
assert disposition(opt_in=True, expiry=32, activation_day=33, qualified_route=True) == (10, False)
assert disposition(opt_in=True, expiry=32, activation_day=32, qualified_route=True) == (170, True)
assert disposition(opt_in=True, expiry=32, activation_day=32, qualified_route=False) == (10, False)
print("Independent preparation, separate sources, consent, expiry and affected services verified.")
