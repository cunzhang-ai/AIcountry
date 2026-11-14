"""Check authored scam compensation and the restricted sum and time."""

from fractions import Fraction


def settle(loss, ceiling, returned_before=0, returned_after=0):
    assert 0 <= returned_before + returned_after <= loss
    reimbursement = min(ceiling, loss - returned_before)
    remaining_consumer_loss = loss - returned_before - reimbursement
    returned_to_consumer = min(returned_after, remaining_consumer_loss)
    credited_to_providers = returned_after - returned_to_consumer
    assert credited_to_providers <= reimbursement
    consumer_cash = returned_before + reimbursement + returned_to_consumer
    provider_cost = Fraction(reimbursement - credited_to_providers, 2)
    assert consumer_cash == 2 * provider_cost + returned_before + returned_after
    return reimbursement, consumer_cash, provider_cost


def temporary_hold(available_attributable, reported_loss, first_restriction, now):
    if now >= first_restriction + 4:
        return 0
    return min(available_attributable, reported_loss)


def main():
    loss, attributable, unrelated = (100, 35, 25)
    balance = attributable + unrelated
    held = temporary_hold(attributable, loss, first_restriction=0, now=0)
    assert held == 35 and balance - held == unrelated
    assert temporary_hold(attributable, loss, first_restriction=0, now=3) == 35
    assert temporary_hold(attributable, loss, first_restriction=0, now=4) == 0
    assert temporary_hold(attributable, 20, first_restriction=0, now=1) == 20

    assert settle(loss, 100, returned_before=35) == (65, 100, Fraction(65, 2))
    assert settle(loss, 100, returned_after=35) == (100, 100, Fraction(65, 2))
    assert settle(loss, 100) == (100, 100, 50)
    assert settle(loss, 80, returned_after=35) == (80, 100, Fraction(65, 2))
    assert settle(loss, 80) == (80, 80, 40)

    gross_sender, consumer_cash, final_each = settle(loss, 100)
    assert (gross_sender, consumer_cash, gross_sender - final_each) == (100, 100, 50)

    print("Restrict 35 only, leave 25 available, and release at hour four without further authority.")
    print("Return of 35 leaves net provider cost 32.5 each, whether before or after first payment.")
    print("A temporary hold with no actual return leaves provider cost 50 each.")
    print("At an 80 ceiling, later recovery first covers the remaining consumer loss.")
    print("Consumer receives 100 while the sender awaits the other provider's 50 contribution.")


if __name__ == "__main__":
    main()
