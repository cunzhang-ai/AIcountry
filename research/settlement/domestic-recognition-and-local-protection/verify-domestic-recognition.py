"""Check the timing and distinct receipt gates in the constructed two-site case."""

SERVICE_DEADLINE = 4
DISPATCH_PAYMENT_DEADLINE = 3
BACKUP_PRICE = 4
BACKUP_ARRIVAL = 4
LOCAL_INSPECTION_DAYS = 1
INSTALLATION_DAYS = 1


def original_receipt(evidence_days, *, claim_covered, batch_held, site_approved):
    if not claim_covered or batch_held or not site_approved:
        return None
    return evidence_days + LOCAL_INSPECTION_DAYS + INSTALLATION_DAYS


def backup_receipt(payments, *, receiving_confirmed):
    timely_cash = sum(
        amount for day, amount in payments if day <= DISPATCH_PAYMENT_DEADLINE
    )
    if timely_cash < BACKUP_PRICE or not receiving_confirmed:
        return None
    return BACKUP_ARRIVAL


def in_time(receipt):
    return receipt is not None and receipt <= SERVICE_DEADLINE


def main():
    repeated = tuple(
        original_receipt(3, claim_covered=True, batch_held=False, site_approved=True)
        for _ in range(2)
    )
    recognized = tuple(
        original_receipt(1, claim_covered=True, batch_held=False, site_approved=True)
        for _ in range(2)
    )
    assert repeated == (5, 5) and not any(map(in_time, repeated))
    assert recognized == (3, 3) and all(map(in_time, recognized))

    site_a = recognized[0]
    mismatched = original_receipt(1, claim_covered=False, batch_held=False, site_approved=True)
    site_rejected = original_receipt(1, claim_covered=True, batch_held=False, site_approved=False)
    held = original_receipt(1, claim_covered=True, batch_held=True, site_approved=True)
    assert in_time(site_a)
    assert mismatched is None and site_rejected is None and held is None

    funded = backup_receipt([(3, 4)], receiving_confirmed=True)
    late = backup_receipt([(3, 3), (4, 1)], receiving_confirmed=True)
    unreceived = backup_receipt([(3, 4)], receiving_confirmed=False)
    assert funded == SERVICE_DEADLINE
    assert late is None and unreceived is None
    print("Domestic recognition: timing, scope, site inspection, batch hold, payment and receipt passed.")


if __name__ == "__main__":
    main()
