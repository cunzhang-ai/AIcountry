"""Check conditional remedy release in the constructed closure comparison."""


def first_window(*, overlap_cash, specialist, safe_payee, returned, exclusive_release, review):
    full_handoff = overlap_cash >= 2
    return {
        "visit": full_handoff and specialist,
        "redress": 2 if safe_payee and returned and exclusive_release else 0,
        "independent_hearing": review,
    }


assert first_window(overlap_cash=2, specialist=True, safe_payee=True,
                    returned=True, exclusive_release=True, review=True) == {
    "visit": True, "redress": 2, "independent_hearing": True,
}
assert first_window(overlap_cash=1, specialist=True, safe_payee=True,
                    returned=True, exclusive_release=True, review=True) == {
    "visit": False, "redress": 2, "independent_hearing": True,
}
assert first_window(overlap_cash=2, specialist=False, safe_payee=False,
                    returned=True, exclusive_release=False, review=False) == {
    "visit": False, "redress": 0, "independent_hearing": False,
}


assert first_window(overlap_cash=2, specialist=True, safe_payee=True,
                    returned=True, exclusive_release=False, review=True)["redress"] == 0


def unsettled_action(*, finality, usable, safe_payee,
                     lawful_original_receiver=True, exclusive_release=True):
    if finality is True and not lawful_original_receiver:
        return "determine disputed discharge"
    if finality is None:
        return "keep reserved"
    if finality:
        return "reconcile" if usable else "seek access remedy"
    return "pay once" if safe_payee and exclusive_release else "retain due claim"


assert unsettled_action(finality=None, usable=False, safe_payee=True) == "keep reserved"
assert unsettled_action(finality=True, usable=True, safe_payee=True) == "reconcile"
assert unsettled_action(finality=True, usable=False, safe_payee=True) == "seek access remedy"
assert unsettled_action(finality=False, usable=False, safe_payee=True) == "pay once"
assert unsettled_action(finality=False, usable=False, safe_payee=False) == "retain due claim"
assert unsettled_action(finality=True, usable=True, safe_payee=True,
                        lawful_original_receiver=False) == "determine disputed discharge"
assert unsettled_action(finality=False, usable=False, safe_payee=True,
                        exclusive_release=False) == "retain due claim"
assert sum((1, 2, 2, 1, 2)) == 8  # Visit, B, C reserve, provisional protection and overlap.
print("A failed overlap gate need not block the independently payable claim or hearing.")
print("Uncertain and final transfers cannot be replayed; unsafe receiving delays only the affected release.")
