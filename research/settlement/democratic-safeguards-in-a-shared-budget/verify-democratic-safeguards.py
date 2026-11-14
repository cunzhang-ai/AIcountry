"""Check the constructed shared budget under real controller loss."""

limit = 12
costs = {"R": 11, "M": 8, "S": 10, "H": 9}
assert all(cost <= limit for cost in costs.values())
assert costs["R"] - costs["S"] == 1
assert 8 + 1 + 1 == costs["S"]


def delivered(*, common_available, separate_evidence_and_execution, later_payroll, competent_reviewer,
              executor_accepted=True, opposition_access=True, court_records=True):
    evidence = common_available or separate_evidence_and_execution
    executed = evidence and court_records and competent_reviewer and executor_accepted
    evidence = evidence and opposition_access
    payroll = common_available or later_payroll
    return evidence, executed, payroll


assert delivered(common_available=False, separate_evidence_and_execution=False,
                 later_payroll=False, competent_reviewer=True) == (False, False, False)
assert delivered(common_available=False, separate_evidence_and_execution=True,
                 later_payroll=False, competent_reviewer=True) == (True, True, False)
assert delivered(common_available=False, separate_evidence_and_execution=True,
                 later_payroll=True, competent_reviewer=True) == (True, True, True)
assert delivered(common_available=False, separate_evidence_and_execution=True,
                 later_payroll=True, competent_reviewer=False) == (True, False, True)
assert delivered(common_available=False, separate_evidence_and_execution=True,
                 later_payroll=True, competent_reviewer=True,
                 executor_accepted=False) == (True, False, True)
assert delivered(common_available=False, separate_evidence_and_execution=True,
                 later_payroll=True, competent_reviewer=True,
                 opposition_access=False) == (False, True, True)
print("Fiscal alternatives, actual execution and the separate later review call verified.")
