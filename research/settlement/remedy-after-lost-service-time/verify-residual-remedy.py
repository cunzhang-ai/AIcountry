"""Check the constructed remedy and independently funded service."""

def main():
    direct_loss, received_for_same_loss = 6, 2
    award = direct_loss - received_for_same_loss
    assert award == 4
    for reserve, remaining in ((3, 1), (4, 0)):
        assert award - min(award, reserve) == remaining
    assert 7 + 1 + award == 12
    deadline, substitute_received = 1, 2
    assert substitute_received > deadline
    print("Residual remedy: separate service, actual recovery and award passed.")

if __name__ == "__main__":
    main()
