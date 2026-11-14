"""Authored income incidence and investment cross-sections; no executed source.

The frozen87 cohort/tax/price functions are reused within their complete declared
input scope. macro.py contains an explicit, diffed derivative of solve, rather
than altering the frozen module or transferring its review to this proposal.
"""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('frozen87', ROOT/'2026-10-finance-and-delivery-bridge/model.py')
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)


def households(c, p, price, dividends, interestH):
    h = baseline.households(c, p, price, dividends, interestH)
    share = c.get('ordinary_base_share', 0)
    h['ordinary_base_nonolder'] = 0.0
    h['residual_nonolder'] = 0.0
    for person, row in zip(baseline.persons(c, price), h['rows']):
        n = row['weight']/1e6
        personal = c['household']['adult_personal_net_monthly']*12*price['personal_factor']
        if person['kind'] == 'child':
            personal *= c['household']['child_factor']
        meals = person['meal_days']*c['household']['child_meals']['ingredient_unit_net']*(1+price['food_rate'])
        credit = min(meals, .8*personal) if c.get('base_credit_received_meals', True) else 0
        U = share*(personal-credit) if person['kind'] != 'older' else 0
        old = row['topup_CU']
        residual = max(0, old-U) if person['kind'] != 'older' else old
        delta = U+residual-old
        consumption = c['household']['consumption_of_surplus_fraction']*delta
        saving = delta-consumption
        net = consumption/(1+p['discretionary_tax_rate'])
        for key, amount in [('topup', delta), ('general_transfers', delta),
                            ('cash_after_tax_and_transfers', delta),
                            ('H_consumption', consumption), ('H_saving', saving),
                            ('VAT', consumption-net), ('ordinary_pre_tax', net)]:
            h[key] += amount*n
        h['ordinary_base_nonolder'] += U*n
        if person['kind'] != 'older':
            h['residual_nonolder'] += residual*n
        row.update(ordinary_base_CU=U, residual_CU=residual,
                   old_same_receipts_I05_CU=old,
                   topup_CU=U+residual,
                   posttax_resources_after_support_CU=row['posttax_resources_after_support_CU']+delta,
                   voluntary_saving_CU=row['voluntary_saving_CU']+saving,
                   VAT_CU=row['VAT_CU']+consumption-net)
    h['legacy_topup_field_includes_nonolder_base_and_residual'] = True
    return h


def incidence(old, new):
    rows = []
    for a, b in zip(old['rows'], new['rows']):
        delta = b['posttax_resources_after_support_CU']-a['posttax_resources_after_support_CU']
        rows.append(dict(group=a['group'], kind=a['kind'], weight=a['weight'],
                         participant_annual_CU=a['participant_annual_CU'],
                         gross_wage_CU=a['gross_wage_CU'],
                         gross_pension_CU=a['gross_pension_CU'],
                         gross_dividend_before_CU=a['gross_dividend_CU'],
                         gross_dividend_after_CU=b['gross_dividend_CU'],
                         cash_change_CU=delta,
                         old_cash_CU=a['posttax_resources_after_support_CU'],
                         new_cash_CU=b['posttax_resources_after_support_CU']))
    return dict(gaining_people=sum(x['weight'] for x in rows if x['cash_change_CU']>1e-6),
                losing_people=sum(x['weight'] for x in rows if x['cash_change_CU']<-1e-6),
                cash_change_mCU=sum(x['weight']*x['cash_change_CU']/1e6 for x in rows), rows=rows)


def calculate():
    inp = json.loads((HERE/'inputs.json').read_text())
    for name, digest in inp['pinned_support'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    c = json.loads((ROOT/'2026-10-finance-and-delivery-bridge/inputs.json').read_text())
    # Import after defining the household adapter; no monkey-patching old functions.
    import macro
    p = c['policies'][1]
    base = macro.solve(c, p)
    fixed = []
    cases = []
    for share in inp['base_share_cases']:
        q = copy.deepcopy(c); q['ordinary_base_share'] = share
        h = households(q, p, base['prices'], base['F_dividend']+base['E_dividend'], 20.9)
        fixed.append(dict(share=share,
                          extra_transfers_mCU=h['general_transfers']-base['household']['general_transfers'],
                          income_incidence=incidence(base['household'], h)))
        for policy in q['policies']:
            a = macro.solve(q, policy)
            reference = macro.solve(c, policy)
            a['share'] = share
            a['incidence_against_same_tax_I05'] = incidence(reference['household'], a['household'])
            cases.append(a)
    # This is an optimistic cash ceiling, not a target-company valuation or bid.
    mu = inp['mutual']; price = mu['optimistic_book_price_mCU']
    service = price*(mu['seller_loan_rate']+1/mu['equal_principal_years'])
    mutual = dict(available_F_dividend_mCU=base['F_dividend'],
                  first_year_service_mCU=service,
                  optimistic_shortfall_mCU=service-base['F_dividend'],
                  zero_extra_cost_price_ceiling_mCU=base['F_dividend']/(mu['seller_loan_rate']+1/mu['equal_principal_years']),
                  actual_price_and_target_receipts=None)
    pr = inp['project']; capital = pr['capital_mCU']; cfc = capital/pr['life_years']
    GWh = pr['nameplate_MW']*pr['equivalent_hours']/1000
    energy = GWh*pr['displaced_energy_price_CU_kWh']
    phases = [dict(id='earmark', reserve_after_prior_offer=capital),
              dict(id='build', build=capital, build_import_share=pr['import_share']),
              dict(id='accepted_output', opening_stock=capital, CFC=cfc, reserve=cfc,
                   displaced_imports=energy, operating_imports=pr['imported_operating_inputs_mCU']),
              dict(id='zero_output_after_commission', opening_stock=capital, CFC=cfc, reserve=cfc,
                   displaced_imports=0, operating_imports=pr['imported_operating_inputs_mCU']),
              dict(id='commissioning_delayed', opening_stock=capital, CFC=0,
                   displaced_imports=0, operating_imports=pr['imported_operating_inputs_mCU'])]
    investments = []
    for phase in phases:
        q = copy.deepcopy(c); q['investment'] = phase
        a = macro.solve(q, p); investments.append(a)
    bank = base['capital_positions']['legacy_bank_reference']['retention_ringfence']
    remaining = base['planned_sector_cash_before_financing']['F']-bank-base['finance']['new_bond_offers']['F']
    fullcash = copy.deepcopy(c)
    fullcash.update(ordinary_base_share=1, base_credit_received_meals=False)
    fullcash_h = households(fullcash, p, base['prices'], base['F_dividend']+base['E_dividend'], 20.9)
    combined = []
    for phase in [phases[1], phases[2]]:
        q = copy.deepcopy(c); q.update(ordinary_base_share=1, investment=phase)
        combined.append(macro.solve(q, p))
    return dict(edition=88, qualification=inp['status'], fixed_receipts_incidence=fixed,
                income_cases=cases, mutual=mutual, investment_cases=investments,
                full_cash_with_food_additional_counterfactual=dict(
                    extra_transfers_mCU=fullcash_h['general_transfers']-base['household']['general_transfers'],
                    incidence=incidence(base['household'], fullcash_h)),
                combined_full_base_and_project_cross_sections=combined,
                project=dict(annual_GWh_if_accepted=GWh, displaced_imports_mCU=energy,
                             conditional_retention_after_bank_and_prior_bond_offer=remaining,
                             capital_earmark_mCU=capital,
                             dedicated_capital_cash_rollforward=[
                                 dict(phase='earmark', opening=0, reserve_from_realized_retention=capital, build=0, closing=capital),
                                 dict(phase='build', opening=capital, reserve_from_realized_retention=0, build=capital, closing=0)],
                             conditional_not_executed=True,
                             capital_imports=capital*pr['import_share'],
                             domestic_own_account_build=capital*(1-pr['import_share']),
                             no_cash_creation_from_reservation=True,
                             cross_sections_not_a_sequential_funded_path=True,
                             firm_capacity_credit_MW=0,
                             actual_qualified_staff_grid_roofs_and_funding=None),
                actual=inp['actual'])


if __name__ == '__main__':
    (HERE/'results.json').write_text(json.dumps(calculate(), indent=2)+'\n')
    print('Wrote conditional income incidence, twelve income closures, five investment phases and acquisition bound.')
