"""Check paired transfers, shared Treasury cash and each payer's cutoff."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Transfer:
    obligation: str
    recipient: str
    amount: int


def balances(opening, external_net, transfers):
    cash = {payer: amount + external_net[payer] for payer, amount in opening.items()}
    assert len({transfer.obligation for transfer in transfers}) == len(transfers)
    for transfer in transfers:
        cash["Treasury"] -= transfer.amount
        cash[transfer.recipient] += transfer.amount
    assert sum(cash.values()) == sum(opening.values()) + sum(external_net.values())
    return cash


def main():
    opening = {"Treasury": 20, "Local": 2, "Pension": 3, "Operator": 2}
    first = [Transfer("L1", "Local", 5), Transfer("P1", "Pension", 4),
             Transfer("E1", "Operator", 3)]
    ordinary = {"Treasury": 4 - 11, "Local": -7, "Pension": -7, "Operator": -5}
    assert balances(opening, ordinary, first) == dict.fromkeys(opening, 0) | {"Treasury": 1}

    stopped = ordinary | {"Treasury": -11}
    assert balances(opening, stopped, []) == {
        "Treasury": 9, "Local": -5, "Pension": -4, "Operator": -3,
    }
    minimum = 1
    alternate_cost = 1
    insufficient = stopped | {"Treasury": 4 - 11 - alternate_cost}
    assert balances(opening, insufficient, first)["Treasury"] == 0
    covered = stopped | {"Treasury": 5 - 11 - alternate_cost}
    end_first = balances(opening, covered, first)
    assert end_first["Treasury"] == minimum
    for optional_cost in (1, 4):
        assert minimum - (end_first["Treasury"] - optional_cost) == optional_cost

    second = [Transfer("L2", "Local", 3), Transfer("P2", "Pension", 2),
              Transfer("E2", "Operator", 2)]
    second_net = {"Treasury": 20 - 8 - 5, "Local": -3, "Pension": -2, "Operator": -2}
    assert balances(end_first, second_net, second) == end_first
    still_late = second_net | {"Treasury": second_net["Treasury"] - 4}
    assert minimum - balances(end_first, still_late, second)["Treasury"] == 4
    print("Joined opening budget: four payers, paired transfers and two windows passed.")


if __name__ == "__main__":
    main()
