"""Reproduce the authored paid-time and care-coverage comparison."""


def roster(gross, review, correction, training, qualified, demand):
    net = gross - review - correction - training
    reassigned = min(net, qualified, demand)
    return net - reassigned, demand - reassigned


first_release, first_external = roster(100, 24, 16, 20, 24, 36)
assert (first_release, first_external) == (16, 12)
second_release, second_external = roster(100, 24, 16, 0, 24, 36)
assert (second_release, second_external) == (36, 12)
assert roster(100, 24, 32, 20, 24, 36) == (0, 12)

hourly_external = 2
instructor = 6
assert 36 * hourly_external + instructor == 78
assert 36 * hourly_external == 72
assert first_external * hourly_external + instructor == 30
assert second_external * hourly_external == 24
assert 24 < 36
print("Paid time: verified task hours, qualified care, retained-pay release and stressed cycles passed.")
