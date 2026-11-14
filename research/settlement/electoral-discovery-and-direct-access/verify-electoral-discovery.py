"""Check the constructed overlap, source roots and useful deadlines."""


def main():
    voters = set(range(100))
    ordinary = set(range(60))
    repaired = ordinary | set(range(60, 70))
    direct = set(range(60, 95))
    assert len(repaired & direct) == 10
    assert len(repaired | direct) == 95
    assert len(voters - (repaired | direct)) == 5
    roots = {"assistant_a": "stale index", "assistant_b": "stale index"}
    assert len(set(roots.values())) == 1

    def received_before(deadline, public, supplemental, delivered_at):
        return public | supplemental if delivered_at <= deadline else public

    assert len(received_before(10, repaired, direct, 9)) == 95
    assert len(received_before(10, repaired, direct, 11)) == 70
    print("Electoral discovery: distinct voters, common source and cutoff passed.")


if __name__ == "__main__":
    main()
