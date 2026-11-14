def timely_service(funded, accepted, receipt_day, due_day):
    return funded and accepted and receipt_day <= due_day


def qualifying_omissions(verified_intake, agency_export):
    return verified_intake - agency_export


def verify():
    verified_intake = set(range(1, 9))
    agency_export = {1, 2, 3, 4, 5, 6}
    assert qualifying_omissions(verified_intake, agency_export) == {7, 8}

    investigation_cost = 3
    care_cost = 4
    shared_budget = 6
    assert investigation_cost + care_cost - shared_budget == 1

    assert timely_service(True, True, 1, 1)
    assert not timely_service(True, True, 2, 1)
    assert not timely_service(True, False, 1, 1)
    assert not timely_service(False, True, 1, 1)
    print('Two verified intakes are missing, and one shared provision cannot fund both timely care and investigation.')


if __name__ == '__main__':
    verify()
