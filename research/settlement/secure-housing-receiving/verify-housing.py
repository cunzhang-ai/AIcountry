"""Reproduce Design235's authored same-room and two-period comparison."""

from collections import Counter

OPTIONS = {
    "direct": (8, None),
    "independent bridge": (5 + 6, "alternate room"),
    "shared room": (4 + 6, "local room"),
}
PREVENTION = 5
C_LOCAL_ROOM = 4
B_RECURRING = 6
BRIDGE_NIGHTS = range(4)


def coverage(first_budget, later_budget, available_options):
    payable_now = {}
    durable = {}
    for option in available_options:
        housing_cost, room = OPTIONS[option]
        occupancy = Counter(("local room", night) for night in BRIDGE_NIGHTS)
        if room is not None:
            occupancy.update((room, night) for night in BRIDGE_NIGHTS)
        cost = PREVENTION + housing_cost + C_LOCAL_ROOM
        if max(occupancy.values()) > 1 or cost > first_budget:
            continue
        payable_now[option] = cost
        if B_RECURRING <= later_budget:
            durable[option] = cost
    return payable_now, durable


if __name__ == "__main__":
    direct = {"direct": 17}
    both = {"direct": 17, "independent bridge": 20}
    assert coverage(17, 6, OPTIONS) == (direct, direct)
    assert coverage(20, 6, OPTIONS) == (both, both)
    assert coverage(16, 6, OPTIONS) == ({}, {})
    assert coverage(20, 5, OPTIONS) == (both, {})
    assert coverage(19, 6, ["shared room"]) == ({}, {})
    alternate = {"independent bridge": 20}
    assert coverage(20, 6, ["independent bridge", "shared room"]) == (
        alternate, alternate
    )
    print("Matched direct package: 17. Independent bridge: 20.")
    print("Shared room is double-booked. A later budget of 5 cannot sustain either.")
