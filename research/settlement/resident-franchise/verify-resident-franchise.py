"""Reproduce the authored ordinary resident-franchise boundaries."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Residence:
    continuous_months: int
    cumulative_months: int
    current_home: bool = True
    local_home: bool = True
    prior_qualification: bool = False


def eligibility(residence, *, threshold_operates, protected_succession=False):
    national_months = 12 if threshold_operates and not protected_succession else 48
    local = residence.current_home and residence.local_home and residence.cumulative_months >= 6
    national = residence.current_home and (
        residence.prior_qualification or residence.continuous_months >= national_months
    )
    secure_basis = residence.continuous_months >= 48
    return local, national, secure_basis


def initiative_threshold(opening_electorate):
    assert opening_electorate > 0
    return (opening_electorate + 999) // 1000


def check_cases():
    assert eligibility(Residence(8, 8), threshold_operates=True) == (True, False, False)
    established = Residence(18, 18)
    assert eligibility(established, threshold_operates=False) == (True, False, False)
    assert eligibility(established, threshold_operates=True) == (True, True, False)
    assert eligibility(Residence(12, 12), threshold_operates=True) == (True, True, False)
    assert eligibility(Residence(7, 18), threshold_operates=True) == (True, False, False)
    assert eligibility(Residence(48, 48), threshold_operates=False) == (True, True, True)
    assert eligibility(Residence(1, 18, prior_qualification=True), threshold_operates=True) == (True, True, False)
    assert eligibility(Residence(0, 18, current_home=False, prior_qualification=True),
                       threshold_operates=True) == (False, False, False)
    assert eligibility(established, threshold_operates=True, protected_succession=True) == (True, False, False)
    assert initiative_threshold(100_000) == 100
    assert initiative_threshold(103_000) == 103
    assert initiative_threshold(103_001) == 104


if __name__ == "__main__":
    check_cases()
    print("The 18-month resident gains national standing only in the future ordinary scope.")
    print("Local and secure-residence thresholds, actual return, protected succession and separate initiative dates checked.")
