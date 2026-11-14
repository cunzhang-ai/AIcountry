"""Reproduce individual and joint availability in the constructed catchment."""

workers = set("ABCDEFGHIJKL")
care = set("ABCDEFGH")
transport = set("EFGHIJKL")


def usable(offers, care_places, travel_places):
    return offers & care_places & travel_places


assert usable(workers, care, transport) == set("EFGH")
assert len(usable(workers, workers, transport)) == 8
assert len(usable(workers, care, workers)) == 8
assert usable(workers, workers, workers) == workers
assert not usable(set(), workers, workers)
offers_with_a_shared_verification_gate = workers - set("GHIJKL")
assert len(usable(offers_with_a_shared_verification_gate, workers, workers)) == 6
replacement_buyer_orders = set("ABCDEFGH")
assert len(usable(replacement_buyer_orders, workers, workers)) == 8

existing_medical = {"driver-1"}
proposed_work = {"driver-1"}
replacement_work = {"driver-2"}
assert existing_medical & proposed_work
assert not (existing_medical & replacement_work)

def reachable(*, minutes_needed, minutes_released, accepted_receiver, necessary_cover):
    return minutes_released >= minutes_needed and accepted_receiver and necessary_cover


assert reachable(minutes_needed=90, minutes_released=90, accepted_receiver=True, necessary_cover=True)
assert not reachable(minutes_needed=120, minutes_released=0, accepted_receiver=True, necessary_cover=True)
assert not reachable(minutes_needed=120, minutes_released=120, accepted_receiver=True, necessary_cover=False)
assert reachable(minutes_needed=120, minutes_released=120, accepted_receiver=True, necessary_cover=True)
assert not reachable(minutes_needed=120, minutes_released=120, accepted_receiver=False, necessary_cover=True)

print("Matched jobs, independent gate losses and voting-time access reproduced.")
