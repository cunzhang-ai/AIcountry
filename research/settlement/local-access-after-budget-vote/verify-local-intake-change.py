"""Check the difference between scope authority, readiness and actual receiving."""


def classify_change(*, covered_scope, required_instrument_matches, delegated_method):
    if covered_scope and required_instrument_matches and delegated_method:
        return "local operating change"
    return "return affected scope to competent authority"


def optional_release(*, authorized, accessible, hearing_protected, independent_appeal,
                     cash, required_cash, separately_authorized=frozenset()):
    if not authorized or not hearing_protected or not independent_appeal or cash < required_cash:
        return set()
    if len(accessible) == 2:
        return accessible
    return accessible & separately_authorized


def delivered(released, *, meaning_confirmed, timely_receipt):
    return released & meaning_confirmed & timely_receipt


assert classify_change(covered_scope=True, required_instrument_matches=True,
                       delegated_method=True) == "local operating change"
assert classify_change(covered_scope=False, required_instrument_matches=True,
                       delegated_method=True) == "return affected scope to competent authority"
assert classify_change(covered_scope=True, required_instrument_matches=False,
                       delegated_method=True) == "return affected scope to competent authority"
assert classify_change(covered_scope=True, required_instrument_matches=True,
                       delegated_method=False) == "return affected scope to competent authority"

base = dict(authorized=True, accessible={"A", "B"}, hearing_protected=True,
            independent_appeal=True, cash=4, required_cash=4)
released = optional_release(**base)
assert released == {"A", "B"}
assert optional_release(**(base | {"accessible": {"A"}})) == set()
assert optional_release(**(base | {"accessible": {"A"}, "separately_authorized": {"A"}})) == {"A"}
assert optional_release(**(base | {"accessible": {"A"}, "separately_authorized": {"B"}})) == set()
assert optional_release(**(base | {"cash": 4, "required_cash": 5})) == set()
assert optional_release(**(base | {"hearing_protected": False})) == set()
assert optional_release(**(base | {"independent_appeal": False})) == set()
assert optional_release(**(base | {"authorized": False})) == set()
assert delivered(released, meaning_confirmed={"A", "B"}, timely_receipt={"A", "B"}) == {"A", "B"}
assert delivered(released, meaning_confirmed={"A"}, timely_receipt={"A", "B"}) == {"A"}
assert delivered(released, meaning_confirmed={"A", "B"}, timely_receipt={"A"}) == {"A"}

print("A delegated accessible change can preserve the same authorization and both sessions.")
print("Missing access, authority, timely cash or independent hearing protection constrains the optional release.")
