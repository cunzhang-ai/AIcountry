"""Check the stipulated functional windows and paid continuity comparison."""

USEFUL_HOURS = {"indoor": 8, "community": 18, "communication": 4}
OPERATING_CASH = 700
SUPPLIER_CLAIM = 500
AVAILABLE_RECOVERY = 0


def unmet_functions(deliveries):
    return {
        function
        for function, deadline in USEFUL_HOURS.items()
        if function not in deliveries or deliveries[function] > deadline
    }


fitting_and_delivery = 100
communication_replacement = 350
indoor_option = 250 + communication_replacement + fitting_and_delivery
full_option = 450 + communication_replacement + fitting_and_delivery
usable_cash = OPERATING_CASH + AVAILABLE_RECOVERY

assert indoor_option == usable_cash == 700
assert full_option == 900
assert full_option - usable_cash == 200
assert OPERATING_CASH + SUPPLIER_CLAIM >= full_option > usable_cash

assert unmet_functions({}) == set(USEFUL_HOURS)
assert unmet_functions({"indoor": 6, "communication": 3}) == {"community"}
assert unmet_functions({"indoor": 6, "community": 16, "communication": 3}) == set()
assert unmet_functions({"indoor": 6}) == {"community", "communication"}
assert unmet_functions({"indoor": 6, "community": 16, "communication": 6}) == {"communication"}
assert 6 - USEFUL_HOURS["communication"] == 2

print("Assistive equipment comparison passed: paid capacity, shared failure and actual function.")
