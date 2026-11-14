"""Reconcile authored purpose-specific cash and common-failure coverage."""

from dataclasses import dataclass


DUTIES = {"care": 4, "water": 3, "benefit": 4, "court": 3, "election": 2}

# Each route names the dependencies varied by this case.
ORDINARY = {
    "care": ({"direct-care"},),
    "water": ({"ordinary-road-crew"},),
    "benefit": ({"common-signing-root", "benefit-app"},),
    "court": ({"common-signing-root", "court-app"},),
    "election": ({"common-signing-root", "election-app"},),
}
WATER_ALTERNATE = {"independent-water-crew"}


@dataclass(frozen=True)
class Option:
    early: int
    late: int
    recurring: int
    routes: dict[str, tuple[set[str], ...]]

    def exposed_duties(self, lost_dependencies):
        return {
            duty for duty, alternatives in self.routes.items()
            if all(route & lost_dependencies for route in alternatives)
        }

    def funding_gap(self, available, binding_training=False):
        early, cumulative, recurring = available
        training_early, training_late = (1, 1) if binding_training else (0, 0)
        return (
            max(0, self.early + training_early - early),
            max(0, self.early + self.late + training_early + training_late - cumulative),
            max(0, self.recurring - recurring),
        )


def unsupported_due_sources(balances):
    return {duty for duty, amount in DUTIES.items() if balances.get(duty, 0) < amount}


def main():
    assert sum(DUTIES.values()) == 16
    assert unsupported_due_sources(DUTIES) == set()
    assert unsupported_due_sources(dict(DUTIES, benefit=3)) == {"benefit"}

    shared = Option(0, 0, 0, ORDINARY)
    duplicate = Option(1, 0, 1, ORDINARY | {
        "water": (*ORDINARY["water"], WATER_ALTERNATE),
        "benefit": (*ORDINARY["benefit"], {"common-signing-root", "backup-benefit-app"}),
        "court": (*ORDINARY["court"], {"common-signing-root", "backup-court-app"}),
        "election": (*ORDINARY["election"], {"common-signing-root", "backup-election-app"}),
    })
    split = Option(3, 1, 2, ORDINARY | {
        "water": (*ORDINARY["water"], WATER_ALTERNATE),
        "benefit": (*ORDINARY["benefit"], {"independent-benefit-settlement"}),
        "court": (*ORDINARY["court"], {"court-executor", "protected-records-site"}),
        "election": (*ORDINARY["election"], {"election-staff", "protected-records-site"}),
    })
    local = Option(2, 2, 3, {duty: ({f"direct-{duty}-route"},) for duty in DUTIES})
    ordinary, weak = (3, 5, 2), (2, 5, 2)
    combined_loss = {"common-signing-root", "ordinary-road-crew"}

    assert shared.exposed_duties(combined_loss) == {"water", "benefit", "court", "election"}
    assert duplicate.exposed_duties(combined_loss) == {"benefit", "court", "election"}
    assert duplicate.exposed_duties({"benefit-app"}) == set()
    assert split.exposed_duties(combined_loss) == set()
    assert split.exposed_duties(combined_loss | {"protected-records-site"}) == {"court", "election"}
    assert local.exposed_duties(combined_loss) == set()
    assert split.funding_gap(ordinary) == (0, 0, 0)
    assert split.funding_gap(weak) == (1, 0, 0)
    assert local.funding_gap(weak) == (0, 0, 1)

    accelerated = (weak[0] + 1, weak[1], weak[2])
    assert split.funding_gap(accelerated) == (0, 0, 0)
    assert split.funding_gap(weak, binding_training=True) == (2, 1, 0)
    assert split.funding_gap(accelerated, binding_training=True) == (1, 1, 0)
    new_source = (accelerated[0] + 1, accelerated[1] + 1, accelerated[2])
    assert split.funding_gap(new_source, binding_training=True) == (0, 0, 0)

    print("Shared stack loses four protected duties; duplicate with water standby loses three.")
    print("Split alternates protect all five with ordinary funds.")
    print("Losing the split alternate records site also exposes court and election access.")
    print("Weak timing needs one authorized earlier receipt; the local rival needs one recurring unit.")
    print("An already-bound optional claim needs one further early and cumulative unit after timing repair.")
    print("An unfilled restricted benefit source cannot be replaced by general reserve in this case.")


if __name__ == "__main__":
    main()
