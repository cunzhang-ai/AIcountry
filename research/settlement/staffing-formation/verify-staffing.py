"""Reconcile a sourced historical comparison and a separate authored roster."""

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Option:
    early_cash: int
    recurring_cash: int
    early_receiving: int
    early_origin: int
    later_receiving: int
    later_origin: int

    def can_continue(self):
        return (
            self.early_cash <= 6
            and self.recurring_cash <= 5
            and min(self.early_receiving, self.later_receiving) >= 18
            and min(self.early_origin, self.later_origin) >= 20
        )


def compare_sources():
    evidence = (
        Path(__file__).resolve().parents[2]
        / "2026-11-staffing-formation-and-first-service-capacity"
        / "observations.json"
    )
    source = json.loads(evidence.read_text())
    agreements = source["reported_agreements"]
    target = source["annual_2022_to_2026_agreement_targets"]
    for counts in (agreements, target, source["annual_2027_to_2031_agreement_targets"]):
        assert counts["assistant"] + counts["helper"] == counts["total"]
    differences = {role: agreements[role] - target[role] for role in agreements}
    assert differences == source["differences_reported_minus_target"]
    assert differences == {"assistant": -510, "helper": 1468, "total": 958}
    allocation = source["supervisor_measure_annual_allocation_dkk_million_2025_to_2028"]
    assert round(allocation["state_education"] + allocation["municipal_regional_application_pool"], 1) == allocation["total"]
    assert source["verified_2024_cohort_qualification"] is None
    assert source["verified_2024_cohort_paid_service_shifts"] is None
    print("Observed agreements versus targets:", differences)


def compare_rosters():
    baseline_early = 20
    baseline_later = baseline_early - 2
    origin = 20
    offers, entries, qualifications, deployments, retained = (8, 6, 4, 3, 2)
    assert offers >= entries >= qualifications >= deployments >= retained
    early_mentors = 3
    replacement = 1
    saved_shifts = 2
    willing_return = 1
    moved_shifts = 4
    origin_replacement = 1
    staffed_during_training = baseline_early - early_mentors + replacement
    retained_receiving = baseline_later + saved_shifts + willing_return

    baseline = Option(0, 0, baseline_early, origin, baseline_later, origin)
    retention = Option(3, 3, baseline_early, origin, retained_receiving, origin)
    transfer = Option(3, 4, baseline_early, origin,
                      baseline_later + moved_shifts, origin - moved_shifts + origin_replacement)
    cohort = Option(4, 3, staffed_during_training, origin, baseline_later + retained, origin)
    cohort_loss = Option(4, 3, staffed_during_training - replacement, origin,
                         baseline_later + retained, origin)
    combined = Option(retention.early_cash + cohort.early_cash,
                      retention.recurring_cash + cohort.recurring_cash,
                      staffed_during_training, origin, retained_receiving + retained, origin)
    small_cohort = Option(3, 2, baseline_early - 2 + replacement, origin,
                          baseline_later + 1, origin)
    staged = Option(retention.early_cash + small_cohort.early_cash,
                    retention.recurring_cash + small_cohort.recurring_cash,
                    small_cohort.early_receiving, origin, retained_receiving + 1, origin)
    staged_loss = Option(staged.early_cash, staged.recurring_cash,
                         staged.early_receiving - replacement, origin,
                         staged.later_receiving - 1, origin)
    assert baseline.can_continue() and retention.can_continue() and cohort.can_continue()
    assert not transfer.can_continue() and transfer.later_origin == 17
    assert transfer.later_receiving + transfer.later_origin == baseline_later + origin + 1
    assert not cohort_loss.can_continue() and cohort_loss.early_receiving == 17
    assert not combined.can_continue() and (combined.early_cash, combined.recurring_cash) == (7, 6)
    assert (retained_receiving, retained_receiving - 1, retained_receiving - saved_shifts) == (21, 20, 19)
    print("Transfer adds one net shift but leaves three uncovered at origin.")
    print("The cohort retains two later shifts and falls to 17 early if backfill fails.")
    assert (staged.early_cash, staged.recurring_cash) == (6, 5)
    assert (staged.early_receiving, staged.later_receiving) == (19, 22)
    assert (staged_loss.early_receiving, staged_loss.later_receiving) == (18, 21)
    assert staged.can_continue() and staged_loss.can_continue()
    print("Full training with retention exceeds both cash limits.")
    print("Staggered training with retention fits both limits and retains 18 early and 21 later shifts under the declared loss.")


if __name__ == "__main__":
    compare_sources()
    compare_rosters()
