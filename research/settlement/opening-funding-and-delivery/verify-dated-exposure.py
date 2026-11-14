"""Verify cumulative obligations under the authored backup contract options."""

def qualifies(available_cash, mutually_exclusive, lawful_scope=True):
    booking = 1
    review = 1
    main = 2
    alternate = 3
    adverse_cost = max(main, alternate) if mutually_exclusive else main + alternate
    required_cash = (booking, booking + review + adverse_cost)
    return lawful_scope and all(
        actual >= required for actual, required in zip(available_cash, required_cash, strict=True)
    )

assert qualifies((1, 5), True)
assert not qualifies((1, 4), True)
assert not qualifies((0, 5), True)
assert not qualifies((1, 0), True)
assert not qualifies((1, 5), False)
assert qualifies((1, 7), False)
assert not qualifies((1, 7), True, lawful_scope=False)
print("The exclusive fallback needs five by cutoff; concurrent binding charges need seven.")
