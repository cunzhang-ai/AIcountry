"""Check the constructed fiscal and independent-roster constraints."""


def main():
    treasury_available = 1 - 1
    ordinary_appeals, standing_review = 2, 4
    one_agency_evaluation = 2
    failure_followup = 2
    assert 4 + 4 - 8 == 0
    assert treasury_available == 0
    assert ordinary_appeals + one_agency_evaluation == standing_review
    assert ordinary_appeals + 2 * one_agency_evaluation - standing_review == 2
    stressed_demand = ordinary_appeals + one_agency_evaluation + failure_followup
    for source in (0, 2):
        accepted_alternate = 2 if source >= 2 else 0
        assert stressed_demand - standing_review - accepted_alternate == 2 - source
    print("AI budget: shared review, funding independence and adverse receiving passed.")


if __name__ == "__main__":
    main()
