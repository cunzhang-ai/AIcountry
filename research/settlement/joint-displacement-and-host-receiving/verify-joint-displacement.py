def usable_offer(legal_vacancy, care_available, transport_available, accepted):
    return legal_vacancy and care_available and transport_available and accepted


def funded_gap(window, dated_receipts, due_costs):
    settled = sum(amount for available_in, amount in dated_receipts if available_in <= window)
    return max(0, sum(due_costs) - settled)


def verify():
    east_committed_care = {"east worker"}
    east_advertised_backup = {"east worker"}
    west_standby = {"west worker"}
    east_free_care = east_advertised_backup - east_committed_care
    west_free_care = west_standby - east_committed_care

    assert not usable_offer(True, bool(east_free_care), True, True)
    assert usable_offer(True, bool(west_free_care), True, True)
    assert usable_offer(True, True, True, True)  # B has no added care task.
    assert not usable_offer(False, True, True, True)
    assert not usable_offer(True, True, True, False)

    due_costs = [5, 3]
    assert funded_gap(1, [(1, 8)], due_costs) == 0
    next_window_receipts = [(2, 6), (3, 2)]
    assert funded_gap(2, next_window_receipts, due_costs) == 2
    assert funded_gap(3, next_window_receipts, due_costs) == 0
    print('Two independently accepted placements fit the first window. The next window needs two more settled units before the reimbursement.')


if __name__ == '__main__':
    verify()
