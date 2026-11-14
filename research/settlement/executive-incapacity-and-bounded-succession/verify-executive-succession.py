def standing_payment(settled, qualified_payer, accepting_receiver):
    return settled and qualified_payer and accepting_receiver


def authenticated_activation(attesting_ministers, acting_claimants, originals_verified):
    signers = set(attesting_ministers)
    return len(signers) == 2 and signers.isdisjoint(acting_claimants) and originals_verified


def provisional_authority(hour_since_activation, available_roster_member, activation, disputed):
    return 0 <= hour_since_activation < 24 and available_roster_member and activation and not disputed


def verify():
    assert standing_payment(True, True, True)
    assert not standing_payment(True, True, False)

    approved_actor = {"substitute"}
    valid_activation = authenticated_activation(["minister A", "minister B"], approved_actor, True)
    assert valid_activation
    assert not authenticated_activation(["minister A", "minister A"], approved_actor, True)
    assert not authenticated_activation(["minister A", "substitute"], approved_actor, True)
    assert not authenticated_activation(["minister A", "minister B"], approved_actor, False)

    assert provisional_authority(6, True, valid_activation, False)
    assert not provisional_authority(6, True, False, False)
    assert not provisional_authority(6, True, valid_activation, True)
    assert not provisional_authority(6, False, valid_activation, False)
    assert provisional_authority(23, True, valid_activation, False)
    assert not provisional_authority(24, True, valid_activation, False)

    for receiving_site_available in (True, False):
        authorized = provisional_authority(6, True, valid_activation, False)
        received = authorized and receiving_site_available
        assert authorized and received == receiving_site_available
    print('Standing payment survives the contested branch. Reserved action needs valid cover and timely acceptance, and provisional cover expires at hour 24.')


if __name__ == '__main__':
    verify()
