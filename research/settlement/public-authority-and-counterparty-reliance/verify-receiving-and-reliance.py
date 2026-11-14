"""Check the constructed continuity and residual payment counterexample."""

def main():
    orders = {"binding earlier order": True, "new expired direction": False}
    assert [name for name, authority in orders.items() if authority] == ["binding earlier order"]
    reasonable_loss, actual_recovery = 6, 2
    award = reasonable_loss - actual_recovery
    assert award == 4
    for reserve, remaining in ((3, 1), (4, 0)):
        assert award - min(award, reserve) == remaining
    assert 8 + 1 + award == 13
    print("Handover: continuing order and separate reliance remedy passed.")


if __name__ == "__main__":
    main()
