"""Check the constructed source, installation and second-window gates."""


def first_ready(*, authority, currency, settlement, onsite, staff, passed_test=True):
    lawful_source = (
        currency == "FX" and settlement is not None and settlement <= 24
        or currency == "domestic" and settlement is not None and settlement <= 42
    )
    return authority and lawful_source and staff and passed_test and max(42, onsite) + 10 <= 52


assert not first_ready(authority=True, currency="FX", settlement=24, onsite=46, staff=True)
assert first_ready(authority=True, currency="FX", settlement=24, onsite=42, staff=True)
assert not first_ready(authority=True, currency="FX", settlement=25, onsite=42, staff=True)
assert first_ready(authority=True, currency="domestic", settlement=42, onsite=42, staff=True)
assert not first_ready(authority=False, currency="domestic", settlement=42, onsite=42, staff=True)
assert not first_ready(authority=True, currency="domestic", settlement=42, onsite=42, staff=False)
assert not first_ready(authority=True, currency="domestic", settlement=42, onsite=42,
                       staff=True, passed_test=False)
assert (15 + 3, 3 + 1, 2 + 1, 2) == (18, 4, 3, 2)


def later_call(*, lawful_source, onsite, staff, verified_finish, binding):
    ready = (
        lawful_source and onsite <= 72 and staff
        and verified_finish is not None and onsite + 11 <= verified_finish < 84
    )
    if ready:
        return "eligible to deliver"
    return "due; remedy continues" if binding else "hold optional start"


later = dict(lawful_source=True, onsite=72, staff=True, verified_finish=83, binding=True)
assert later_call(**later) == "eligible to deliver"
assert later_call(**(later | {"staff": False})) == "due; remedy continues"
assert later_call(**(later | {"lawful_source": False})) == "due; remedy continues"
assert later_call(**(later | {"verified_finish": 85, "binding": False})) == "hold optional start"

# All incoming equipment tests can pass while the in-place cutover
# still interrupts a prior service on the same network.
def cutover_ready(*, cash, isolated, parallel_accepted=False, restoration_paid=False):
    if isolated:
        return cash >= 18
    return cash >= 19 and parallel_accepted and restoration_paid


assert not cutover_ready(cash=18, isolated=False)
assert not cutover_ready(cash=19, isolated=False, parallel_accepted=True)
assert not cutover_ready(cash=18, isolated=False, parallel_accepted=True, restoration_paid=True)
assert cutover_ready(cash=19, isolated=False, parallel_accepted=True, restoration_paid=True)
assert cutover_ready(cash=18, isolated=True)
print("Settlement, site acceptance, live cutover and second-call branches verified.")
