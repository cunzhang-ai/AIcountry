"""Verify the constructed receipt and equalization comparisons."""

from fractions import Fraction


def grant(need, capacity):
    return max(0, need - Fraction(3, 4) * capacity)


separate_awards = [grant(50, 10), grant(50, 90)]
combined_award = grant(100, 100)
assert separate_awards == [Fraction(85, 2), 0]
assert combined_award == 25
assert sum(separate_awards) - combined_award == Fraction(35, 2)
assert 50 - (10 + combined_award + 5) == 10
assert 50 - (10 + combined_award + 15) == 0

eligible = {"dense": 20, "remote": 20}
mandatory_app = {"dense": 20, "remote": 12}
qualified_local_route = {"dense": 20, "remote": 20}
assert sum(eligible[key] - mandatory_app[key] for key in eligible) == 8
assert qualified_local_route == eligible


def may_release(*, competent_vote, actual_source, external_disposition, safe_receiving):
    return all((competent_vote, actual_source, external_disposition, safe_receiving))


assert may_release(
    competent_vote=True, actual_source=True, external_disposition=True, safe_receiving=True
)
assert not may_release(
    competent_vote=True, actual_source=True, external_disposition=False, safe_receiving=True
)
assert not may_release(
    competent_vote=True, actual_source=True, external_disposition=True, safe_receiving=False
)

print("An unchanged formula changes the transfer when the map changes. Scope and receipt still need separate proof.")
