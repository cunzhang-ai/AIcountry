"""Check protected funding and the optional grant in the constructed case."""


def service_gap(own_funding: int, equalization: int, settled_by_payroll: bool) -> int:
    protected_cost = 10
    usable_grant = equalization if settled_by_payroll else 0
    return max(0, protected_cost - own_funding - usable_grant)


if __name__ == "__main__":
    assert service_gap(2, 8, settled_by_payroll=False) == 8
    assert service_gap(4, 6, settled_by_payroll=False) == 6
    assert service_gap(2, 8, settled_by_payroll=True) == 0
    assert service_gap(4, 6, settled_by_payroll=True) == 0
    optional_envelope = 8
    accepted_projects = {"North": 0, "South": 4}
    assert optional_envelope - sum(accepted_projects.values()) == 4
    print("Declining an optional grant leaves the protected transfer and service duty intact.")
