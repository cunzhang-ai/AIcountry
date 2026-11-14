"""Check purpose separation and the joint receiving limits of a constructed case."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class PublicDuty:
    legal_facts_verified: bool = True
    uses_unrelated_label: bool = False
    review_slot: str | None = None
    received_in_time: bool = True

    @property
    def lawfully_delivered(self):
        return (
            self.legal_facts_verified
            and not self.uses_unrelated_label
            and self.review_slot is not None
            and self.received_in_time
        )


def delivered_count(housing, ride):
    # In this case each distinct paid slot can support only one duty.
    return len({duty.review_slot for duty in (housing, ride) if duty.lawfully_delivered})


def main():
    housing = PublicDuty(review_slot="housing review")
    ride = PublicDuty(review_slot="ride review")
    labeled_housing = replace(housing, uses_unrelated_label=True)
    labeled_ride = replace(ride, uses_unrelated_label=True)

    assert delivered_count(labeled_housing, labeled_ride) == 0
    assert delivered_count(housing, ride) == 2
    assert delivered_count(housing, replace(ride, review_slot=housing.review_slot)) == 1
    assert delivered_count(housing, replace(ride, review_slot=None)) == 1
    assert delivered_count(replace(housing, review_slot=None), ride) == 1
    assert delivered_count(replace(housing, legal_facts_verified=False), ride) == 1
    assert delivered_count(housing, replace(ride, received_in_time=False)) == 1
    print("Purpose limits: separate lawful proof, shared review capacity and actual receipt passed.")


if __name__ == "__main__":
    main()
