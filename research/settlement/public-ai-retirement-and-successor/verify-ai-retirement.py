"""Check the constructed support boundary and separate staffing roles."""


def may_rely(day, supported_through, contract_end, evaluated):
    return day <= min(supported_through, contract_end) and evaluated


def main():
    assert may_rely(10, 10, 30, True)
    assert not may_rely(11, 10, 30, True)
    assert not may_rely(11, 30, 30, False)
    assert may_rely(14, 30, 30, True)

    service_hours = 6 + 5
    ordinary_pool = 8
    independent_review = 2
    assert service_hours - ordinary_pool == 3
    assert ordinary_pool + 3 == service_hours
    assert service_hours - (ordinary_pool + 2) == 1
    assert independent_review == 2
    print("AI retirement: distinct deadlines, shared pool and qualified replacement passed.")


if __name__ == "__main__":
    main()
