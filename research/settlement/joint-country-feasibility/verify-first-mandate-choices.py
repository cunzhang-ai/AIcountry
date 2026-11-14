"""Reproduce the authored joint choice with no early knowledge of the loss."""

from itertools import product


losses = ("care", "hearing")
reserve_options = {frozenset(), frozenset({"care"}), frozenset({"hearing"}), frozenset(losses)}
budget = 3
admissible_initial_choices = {choice for choice in reserve_options if 2 * len(choice) <= budget}
assert all(any(loss in choice for choice in admissible_initial_choices) for loss in losses)
assert not any(all(loss in choice for loss in losses) for choice in admissible_initial_choices)

booking_cutoff, information_received, service_cutoff = 1, 4, 6
assert booking_cutoff < information_received
assert information_received + 2 <= service_cutoff < 5 + 2
assert 3 <= budget < 4
def switch_completes(failed, received_signal, signal_time):
    due = set(failed)
    if received_signal not in due or signal_time + 2 > service_cutoff:
        return set()
    return {received_signal}


for loss in losses:
    assert switch_completes({loss}, loss, 4) == {loss}
    assert not switch_completes({loss}, loss, 5)
    assert not switch_completes({loss}, None, 4)
for signal in losses:
    assert switch_completes(losses, signal, 4) != set(losses)
assert budget < 3 + 1 == 2 + 2


def can_assign(duty_workers):
    return any(len(set(team)) == len(duty_workers) for team in product(*duty_workers))


assert not can_assign(({"specialist"}, {"specialist"}, {"poll officer"}))
assert can_assign(({"specialist"}, {"second specialist"}, {"poll officer"}))

shared_eligibility = ({"A"}, {"A"}, {"B", "C"}, {"C", "D"})
assert not can_assign(shared_eligibility)
assert not can_assign(({"A"}, {"A"}, {"B", "C", "E"}, {"C", "D"}))
assert can_assign(({"A"}, {"A", "E"}, {"B", "C"}, {"C", "D"}))

print("A hindsight plan can pass every branch while no executable early choice covers them together.")
