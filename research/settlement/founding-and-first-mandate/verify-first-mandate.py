"""Verify separation of the authored authority and delivery branches."""

import re
from pathlib import Path

source = Path(__file__).with_name("01-adoption-register-and-first-mandate.md")
chapters = re.findall(r"^\| \[C(\d\d) ", source.read_text(), re.MULTILINE)
assert chapters == [f"{i:02}" for i in range(1, 15)]


def contest(*, prior_rules, paid_independent_path, valid_result, valid_formation, handover):
    if not prior_rules or not paid_independent_path:
        return "unqualified"
    if not valid_result:
        return "result unresolved"
    if not valid_formation:
        return "valid assembly; no new cabinet"
    return "office received" if handover else "office conferred; transfer unverified"


qualified = {
    "prior_rules": True,
    "paid_independent_path": True,
    "valid_result": True,
    "valid_formation": True,
    "handover": True,
}
assert contest(**qualified) == "office received"
assert contest(**(qualified | {"prior_rules": False})) == "unqualified"
assert contest(**(qualified | {"paid_independent_path": False})) == "unqualified"
assert contest(**(qualified | {"valid_result": False})) == "result unresolved"
assert contest(**(qualified | {"valid_formation": False})) == "valid assembly; no new cabinet"
assert contest(**(qualified | {"handover": False})) == "office conferred; transfer unverified"


def service(*, exact_authority, release_ready, duty_binding, received):
    if duty_binding:
        return "received" if received else "due; remedy continues"
    if exact_authority and release_ready:
        return "received" if received else "eligible to release"
    return "hold optional act"


assert service(exact_authority=False, release_ready=True,
               duty_binding=False, received=False) == "hold optional act"
assert service(exact_authority=True, release_ready=False,
               duty_binding=False, received=False) == "hold optional act"
assert service(exact_authority=True, release_ready=True,
               duty_binding=False, received=False) == "eligible to release"
assert service(exact_authority=True, release_ready=False,
               duty_binding=True, received=False) == "due; remedy continues"
assert service(exact_authority=True, release_ready=False,
               duty_binding=True, received=True) == "received"
print("Fourteen chapters and distinct authority, release and binding-duty cases verified.")
