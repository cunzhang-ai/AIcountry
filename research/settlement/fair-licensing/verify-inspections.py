#!/usr/bin/env python3
"""Check the scopes and resource loss in the companion example."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Service:
    inspections: int
    qualified_final_decisions: int
    unsupported_final_decisions: int = 0


existing_team = Service(4, 2)
visiting_team = Service(2, 2)
inspection_only_team = Service(2, 0)


def combine(*teams: Service) -> Service:
    return Service(
        sum(team.inspections for team in teams),
        sum(team.qualified_final_decisions for team in teams),
        sum(team.unsupported_final_decisions for team in teams),
    )


local_relicensing = combine(existing_team)
automatic_title = combine(existing_team, visiting_team, Service(2, 0, 2))
recognized_scope = combine(existing_team, visiting_team, inspection_only_team)
unavailable_assessors = combine(existing_team, visiting_team)

assert local_relicensing == Service(4, 2)
assert automatic_title == Service(8, 4, 2)
assert recognized_scope == Service(8, 4)
assert unavailable_assessors == Service(6, 4)
assert recognized_scope.inspections - unavailable_assessors.inspections == 2

print("Scope comparison: 8 inspections and 4 authorized decisions; losing assessors leaves 2 inspections due.")
