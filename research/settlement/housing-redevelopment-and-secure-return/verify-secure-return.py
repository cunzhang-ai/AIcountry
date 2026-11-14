"""Check the constructed receiving and additional-offer comparison."""


def uncovered_households(on_site: int, off_site: int, temporary: int = 0) -> int:
    return max(0, 12 - on_site - off_site - temporary)


def net_entrant_offers(accepted_new_homes: int, on_site_returns: int, off_site_replacements: int) -> int:
    return accepted_new_homes - on_site_returns - off_site_replacements


if __name__ == "__main__":
    assert uncovered_households(0, 2, temporary=8) == 2
    assert uncovered_households(10, 2) == 0
    assert uncovered_households(9, 2) == 1
    assert net_entrant_offers(12, 10, 2) == 0
    assert net_entrant_offers(20, 10, 2) == 8
    print("Housing receiving and net additional entrant offers reconcile separately.")
