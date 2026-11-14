"""Check the constructed possession and funded receiving comparison."""

WORK_END = 0
USABLE_NOTICE = 2
NOTICE_PERIOD = 30
SECURITY = 220


def possession_day(*, role_necessary, court_order, accepted_home_day):
    if not role_necessary or not court_order or accepted_home_day is None:
        return None
    return max(max(WORK_END, USABLE_NOTICE) + NOTICE_PERIOD, accepted_home_day)


assert possession_day(role_necessary=False, court_order=True, accepted_home_day=32) is None
assert possession_day(role_necessary=True, court_order=False, accepted_home_day=32) is None
assert possession_day(role_necessary=True, court_order=True, accepted_home_day=31) == 32
assert possession_day(role_necessary=True, court_order=True, accepted_home_day=36) == 36
assert possession_day(role_necessary=True, court_order=True, accepted_home_day=None) is None

first_fit, unsuitable_room, accessible_fit = 120, 100, 180
assert first_fit + unsuitable_room == SECURITY
assert SECURITY - first_fit == 100
assert first_fit + accessible_fit - SECURITY == 80
assert first_fit + accessible_fit == SECURITY + 80

print("Employment-linked housing comparison passed: independent tenure, dates, access and funding.")
