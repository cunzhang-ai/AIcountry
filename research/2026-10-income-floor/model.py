"""Declared income, pooling and launch-ledger reference; not national estimates."""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def tax_and_net(gross,policy):
    gross=F(str(gross)); contribution=gross*F(str(policy['contribution_rate']))
    base=max(F(0),gross-contribution);tax=F(0)
    for lower,upper,rate in policy['tax_bands']:
        amount=max(F(0),base-F(lower))
        if upper is not None:amount=min(amount,F(upper)-F(lower))
        tax+=amount*F(str(rate))
    return tax,contribution,gross-contribution-tax


def payment(person,policy,package='individual'):
    monthly=F(str(policy['adult_basket']))*(F(str(policy['child_factor'])) if person['kind']=='child' else 1)
    housing=F(str(person.get('housing',policy['housing_share'])))
    work_cost=F(str(person.get('work_cost',0)))
    support=F(str(person.get('support_paid',0)))
    recognized=min(support,F(str(person.get('recipient_need',monthly+housing))))
    tax,contribution,earnings=tax_and_net(person.get('gross',0),policy)
    basic=monthly if person['kind']=='older' or package=='universal' else F(0)
    insurance=F(str(person.get('insurance',0)))
    insurance_credit=insurance-min(insurance*F(str(policy['pension_disregard'])),monthly*F(str(policy['pension_disregard_cap'])))
    received=F(str(person.get('support_received',0)))
    in_kind=min(F(str(person.get('in_kind_personal',0))),monthly-F(str(policy['cash_share']))*monthly)
    needs=monthly+housing+work_cost+recognized-in_kind
    assets=F(str(person.get('liquid_assets',0))) if person.get('assets_usable',True) else F(0)
    draw=max(F(0),assets-F(policy['asset_buffer_months'])*(monthly+housing))/F(policy['asset_draw_months'])
    taper=F(str(policy['withdrawal_rate']))*max(F(0),earnings-monthly*F(str(policy['earnings_disregard'])))
    topup=max(F(0),needs-basic-received-insurance_credit-draw-taper)
    disability=F(str(person.get('disability_cost',0)))
    # Matching disability support compensates its own cost, not ordinary resources.
    disposable=earnings+basic+insurance+received+topup-support-work_cost+disability-disability
    return {'tax':tax,'contribution':contribution,'net_earnings':earnings,
      'basic':basic,'topup':topup,'disability_support':disability,'asset_draw':draw,
      'disposable_after_work_support_cost':disposable,'ordinary_needs':monthly+housing,
      'general_transfer':basic+topup+disability,'received_support':received,'paid_support':support}


def pooled(members,policy):
    rows=[payment(p,policy) for p in members]
    # Private transfers internal to this declared household cancel; no hypothetical support is added.
    needs=sum(r['ordinary_needs']+F(str(p.get('work_cost',0))) for p,r in zip(members,rows))
    basic=sum(r['basic'] for r in rows)
    earnings=sum(r['net_earnings'] for r in rows)
    d=sum(F(str(policy['adult_basket']))*F(str(policy['earnings_disregard'])) for p in members if p['kind']!='child' and p.get('gross',0)>0)
    topup=max(F(0),needs-basic-sum(F(str(p.get('insurance',0))) for p in members)-F(str(policy['withdrawal_rate']))*max(F(0),earnings-d))
    return basic+topup+sum(r['disability_support'] for r in rows)


def population_result(data,policy,package,insurance_branch=False):
    transfers=F(0);tax=F(0);contributions=F(0);count=0;support_paid=F(0);support_received=F(0)
    for group in data['population_groups']:
        members=[dict(p) for p in group['members']]
        children=[p for p in members if p['kind']=='child']
        for p in members:
            if p.get('support_paid',0):
                assert len(children)==1
                p['recipient_need']=F(str(policy['adult_basket']))*F(str(policy['child_factor']))+F(str(children[0].get('housing',policy['housing_share'])))
        if insurance_branch:
            for p in members:
                if p['kind']=='older':p['insurance']=data['legacy_insurance_monthly']
        rows=[payment(p,policy,package) for p in members]
        if package=='pooled':transfers+=group['count']*pooled(members,policy)
        else:transfers+=group['count']*sum(r['general_transfer'] for r in rows)
        tax+=group['count']*sum(r['tax'] for r in rows)
        contributions+=group['count']*sum(r['contribution'] for r in rows)
        support_paid+=group['count']*sum(r['paid_support'] for r in rows)
        support_received+=group['count']*sum(r['received_support'] for r in rows)
        count+=group['count']*len(members)
    assert support_paid==support_received
    return {'people':count,'annual_general_transfers':transfers*12/F(10**6),
      'annual_modeled_personal_tax':tax*12/F(10**6),
      'annual_restricted_contributions':contributions*12/F(10**6),
      'annual_private_support_flow':support_paid*12/F(10**6)}


def launch(result,data,unclassified=0,shock=False):
    base=data['launch'];receipts=result['annual_modeled_personal_tax']+F(str(base['other_assumed_receipts']))
    if shock:receipts*=F('0.9')
    outlays=F(str(base['services']))+result['annual_general_transfers']+F(unclassified)+F(str(base['capital']))+F(str(base['interest']))+(20 if shock else 0)
    room=F(str(base['new_borrowing']))+F(str(base['opening_cash']))-F(str(base['cash_buffer']))
    return {'receipts':receipts,'outlays_excluding_refinanced_principal':outlays,
      'allowed_borrowing_and_cash_draw':room,'unfunded_cash':max(F(0),outlays-receipts-room),
      'unknown_extra_cost':None,'status':'One-year partial reference. Actual law, all tax bases, prices, demand and full delivery unverified; restricted contributions not general funds.'}


def clean(value):
    if isinstance(value,F):return float(value)
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,list):return [clean(v) for v in value]
    return value


def calculate():
    data=json.loads((HERE/'inputs.json').read_text())
    for source,expected in data['pinned_sources'].items():
        if hashlib.sha256((ROOT/source).read_bytes()).hexdigest()!=expected:raise ValueError(source)
    scenarios=[]
    for label,changes in data['calibrations'].items():
        policy={**data['policy'],**changes}
        for package in ['pooled','individual','universal']:
            r=population_result(data,policy,package)
            scenarios.append({'calibration':label,'package':package,**r,
              'launch':launch(r,data),'unclassified_40_launch':launch(r,data,40),
              'compound_launch':launch(r,data,shock=True),'feasibility':'Not established'})
    p=data['policy'];branch=population_result(data,p,'individual',True)
    cases=[{'case':c['label'],'individual':payment(c['person'],p),'universal':payment(c['person'],p,'universal')} for c in data['cases']]
    wage_steps=[]
    for cost in [0,600,8000]:
        for gross in range(0,12001):
            a=payment({'kind':'adult','gross':gross,'work_cost':cost},p);b=payment({'kind':'adult','gross':gross+1,'work_cost':cost},p)
            wage_steps.append(b['disposable_after_work_support_cost']-a['disposable_after_work_support_cost'])
    # Another program imposes a 600 fee at 2000; ordinary need has not yet been updated.
    before=payment({'kind':'adult','gross':1999,'work_cost':0},p)
    after=payment({'kind':'adult','gross':2000,'work_cost':0},p)
    corrected=payment({'kind':'adult','gross':2000,'work_cost':600},p)
    cliff_change=after['disposable_after_work_support_cost']-before['disposable_after_work_support_cost']-600
    corrected_change=corrected['disposable_after_work_support_cost']-before['disposable_after_work_support_cost']
    return clean({'status':data['status'],'scenarios':scenarios,'cases':cases,
      'minimum_gain_per_one_gross_cu_fixed_needs':min(wage_steps),
      'external_fee_cliff_change':cliff_change,'expense_recognized_change':corrected_change,
      'insurance_branch':{'population':branch,'launch':launch(branch,data),
        'separately_owed_legacy_insurance':45,'unknown_remaining_insurance_liability':None},
      'actual_national_cost':None,'observed_wellbeing':None,
      'qualification':'Authored scope/price/cohort comparisons and conservation only. No adequate basket, optimal rate, actual resources, behavioral forecast, lawful launch or superior lives established.'})


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
