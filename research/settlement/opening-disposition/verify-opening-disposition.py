"""Check conditional opening decisions without using historical figures as cash."""


def disposition(*, ordinary_receipt, quote, authorized_source, cover,
                resident_acceptance, independent_review, next_call,
                effective_motion, accepted_operator):
    funded_alternative = (
        quote and authorized_source and cover
        and resident_acceptance and independent_review and next_call
        and effective_motion and accepted_operator
    )
    return ordinary_receipt, funded_alternative


positive = dict(ordinary_receipt=False, quote=True, authorized_source=True,
                cover=True, resident_acceptance=True, independent_review=True,
                next_call=True, effective_motion=True, accepted_operator=True)
assert disposition(**positive) == (False, True)
for condition in ("quote", "authorized_source", "cover", "resident_acceptance",
                  "independent_review", "next_call", "effective_motion", "accepted_operator"):
    assert disposition(**(positive | {condition: False})) == (False, False)
assert disposition(**(positive | {"ordinary_receipt": True, "quote": False})) == (True, False)
print("Standing receipt and qualification of the finite alternative are separate.")
