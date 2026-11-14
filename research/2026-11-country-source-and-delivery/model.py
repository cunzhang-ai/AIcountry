"""Join compatible declared subsets; never manufacture a full national source."""
import json, importlib.util
from pathlib import Path
from datetime import date
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def read(p):
    return json.loads(p.read_text())

def first_january(d,months):
    # Jan 1 must be at least the full notice interval after this authored date.
    year=d.year+(d.month-1+months)//12
    month=(d.month-1+months)%12+1
    return date(year if (month,d.day)==(1,1) else year+1,1,1).isoformat()

def tax_exact(q,M,A):
    q=max(F(0),q-A);out=F(0)
    for width,rate in [(M/2,F(1,5)),(M/2,F(7,20)),(M,F(9,20)),(None,F(11,20))]:
        amount=q if width is None else min(q,width)
        out+=rate*amount;q-=amount
    return out

def benefit_grossup(V,O,M,A):
    if min(V,O,A)<0 or M<=0:raise ValueError('Unsupported negative amount or nonpositive M')
    prior=tax_exact(O,M,A)
    for lo,hi,rate in [(F(0),A,F(0)),(A,A+M/2,F(1,5)),(A+M/2,A+M,F(7,20)),(A+M,A+2*M,F(9,20)),(A+2*M,None,F(11,20))]:
        intercept=tax_exact(lo,M,A)-rate*lo
        g=(rate*(O+V)+intercept-prior)/(1-rate)
        if g>=0 and O+V+g>=lo and (hi is None or O+V+g<=hi):
            assert g==tax_exact(O+V+g,M,A)-prior
            return dict(g=g,c=(V+g)/9)
    raise ValueError('No consistent gross-up bracket')

def money(v):
    # Nonnegative, half-up minor units, same normative NF rule.
    return F((v*100+F(1,2)).numerator//(v*100+F(1,2)).denominator,100)

def minor_grossup(V,cash,other,M,A):
    if min(V,cash,other,A)<0 or M<=0 or (V*100).denominator!=1:raise ValueError('Unsupported currency or negative amount')
    oldY=money(cash/10);O=cash-oldY+other;oldT=money(tax_exact(O,M,A))
    def at(cents):
        P=F(cents,100);c=money((cash+P)/10)-oldY;g=money(tax_exact(O+P-c,M,A))-oldT
        return P-c-g,g,c
    low=0;high=max(1,int(V*100))
    while at(high)[0]<V:high*=2
    while high-low>1:
        mid=(low+high)//2
        if at(mid)[0]>=V:high=mid
        else:low=mid
    net,g,c=at(high)
    return dict(P=F(high,100),g=g,c=c,net=net,previous_net=at(high-1)[0] if high else F(0))

def annual_package(year,first_lawful_U,full_U_tax_from_year):
    # A transition classifier, not U eligibility, commencement or actual receipt.
    first=date.fromisoformat(first_lawful_U) if first_lawful_U else None
    full=first is not None and first<=date(year,1,1) and full_U_tax_from_year is not None and year>=full_U_tax_from_year
    return dict(tax_package='full_U_no_A' if full else 'I05_with_A',
        first_midyear_U_plus_A=bool(first and first.year==year and first>date(year,1,1)),
        U_eligibility_date_unchanged=first_lawful_U,actual_paid_U=None,protection_for_involuntary_nonreceipt=None)

def compute():
    inp=read(HERE/'inputs.json');src=inp['sources']
    ps=read(ROOT/src['physical']);pa=read(ROOT/src['ordinary_goods'])
    persons=read(ROOT/src['persons']);reg=read(HERE/'delivery-register.json')
    spec=importlib.util.spec_from_file_location('frozen_PA_personal',ROOT/src['personal_calculation'])
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    tax=dict(persons['tax']);tax['comparison_general_personal_allowance_CU']=inp['allowance_fraction_M']*tax['annual_tax_scale_M']
    cases=[]
    for c in ps['cases']:
        f,w,p=c['food'],c['water'],c['power']
        cases.append(dict(id=c['id'],holding_ha=f['holding_ha'],field_hours=f['field_cover_hours'],
            annual_field_role_bound=f['roles']['field_and_cover']['annual_post_bound'],harvest_peak_people_bound=f['harvest_favorable_peak_people_bound'],
            extra_water_m3=w['additional_source_required_m3'],source_capacity_m3=w['normal_source_capacity_m3'],
            normal_water_volume_pass=w['normal_source_volume_bound_pass'],
            drought_source_gap_m3=max(0,w['drought20_additional_source_m3']-w['normal_source_capacity_m3']),
            one_tank_lost_pass=w['one_tank_lost_stock_pass'],all_fresh_source_loss_pass=w['all_source_stock_pass'],
            named_PS_quote_CU=c['named_recurring_FX_quote_CU'],
            disjoint_PA_goods_border_quote_CU=pa['ordinary_goods']['annual_final_goods_border_quote_CU'],
            compatible_named_quote_subtotal_CU=c['named_recurring_FX_quote_CU']+pa['ordinary_goods']['annual_final_goods_border_quote_CU'],
            quote_is_complete_or_owned_FX=False,actual_received_owned_FX=None,
            grid_stress=p['stress'],full_national_power_GWh=None,
            current_country_budget_CU=None,accepted_simultaneous_delivery=None,launch_established=False))
    personal=[]
    for person in persons['persons']:
        if person.get('foundation_receipt_fraction',1)!=1:continue
        vals={key:mod.payment(person,tax,kind) for key,kind in [('access_first','retained_I05'),('full_U','protected_foundation'),('U_plus_allowance_rival','extra_personal_allowance')]}
        personal.append(dict(person=person,**vals,scope='Separate fixed-price personal case, no full source/transition/take-up or country tax yield'))
    entrants=[]
    M=F(str(tax['annual_tax_scale_M']));A=F(str(inp['allowance_fraction_M']))*M
    for y in [2028,2029,2030]:
        first=date(y,7,1);days=(date(y+1,1,1)-date(y,1,1)).days
        covered=(date(y+1,1,1)-first).days
        # Separate high-income fixture: no residual claim; no national entrant forecast.
        q=F(108000);B=F(str(tax['ordinary_adult_basket_CU']))
        entrants.append(dict(year=y,people_hypothesis=1,first_legal_U=first.isoformat(),calendar_days=days,U_eligible_days=covered,
            annual_A_CU=float(A),time_proportional_U_due_CU=float(B*covered/days),
            personal_tax_A_CU=float(tax_exact(q,M,A)),personal_tax_full_U_schedule_CU=float(tax_exact(q,M,F(0))),
            extra_tax_relief_from_transition_A_CU=float(tax_exact(q,M,F(0))-tax_exact(q,M,A)),
            actual_received_U=None,actual_country_entrant_numbers=None,
            scope='Separate annual high-income entrant case, not within-year benefit reconciliation or national source'))
    entrants.append(dict(kind='short_domestic_source_no_U',taxable_Q_CU=2000,annual_A_CU=float(A),
        tax_CU=float(tax_exact(F(2000),M,A)),U_due_CU=0,actual_tax_source=None,
        scope='Normative full annual allowance for short source period, no actual receipt/tax-base finding'))
    d=date.fromisoformat(inp['adoption_date_hypothesis'])
    return dict(edition=106,scope=inp['scope'],function_count=len(reg['functions']),later_package_count=len(reg['later_packages']),
        physical_cases=cases,personal_cases=personal,
        authored_notice_starts={str(n):first_january(d,n) for n in [12,18,24]},
        country_alternatives=[dict(id=key,status='Defined research alternative, no full matched source/delivery account',current_country_cost_CU=None,
            owned_cash_FX_and_accepted_simultaneous_delivery=None) for key in ['A_access_first_mixed_repair','B_access_first_import_bulk','C_full_U','D_prepaid_residual','E_direct_public']],
        noncash_source_year_probes={k:{n:str(v) for n,v in benefit_grossup(F(100),F(0),F(1000),A).items()} for k,A in [('I05_A400',F(400)),('full_U_A0',F(0))]},
        recurring_entrant_examples=entrants,
        minor_source_year_probes={k:{n:str(v) for n,v in minor_grossup(F(100),F(0),F(0),F(1000),A).items()} for k,A in [('I05_A400',F(400)),('full_U_A0',F(0))]},
        annual_transition_examples=[annual_package(2028,'2028-07-01',2029),annual_package(2029,'2028-07-01',2029)],
        national_GDP=None,national_tax_yield=None,joined_current_national_cost=None,
        physical_quote_is_national_budget=False,actual=inp['actual'])

if __name__=='__main__':
    (HERE/'results.json').write_text(json.dumps(compute(),indent=2)+'\n')
