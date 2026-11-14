"""Authored cohort computation. No actual valuation, source or payment authority.
Money is CU in the frozen87 selective operating-price baseline. Expected fractional
people are projection weights, never grounds to stop an actual person's payment.
Annual death exposure is half-cycle; this is not a validated payment calendar.
"""
from copy import deepcopy
import json, math
from pathlib import Path

HERE=Path(__file__).resolve().parent
CFG=json.loads((HERE/'cohort-inputs.json').read_text())
OPENING_INDEX=CFG['opening_general_index']
W=CFG['W_authored']
PART_PAY=CFG['participant_annual_gross']
MORTALITY=[(p['upper_age_exclusive'] if p['upper_age_exclusive'] is not None else math.inf,p['q']) for p in CFG['mortality']]
CLASSES=CFG['initial_active']['classes']
LEVY=CFG['worker_levy'];ACCRUAL=CFG['annual_accrual'];BEST=CFG['best_calendar_bases']
CREDIT_RATE=CFG['credit_transfer_rate'];CREDIT_TARGET=CFG['credit_target_multiple_W']
OLD_CAP=CFG['initial_active']['prior_cap_multiple']

def qdeath(age, longevity=False):
    q=next(q for top,q in MORTALITY if age<top)
    return q*(CFG['longevity_case_q65plus_multiplier'] if longevity and age>=65 else 1)

def earned(bases): return ACCRUAL*sum(sorted(bases,reverse=True)[:BEST])

def entry(age,n,tag,pay,credit,part,with_prior=True):
    prior=[]
    for _ in range(max(0,int(age)-18) if with_prior else 0):
        work=pay+(PART_PAY if part else 0)
        base=min(work,OLD_CAP*W)
        if credit: base+=max(0,min(CREDIT_TARGET*W,OLD_CAP*W)-base)
        prior.append(base*OPENING_INDEX)
    return dict(age=float(age),n=n,tag=tag,pay=pay,credit=credit,part=part,
                bases=prior,pension=0.0)

def split_entrants(age,n,with_prior=False):
    rows=[]
    for name,pay,count,credit in CLASSES:
        for frac,part in [(1-CFG['participant_share'],False),(CFG['participant_share'],True)]:
            rows.append(entry(age,n*count/sum(c[2] for c in CLASSES)*frac,name,pay,credit,part,with_prior))
    return rows

def initial():
    people=[]
    for age in range(18):
        n=CFG['initial_children_bands']['0_5_per_age'] if age<6 else CFG['initial_children_bands']['6_12_total']/7 if age<13 else CFG['initial_children_bands']['13_17_total']/5
        people.append(dict(age=float(age),n=n,tag='child',pay=0,credit=False,
                           part=False,bases=[],pension=0.0))
    for age in range(18,65): people+=split_entrants(age,CFG['initial_active']['age18_64_per_age'],with_prior=True)
    # Opening retirees have an authored prior-Y claim, not actual inherited rights.
    # Actual other-source/inherited/foreign claims remain unknown and unmapped.
    for age in range(65,95):
        for f,part in [(1-CFG['participant_share'],False),(CFG['participant_share'],True)]:
            people.append(dict(age=float(age),n=CFG['initial_Y_retirees']['ages65_through94_per_age']*f,tag='authored_Y_retired',pay=0,
                credit=False,part=part,bases=[CFG['initial_Y_retirees']['base_each_before_index']*OPENING_INDEX]*CFG['initial_Y_retirees']['authored_bases'],
                pension=CFG['initial_Y_retirees']['annual_claim_before_opening_index']*OPENING_INDEX))
    # These500 existing recipients are already within the15000 population.
    # Ongoing functional-dependant claims, not12-month bridge claims.
    pots=[dict(id='authored_Y_survivors500',n=CFG['survivors']['opening_Y_pots'],age=CFG['survivors']['opening_recipient_age'],annual=CFG['survivors']['opening_annual_before_index']*OPENING_INDEX,left=math.inf)]
    return people,pots

def allocate_one_pot(earned_annual, losses):
    total=sum(losses);pot=min(CFG['survivors']['pot_fraction']*earned_annual,total)
    return [0. if total==0 else pot*loss/total for loss in losses]

def new_pots(deaths,age,annual,year,source):
    """Mutually exclusive authored claim patterns: one pot/source-death, not three.
    Recipient records do not add people to the demographic population. These are
    dependency assumptions, not marriage tests or legal limits on mixed families.
    """
    specs=[]
    for p in CFG['survivors']['new_death_mutually_exclusive_patterns']:
        if p.get('qualifying_lost_support')==0:continue
        if 'years_to18' in p and (not isinstance(p['recipient_age'],(int,float)) or not 0<=p['recipient_age']<18 or abs(p['recipient_age']+p['years_to18']-18)>1e-9):
            raise ValueError('Child claim age/duration must end at18; retain alternative semantics for review')
        if isinstance(p['recipient_age'],str) and p['recipient_age']!='max18,sourceage-3':
            raise ValueError('Unsupported recipient-age semantics; retain and review input')
        if 'duration' in p and p['duration']!='eligible continuing life':
            raise ValueError('Unsupported survivor-duration semantics; retain and review input')
        age_value=p['recipient_age'] if isinstance(p['recipient_age'],(int,float)) else max(18.,age-3)
        duration=p.get('duration_years',p.get('years_to18',math.inf))
        specs.append((p['probability'],age_value,duration,p['actual_lost_support_cap'],'child' if 'years_to18' in p else 'functional' if 'duration' in p else 'bridge'))
    return [dict(id=f'{year}:{source}:{kind}',n=deaths*prob,age=a,
                 annual=min(CFG['survivors']['pot_fraction']*annual,loss),left=left)
            for prob,a,left,loss,kind in specs if annual>0 and deaths>0]

def merge_pots(pots):
    # Exact equal age/amount/duration states can be combined without changing cash.
    # Source-death disjointness is checked on creation; aggregation is not a new pot.
    groups={}
    for p in pots:
        key=(p['age'],p['annual'],p['left'])
        if key in groups: groups[key]['n']+=p['n']
        else: groups[key]=dict(p,id='aggregated_exact_claim_state')
    return list(groups.values())

def pay_pots(pots,longevity,portion=1.):
    paid=0.;remaining=[]
    for p in pots:
        duration=min(portion,p['left']);q=qdeath(p['age'],longevity)
        paid+=p['n']*p['annual']*duration*(1-.5*q*duration)
        z=dict(p);z['n']*=1-q*duration;z['age']+=duration;z['left']-=duration
        if z['left']>1e-12 and z['n']>0:remaining.append(z)
    return paid,remaining

def step(people,pots,year,cap=2,longevity=False,wage_factor=1.,inflation=1.,
         accrue=True,births=CFG['births_at_yearend']):
    start=sum(x['n'] for x in people);deaths=0.;payroll=contrib=credits=own=0.
    new_annual_accrual=0.;nextpeople=[];created=[]
    for i,r0 in enumerate(people):
        expanded=split_entrants(r0['age'],r0['n']) if r0['tag']=='child' and r0['age']>=18 else [r0]
        for r1 in expanded:
            r=dict(r1);r['bases']=list(r1['bases']);n=r['n'];age=r['age'];q=qdeath(age,longevity);exposure=n*(1-q/2)
            # Y03: price-revalue past bases and accrued/in-payment claims; no deflation cut.
            r['bases']=[b*max(1.,inflation) for b in r['bases']]
            r['pension']*=max(1.,inflation)
            if age>=65: r['pension']=max(r['pension'],earned(r['bases']))
            own+=exposure*r['pension'] if age>=65 else 0
            old_accrued=earned(r['bases'])
            if accrue and age>=18:
                work=(r['pay']*wage_factor if age<65 else 0)+(PART_PAY*wage_factor if r['part'] else 0)
                currentW=W*wage_factor
                workbase=min(work,cap*currentW)
                addition=max(0,min(CREDIT_TARGET*currentW,cap*currentW)-workbase) if r['credit'] and age<65 else 0
                payroll+=exposure*work;contrib+=exposure*LEVY*work;credits+=exposure*CREDIT_RATE*addition
                # Survivors of the year have a full service year. Deaths get half-year
                # newly earned basis for the death-pot computation, not a full new year.
                # Top48 is a sufficient numerical state under uniform Y03 revaluation.
                # Full dated legal service records must be retained elsewhere; no deletion authority.
                endbases=sorted(r['bases']+[workbase+addition],reverse=True)[:BEST]
                new_annual_accrual+=exposure*max(0,earned(endbases)-old_accrued)
                death_earned=r['pension'] if age>=65 else earned(r['bases']+[.5*(workbase+addition)])
                r['bases']=endbases
            else: death_earned=max(r['pension'],old_accrued)
            d=n*q;deaths+=d
            created+=new_pots(d,age,death_earned,year,f'{i}:{r["tag"]}:{r["part"]}')
            r['n']=n-d;r['age']+=1
            nextpeople.append(r)
    for p in pots: p['annual']*=max(1.,inflation)
    survivor,existing=pay_pots(pots,longevity)
    newpaid,newremaining=pay_pots(created,longevity,.5) # midyear starts;12-monthbridge=twohalves
    survivor+=newpaid
    if births>0: nextpeople.append(dict(age=0.,n=births,tag='child',pay=0,credit=False,part=False,bases=[],pension=0.))
    end=sum(x['n'] for x in nextpeople)
    assert abs(end-(start-deaths+births))<1e-6
    row=dict(year=year,start_people=start,deaths=deaths,births=births,end_people=end,
             people65plus=sum(x['n'] for x in people if x['age']>=65),payroll=payroll,
             contributions=contrib,credit_transfer=credits,own_pension=own,
             survivor_pension=survivor,benefits=own+survivor,new_annual_accrual=new_annual_accrual,
             survivor_pots=sum(x['n'] for x in existing+newremaining))
    return nextpeople,merge_pots(existing+newremaining),row

def tail_bounds(longevity=False):
    """Validate the bound against every supported future-dependant age/duration.
    A young lifelong dependant is meaningful, but cannot reuse the old ten-year
    multiplier. Keep the input and require a valid age-specific bound.
    """
    qfloor=min(q for top,q in MORTALITY if top>95)*(CFG['longevity_case_q65plus_multiplier'] if longevity else 1)
    if not 0<qfloor<=1:raise ValueError('No finite supported remaining-tail mortality bound')
    patterns=CFG['survivors']['new_death_mutually_exclusive_patterns']
    if abs(sum(p['probability'] for p in patterns)-1)>1e-9 or any(not 0<=p['probability']<=1 for p in patterns):
        raise ValueError('Mutually exclusive source-death patterns must cover one probability unit')
    spans=[]
    for p in patterns:
        if p.get('qualifying_lost_support')==0:continue
        if 'years_to18' in p:
            age=p['recipient_age']
            if not isinstance(age,(int,float)) or not 0<=age<18 or abs(age+p['years_to18']-18)>1e-9:
                raise ValueError('Child age/duration does not match the stated age18 boundary')
            spans.append(p['years_to18'])
        elif 'duration_years' in p:spans.append(p['duration_years'])
        elif p.get('duration')=='eligible continuing life':
            age=p['recipient_age']
            if isinstance(age,(int,float)):spans.append(max(0,95-age)+1/qfloor)
            elif age=='max18,sourceage-3':spans.append(3+1/qfloor)
            else:raise ValueError('Unsupported age meaning for lifelong tail; retain input for review')
        else:raise ValueError('Unsupported duration meaning for tail; retain input for review')
    need=max(spans,default=0)
    if CFG['tail_remaining_survivor_multiplier']<need:
        raise ValueError('Survivor tail multiplier does not bound the supplied age/duration')
    if CFG['tail_remaining_own_multiplier']<1/qfloor+CFG['survivors']['pot_fraction']*need:
        raise ValueError('Own/future-survivor tail multiplier does not bound supplied inputs')
    return need


def closed_tail(people,pots,first_year,longevity=False):
    """Run off rights accrued by the horizon only. No future contributions, entrants,
    or service accrual. This is NOT a law closing PAYG or an asset-funding target.
    """
    tail_bounds(longevity)
    qfloor=min(q for top,q in MORTALITY if top>95)*(CFG['longevity_case_q65plus_multiplier'] if longevity else 1)
    people=deepcopy(people);pots=deepcopy(pots);paid=0.;n=0
    for j in range(CFG['tail_maximum_years']):
        people,pots,r=step(people,pots,first_year+j,longevity=longevity,accrue=False,births=0)
        paid+=r['benefits'];n+=1
        relevant=[x for x in people if earned(x['bases'])>0 or x['pension']>0]
        # Once all source claims are95+,q>=.16 in longevitystress:own remaining<=6.25y;
        # a newly arising functional dependent may be92+,then<=3+6.25y. Childpot<=6y.
        # Bound conservatively with10y for all dependent claims and half-ownpot.
        if relevant and min(x['age'] for x in relevant)>=95:
            own=sum(x['n']*max(x['pension'],earned(x['bases'])) for x in relevant)
            survivors=sum(x['n']*x['annual'] for x in pots)
            existing_span=max([min(p['left'],max(0,95-p['age'])+1/qfloor) for p in pots],default=0)
            survivor_factor=max(CFG['tail_remaining_survivor_multiplier'],existing_span)
            bound=CFG['tail_remaining_own_multiplier']*own+survivor_factor*survivors
            if bound<CFG['conditional_tail_remaining_bound_target_CU']:return dict(closed_accrued_tail_CU=paid,tail_years=n,residual_bound_CU=bound,
                                  actual_tail_basis=None,not_full_funding_requirement=True)
    return dict(closed_accrued_tail_CU=paid,tail_years=n,residual_bound_CU=None,
                not_full_funding_requirement=True,unqualified_unbounded_tail=True)

def project(cap=2,longevity=False,wage_shock=False):
    tail_bounds(longevity)
    people,pots=initial();rows=[]
    for t in range(CFG['core_projection_years']):
        wf=CFG['wage_cut_case']['gross_and_currentW_multiplier'] if wage_shock and t in CFG['wage_cut_case']['years'] else 1.
        effective_cap=OLD_CAP if t<CFG['notice_first_full_years'] else cap # Jan1year0 enactment;24month notice;year2firstchangedservice
        people,pots,r=step(people,pots,t,cap=effective_cap,longevity=longevity,wage_factor=wf)
        r['new_service_cap_multiple']=effective_cap
        # S coupon is an actual receipt with a paired G coupon expense; not net national funding.
        factor=1-CFG['source']['annual_maturity_fraction']*(1-CFG['source']['roll_fraction'])
        r['S_bond_open']=CFG['source']['S_open_Gbond']*(factor**t)
        r['S_coupon_from_G']=CFG['source']['Gcoupon_rate']*r['S_bond_open']
        r['S_net_principal_return_from_G']=(1-factor)*r['S_bond_open']
        r['S_bond_close']=factor*r['S_bond_open'];r['S_admin']=CFG['source']['admin_annual']
        r['required_G_backing_before_reserve']=max(0,r['benefits']+r['S_admin']-r['contributions']-r['credit_transfer']-r['S_coupon_from_G'])
        r['total_required_G_credit_and_backing']=r['credit_transfer']+r['required_G_backing_before_reserve']
        r['actual_source_received']=None
        rows.append(r)
    return dict(cap_multiple_for_NEW_service=cap,opening_prior_bases_use_2W=True,
        authored_not_calibrated=True,cap_notice_full_years=CFG['notice_first_full_years'],
        actual_W_history_and_index=None,actual_mortality=None,
        actual_other_source_inherited_foreign_claims=None,
        tail_scope='Only this fictional Y ledger including its authored prior bases; no bound on unmapped other-source claims',
        retained_top48_is_working_state_not_legal_record_deletion=True,annual_rows=rows,
        closed_accrued_tail=closed_tail(people,pots,CFG['core_projection_years'],longevity))

def liquidity_seed(annual_gross_benefits=228750000*OPENING_INDEX,admin=3000000,openingcash=25000000):
    due=(annual_gross_benefits+admin)/12;target=4*due
    return dict(next_due=due,post_due_four_month_floor=target,
                before_due_cash_required=due+target,additional_cash_source_required=max(0,due+target-openingcash),
                G_counterpart_and_contractual_receipt_dates_required=True,actual_paid_source=None)

def calculate():
    cases=[]
    for name,kw in [('2W',dict(cap=2)),('1W',dict(cap=1)),('1W_longevity',dict(cap=1,longevity=True)),('1W_two_year_wage_cut',dict(cap=1,wage_shock=True))]:
        case=project(**kw);case['scenario']=name;cases.append(case)
    result=dict(status='Authored bounded pension computation seed; not full national funding or actuarial qualification',
        exact_current_frozen_liquidity_seed=liquidity_seed(),cases=cases,
        limitations=['Initial age/history/dependency/mortality/earnings are authored, not observations.',
                    'Expected annual death half-cycle is not a tested individual payment calendar.',
                    'Births enter yearend for cohort accounting; this never delays actual child protection.',
                    'Basic/IC provision is G-financed and excluded here to avoid duplicate older basic.',
                    '75year Gtax/services/investment counterpart is for root integration, not supplied as free backing.',
                    'Future age-specific care, staff, capital, tax/price and foreign capacity must be joined externally.',
                    'Opening S100m Gbond follows authored20%annualmaturity/80%roll/no new Sbid: coupon and principal decay; G source must be paid.',
                    'No automatic tax, benefit cut, age increase or actuarial quote is authorized.',
                    'Unmapped inherited/foreign/other-source claims remain null, not zero; this is no lawful successor map.'])
    return result


if __name__=='__main__':
    (HERE/'cohort-results.json').write_text(json.dumps(calculate(),indent=2)+'\n')
    print('Wrote four75-year authored cohort cases and bounded accrued tails.')
