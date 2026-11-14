"""Separate actual-type receipts, wage hours, ordinary protection and personal tax."""
import math


def work_calendar(c,fraction=1,days=5):
    if not 0<fraction<=1 or not 1<=days<=6:raise ValueError('Unsupported normal work pattern')
    weekly=c['normal_week']*fraction;daily=weekly/days
    if daily>10:raise ValueError('Declared normal day exceeds duty cap')
    scheduled=weekly*c['scheduled_weeks'];breaks=.5*days*c['scheduled_weeks'] if daily>6 else 0
    learning=c['learning_fulltime']*fraction;tasks=(scheduled-breaks-learning)*(1-c['unexpected_loss'])
    return dict(normal_weekly_paid_hours=weekly,normal_days=days,annual_normal_paid_hours=weekly*c['paid_weeks'],scheduled_hours=scheduled,paid_breaks=breaks,learning=learning,task_hours=tasks)


def labor_cases(c):
    floor=c['minimum_median_fraction']*c['median_ordinary_hourly_hypothesis'];out=[]
    for case in c['cases']:
        rows=[]
        for x in c['cohorts']:
            fraction=case['low_fraction'] if x['id']=='low' else 1;days=case['low_days'] if x['id']=='low' else 5
            cal=work_calendar(c,fraction,days);minimum=floor*cal['annual_normal_paid_hours']
            pay=max(x['annual_pay'],minimum) if case['uplift'] else x['annual_pay']
            rows.append(dict(id=x['id'],people=x['people'],annual_pay_CU=pay,normal_paid_FTE=fraction*x['people'],calendar=cal,hourly_cash_CU=pay/cal['annual_normal_paid_hours'],minimum_compliant=pay+1e-6>=minimum,employer_and_job_assignment=None,actual_consent=None))
        out.append(dict(id=case['id'],rows=rows,people=sum(x['people'] for x in rows),normal_paid_FTE=sum(x['normal_paid_FTE'] for x in rows),scenario_wages_CU=sum(x['people']*x['annual_pay_CU'] for x in rows),task_hour_upper_bound=sum(x['people']*x['calendar']['task_hours'] for x in rows),credited_actual_payroll_or_tax_source=None,complete_job_match=False))
    return out


def progressive(q,c):
    if q<0:raise ValueError('Negative ordinary tax base')
    if len(c['marginal_rates'])!=len(c['band_width_multiple_M']) or c['band_width_multiple_M'][-1] is not None:raise ValueError('Incomplete tax schedule')
    tax=0;left=q
    for rate,width in zip(c['marginal_rates'],c['band_width_multiple_M']):
        amount=left if width is None else min(left,width*c['annual_tax_scale_M'])
        tax+=rate*amount;left-=amount
        if left<=0:break
    return tax


def payment(person,c,kind='protected_foundation',attribution=None):
    if kind not in ['protected_foundation','extra_personal_allowance','retained_I05','equivalent_taxable_gross']:raise ValueError('Unsupported income architecture')
    allowed={'id','kind','wage','net_business','replacement','pension','capital','support_received','in_kind','housing','access_cost','recognized_work_cost','recognized_support_paid','lawful_asset_draw','foundation_receipt_fraction','scope','ordinary_component'}
    unknown=set(person)-allowed
    if unknown:raise ValueError('Unsupported person-resource semantics: '+','.join(sorted(unknown)))
    if not 0<=person.get('foundation_receipt_fraction',1)<=1:raise ValueError('Invalid ordinary receipt fraction')
    if any(person.get(k,0)<0 for k in ['wage','net_business','replacement','pension','capital','support_received','in_kind','housing','access_cost','recognized_work_cost','recognized_support_paid','lawful_asset_draw']):raise ValueError('Unsupported negative receipt/loss/refund semantics require a separate matched account')
    if person.get('kind','adult') not in ['adult','older','child']:raise ValueError('Unsupported person kind')
    B=c['ordinary_adult_basket_CU']*(c['child_factor'] if person.get('kind')=='child' else 1)
    C=min(person.get('in_kind',0),.8*B);housing=person.get('housing',c['default_housing_CU']);workcost=person.get('recognized_work_cost',0)
    due=max(0,B-C) if kind!='retained_I05' or person.get('kind')=='older' else 0
    U=due*person.get('foundation_receipt_fraction',1)
    wage=person.get('wage',0)+person.get('net_business',0);contribution=wage*c['contribution_rate'];L=wage-contribution+person.get('replacement',0)
    P=person.get('pension',0);K=person.get('capital',0);Q=L+P+K
    allowance=c['comparison_general_personal_allowance_CU'] if kind in ['extra_personal_allowance','retained_I05'] else 0
    tax=progressive(max(0,Q-allowance),c)
    attribution=attribution or c['selected_attribution']
    if attribution=='proportionate_nonfoundation':
        ta=[tax*x/Q if Q else 0 for x in [L,P,K]]
    elif attribution=='work_first':
        t=lambda q:progressive(max(0,q-allowance),c)
        ta=[t(L),t(L+P)-t(L),t(Q)-t(L+P)]
    else:raise ValueError('Unsupported tax attribution')
    E=L-ta[0];pnet=P-ta[1];knet=K-ta[2]
    disregard=min(c['pension_disregard_fraction']*pnet,c['pension_disregard_cap_fraction']*B)
    O=pnet-disregard+knet+person.get('support_received',0)
    N=B-C+housing+workcost+person.get('recognized_support_paid',0)
    A=person.get('lawful_asset_draw',0);d=c['earnings_disregard_fraction']*B
    residual=max(0,N-U-O-A-c['withdrawal']*max(0,E-d))
    access=person.get('access_cost',0)
    disposable=U+E+pnet+knet+person.get('support_received',0)+residual-workcost-person.get('recognized_support_paid',0)
    return dict(id=person['id'],architecture=kind,ordinary_basket=B,actual_in_kind=C,foundation_due=due,foundation_received=U,
                exclusive_foundation_tax_offset=(U if kind=='equivalent_taxable_gross' else 0),ordinary_other_tax_base=Q,
                earnings_allowance=allowance,personal_tax=tax,tax_attribution=dict(work=ta[0],pension=ta[1],capital=ta[2],foundation=0),
                employee_Y_contribution=contribution,net_work_E=E,net_pension=pnet,net_capital=knet,pension_disregard=disregard,counted_other_O=O,
                needs_N=N,residual_R=residual,access_compensation=access,disposable_cash_after_matched_work_support=disposable,
                usable_resources_including_actual_asset_draw=disposable+A,
                ordinary_component_source=('Ybasicmatchedonce' if person.get('kind')=='older' else 'ICordinarycash'),
                general_transfer_CU=U+residual+access,net_G_cash_use_before_other_sources_CU=U+residual+access-tax,
                received_ordinary_exclusion_once=True,actual_source_or_adequacy=None,
                transition_extra_protection_not_calculated=(person.get('foundation_receipt_fraction',1)<1),complete_migration_or_annual_tax_administration=False)


def pension_new_year(earnings,eligible_fraction,earnings_in_eligible,W):
    if not 0<=eligible_fraction<=1 or not 0<=earnings_in_eligible<=earnings:raise ValueError('Invalid matched Y period')
    if eligible_fraction==0 and earnings_in_eligible!=0:raise ValueError('No earnings in nonexistent eligible period')
    if eligible_fraction==1 and earnings_in_eligible!=earnings:raise ValueError('Full-year eligibility must match full-year earnings')
    addition=min(max(0,W-earnings),max(0,.5*W*eligible_fraction-earnings_in_eligible))
    base=min(W,earnings+addition)
    return dict(contribution=.1*earnings,eligible_fraction=eligible_fraction,matched_earnings=earnings_in_eligible,G_credit_transfer=.1*addition,new_base=base,new_annual_lifetime_unit=.0125*base,prior_units_unchanged=True,actual_eligibility=None)


def update_tax_scale(prior,verified_W=None,verified_CPI=None):
    if prior<=0 or verified_W is not None and verified_W<=0 or verified_CPI is not None and verified_CPI<=0:
        raise ValueError('Invalid tax-scale source; missing evidence is None, not zero')
    inflation=prior*max(1,verified_CPI) if verified_CPI is not None else prior
    return max(prior,inflation,verified_W if verified_W is not None else prior)
