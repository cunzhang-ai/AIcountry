"""Check constructed staffing costs and usable visits by service and window."""

OLD_DUE = 6
NEW_DUE = 2
STARTUP_NEEDED = 2 + 1
RECURRING_NEEDED = 2 + 1


def delivered(*, original_slots, departing, original_replacements, new_slots,
              original_accepted=OLD_DUE, new_accepted=NEW_DUE):
    old = min(OLD_DUE, original_slots - departing + original_replacements, original_accepted)
    new = min(NEW_DUE, new_slots, new_accepted)
    return old, new


def training_qualifies(*, startup, backfill, consent, independent_assessment):
    return startup >= STARTUP_NEEDED and backfill and consent and independent_assessment


assert training_qualifies(startup=3, backfill=True, consent=True, independent_assessment=True)
assert not training_qualifies(startup=2, backfill=True, consent=True, independent_assessment=True)
assert not training_qualifies(startup=3, backfill=False, consent=True, independent_assessment=True)
assert not training_qualifies(startup=3, backfill=True, consent=False, independent_assessment=True)
assert RECURRING_NEEDED == 3
assert delivered(original_slots=6, departing=2, original_replacements=0, new_slots=2) == (4, 2)
assert delivered(original_slots=6, departing=0, original_replacements=0, new_slots=2) == (6, 2)
assert delivered(original_slots=6, departing=1, original_replacements=0, new_slots=2) == (5, 2)
assert delivered(original_slots=6, departing=1, original_replacements=1, new_slots=2) == (6, 2)
assert delivered(original_slots=6, departing=0, original_replacements=0, new_slots=2,
                 new_accepted=1) == (6, 1)
assert delivered(original_slots=6, departing=0, original_replacements=0, new_slots=1) == (6, 1)

# The staffing plan and actual receipt are distinct in each service window.
assert delivered(original_slots=6, departing=0, original_replacements=0, new_slots=2,
                 new_accepted=0) == (6, 0)
def shared_origin_windows(*, reserve_reassigned):
    urgent_covered = 1 - reserve_reassigned
    ordinary, destination = delivered(
        original_slots=6, departing=2,
        original_replacements=reserve_reassigned, new_slots=2,
    )
    return ordinary, destination, urgent_covered


assert shared_origin_windows(reserve_reassigned=0) == (4, 2, 1)
assert shared_origin_windows(reserve_reassigned=1) == (5, 2, 0)
assert delivered(original_slots=6, departing=0, original_replacements=0, new_slots=0) == (6, 0)

print("Recruitment from an uncovered roster delivers six total. Protected training and return can deliver eight.")
print("Retirement, unavailable cover or missing acceptance leaves a distinct gap.")
