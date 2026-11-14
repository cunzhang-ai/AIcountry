"""Recurring-source bounds, dated debt stress and pension component safeguards.

Frozen88 computation runs in its own process/module namespace, read-only. No
predecessor validator runs, function patching or mutation of dated editions.
Debt stress holds the non-interest cash requirement fixed; it is deliberately
not an endogenous national income, holder-incidence or demographic projection.
"""
from pathlib import Path
import copy
import hashlib
import json
import os
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def run_frozen_jobs(jobs):
    code='''import json,sys,macro
jobs=json.load(sys.stdin)
json.dump([dict(id=j['id'],result=macro.solve(j['inputs'],j['policy'])) for j in jobs],sys.stdout)
'''
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    result=subprocess.run([sys.executable,'-c',code],cwd=ROOT/'2026-11-income-and-investment-settlement',
                          input=json.dumps(jobs),text=True,capture_output=True,check=True,env=env)
    return json.loads(result.stdout)


def cash_classification(a,c):
    tx=a['transactions']
    uses=sum(t['amount_mCU'] for t in tx if t['payer']=='G')
    receipts=sum(t['amount_mCU'] for t in tx if t['receiver']=='G')
    interest=sum(t['amount_mCU'] for t in tx if t['purpose']=='opening public debt coupon')
    internal=sum(t['amount_mCU'] for t in tx if t['payer']=='G' and t['receiver']=='S' and t['purpose']=='opening public debt coupon')
    equity=c['public']['G_equity_subscription_to_E']
    capital=a['actual_capital_plan']['G'];inventory=a['actual_capital_plan']['G_inventory']
    renewal=c['public']['G_renewal_fraction']*a['public_terms']['DG']
    growth=c['public']['new_retrofit_G']
    cashgap=uses-receipts
    bank=a['capital_positions']['legacy_bank_reference']['retention_ringfence']
    nonbank=a['planned_sector_cash_before_financing']['F']-bank
    return dict(G_gross_cash_uses=uses,G_gross_cash_receipts=receipts,G_cash_deficit=cashgap,
                G_interest_cash=interest,G_noninterest_cash_requirement=cashgap-interest,
                G_nonfinancial_primary_cash_gap=cashgap-interest-equity,
                G_current_nonfinancial_primary_cash_gap=cashgap-interest-equity-capital,
                G_actual_own_capital_and_inventory=capital,G_own_replacement=renewal,
                G_own_growth=growth,G_initial_inventory=inventory,G_E_equity_subscription=equity,
                G_recurring_full_cost_primary_gap=cashgap-interest-equity-growth-inventory,
                GS_internal_coupon=internal,
                GS_recurring_full_cost_primary_gap=cashgap-a['planned_sector_cash_before_financing']['S']-(interest-internal)-equity-growth-inventory,
                F_current_retention= a['planned_sector_cash_before_financing']['F'],
                legacy_bank_retention=bank,nonbank_current_retention=nonbank,
                nonbank_operating_profit_before_legacy_bank_coupon=a['F_operating_profit'],
                within_positive_nonbank_and_separate_bank_scope=(nonbank>=0 and a['F_operating_profit']>=0),
                nonbank_annual_cash_break_even_GVA=a['F_wages']+a['F_CFC']+a['prices']['land_tax'],
                one_period_offers_cover_request=a['finance']['unmatched_requirement']<1e-8,
                conditional_closing_positions_nonnegative=a['finance']['valid_closing_cash_assets'] is not None,
                recurring_country_funding_proved=False)


def debt_stress(a,c,inp):
    d=sum(c['public']['G_debt_initial_by_holder'].values())
    rate=inp['coupon_rate'];primary=cash_classification(a,c)['G_noninterest_cash_requirement']
    offer=sum(a['finance']['new_bond_offers'].values())
    rows=[]
    for year in range(1,inp['years']+1):
        interest=rate*d
        due=d*c['finance']['maturing_principal_fraction']
        rolled=due*c['finance']['refinance_offer_fraction']
        draw=inp['cash_draw_first_year'] if year==1 else 0
        requested_new=max(0,primary+interest+due-rolled-draw)
        requested_closing=d-due+rolled+requested_new
        rows.append(dict(year=year,opening_debt=d,noninterest_cash_requirement=primary,
                         coupon=interest,due_principal=due,conditional_rollover=rolled,
                         cash_draw=draw,new_borrowing_request=requested_new,
                         frozen_new_offer_cap=offer,unmatched_request=max(0,requested_new-offer),
                         contractual_debt_if_all_requests_received=requested_closing,
                         actual_executed_debt=None))
        d=requested_closing
    return dict(rows=rows,first_unmatched_year=next((x['year'] for x in rows if x['unmatched_request']>1e-8),None),
                qualification='Conditional contractual stress only; after first failure the debt series is an unexecuted request, not a funded path. No fixed macro tax/price or lender-incidence forecast.',
                executed_path=None)


def pension_liquidity(a,c):
    dues=a['household']['pensions']+c['public']['S_admin_service_payment_to_G']
    opening=c['finance']['opening_settlement_claim_on_R']['S']
    nextdue=dues/12;postreserve=4*dues/12
    seed=max(0,nextdue+postreserve-opening)
    # A separate intra-year illustration, not proof of actual source dates:
    # regular monthly receipts come only after that month's due payment.
    cash=opening+seed;calendar=[]
    for month in range(1,13):
        before=cash;cash-=nextdue;after=cash;cash+=dues/12
        calendar.append(dict(month=month,before_due=before,due=nextdue,
                             after_due=after,receipts_after_due=dues/12,closing_cash=cash))
    return dict(annual_earned_survivor_admin=dues,next_month_due=nextdue,
                required_post_due_cash_reserve=postreserve,opening_S_cash=opening,
                seed_before_next_due_if_no_other_receipts=seed,
                annual_current_G_backing=a['S_current_backing'],
                G_bond_in_S=c['public']['G_debt_initial_by_holder']['S'],G_coupon_to_S=c['public']['G_debt_initial_by_holder']['S']*c['public']['G_coupon_rate'],
                consolidated_extra_source_from_coupon=0,
                G_credit_payment=c['public']['S_credit_transfer'],
                extra_credited_base_needed_to_explain_old_credit_transfer=c['public']['S_credit_transfer']/.1,
                actual_credited_people_and_original_bases=None,
                monthly_conditional_calendar=calendar,
                actual_seed_source=None)


def best_units(units):
    return sum(sorted(units,reverse=True)[:48])


def accrual_examples(inp):
    # W and careers are authored examples; no current pension is recomputed.
    W=30000;accrual=inp['annual_accrual'];rows=[]
    for name,old_bases,new_base in [('median_worker',[W]*30,W),
                                   ('higher_worker',[2*W]*30,2*W),
                                   ('care_credit',[.5*W]*30,.5*W),
                                   ('already_48_high_years',[2*W]*48,2*W)]:
        prior=[accrual*x for x in old_bases]
        retained=prior[:];revised=prior[:]
        for year in range(1,21):
            retained.append(accrual*min(new_base,2*W))
            revised.append(accrual*min(new_base,W))
            rows.append(dict(example=name,new_year=year,prior_accrued_annual_pension=best_units(prior),
                             retained_2W_annual_pension=best_units(retained),
                             selected_1W_annual_pension=best_units(revised),
                             contribution_each_year=.1*new_base,
                             credit_transfer_if_wholly_credited=.1*new_base if name=='care_credit' else 0,
                             actual_career_or_fairness_proof=None))
    return rows


def calculate():
    inp=json.loads((HERE/'inputs.json').read_text())
    for name,digest in inp['pinned_support'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    c=json.loads((ROOT/'2026-10-finance-and-delivery-bridge/inputs.json').read_text());jobs=[]
    for case in inp['tax_cases']:
        q=copy.deepcopy(c);q['ordinary_base_share']=case['share'];p=copy.deepcopy(q['policies'][1])
        if 'personal_rates' in case:p['personal_rates']=case['personal_rates']
        if 'supplier_margin' in case:q['production']['supplier_profit_margin_on_cost']=case['supplier_margin']
        jobs.append(dict(id=case['id'],inputs=q,policy=p))
    cases=run_frozen_jobs(jobs)
    for case,job in zip(cases,jobs):case['classification']=cash_classification(case['result'],job['inputs'])
    byid={x['id']:x for x in cases};cashpass=byid['universal_82_all_bands']['result']
    pension=pension_liquidity(byid['universal_current']['result'],c)
    need=cashpass['finance']['funding_requirement'];offers=sum(cashpass['finance']['new_bond_offers'].values())
    seeded=dict(old_G_new_source_request=need,old_new_offers=offers,
                minimum_seed_before_first_due=pension['seed_before_next_due_if_no_other_receipts'],
                G_cash_use=pension['seed_before_next_due_if_no_other_receipts'],
                S_restricted_cash_claim_increase=pension['seed_before_next_due_if_no_other_receipts'],
                additional_GDP_or_annual_benefit=0,
                extra_consolidated_recurring_cost_from_internal_seed=0,
                revised_G_source_request_lower_bound=need+pension['seed_before_next_due_if_no_other_receipts'],
                unmatched_lower_bound=need+pension['seed_before_next_due_if_no_other_receipts']-offers,
                early_loan_coupon_fees_and_timing_actual=None,
                actual_received_source=None)
    return dict(edition=89,status=inp['status'],cases=cases,
                debt_stress=debt_stress(cashpass,c,inp['debt_stress']),
                pension_liquidity=pension,
                cash_pass_with_required_pension_liquidity_lower_bound=seeded,
                accrual_examples=accrual_examples(inp['pension_choices']),
                actual=inp['actual'])


if __name__=='__main__':
    (HERE/'results.json').write_text(json.dumps(calculate(),indent=2)+'\n')
    print('Wrote scoped recurring-source/offer counterexamples, contractual debt stress and protected accrual examples.')
