"""Three authored institutions, same service bid; no behavior or adoption forecast."""
from pathlib import Path
from fractions import Fraction as F
import copy, hashlib, importlib.util, json, sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def q(x): return F(str(x))
def solve(at):
    # Benefit thresholds make consumption piecewise affine; the old single secant
    # is valid for A, but cannot silently be transferred to different institutions.
    lo,hi=F(2000),F(5000)
    flo=at(lo)[0]['consumption']-lo; fhi=at(hi)[0]['consumption']-hi
    assert flo>=0 and fhi<=0, 'No cash root in declared comparison bracket'
    for _ in range(160):
        x=(lo+hi)/2; fx=at(x)[0]['consumption']-x
        if fx==0:return x
        candidate=(lo*fhi-hi*flo)/(fhi-flo)
        if lo<=candidate<=hi and at(candidate)[0]['consumption']==candidate:return candidate
        if fx>0:lo,flo=x,fx
        else:hi,fhi=x,fx
    raise ValueError('Piecewise cash closure did not converge exactly')

def book_module(case):
    path=ROOT/'2026-10-country-operating-book/model.py'
    source=path.read_text()
    old="p0,*_=at(F(2000));p1,*_=at(F(3000));slope=(p1['consumption']-p0['consumption'])/1000;assert 0<=slope<1\n h=(p0['consumption']-slope*2000)/(1-slope);people,gdp,op,taxable=at(h);assert people['consumption']==h"
    assert source.count(old)==1, 'Pinned solver handoff changed'
    source=source.replace(old,"h=_solve69(at);people,gdp,op,taxable=at(h);assert people['consumption']==h")
    spec=importlib.util.spec_from_file_location('book69_'+case,path)
    m=importlib.util.module_from_spec(spec);m._solve69=solve
    exec(compile(source,str(path),'exec'),m.__dict__)
    return m
def clean(x):
    if isinstance(x, F): return float(x)
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, list): return [clean(v) for v in x]
    return x

def adapter(case, settings):
    def personal(d, income, im, taxable_profit, interest_h):
        after = taxable_profit * (1-q(d['rates']['corporate']))
        dg = after*q(d['opening']['public_equity_share']); dh = after-dg
        ct_rate = q(d['rates']['capital_personal'])
        principal = q(settings['mutual_purchase_price'])
        coupon = principal*q(settings['seller_loan_rate'])
        repayment = principal/q(settings['seller_loan_years'])
        common = (1-ct_rate)*(dh-coupon)-repayment if case == 'C' else F(0)
        # C trial points may have negative fund cash: disclose, never clamp or borrow.
        if case == 'C' and common < 0:
            raise ValueError('Fund cannot pay debt service from declared dividend')
        totals = {k:F(0) for k in ['work_tax','capital_tax','contribution',
                  'general_transfers','consumption','earned','survivors']}
        rows = []
        for group in income['population_groups']:
            for person in group['members']:
                g=q(person.get('gross',0)); kind=person['kind']
                m=F(600) if kind=='child' else F(1000)
                paid=q(person.get('support_paid',0)); received=q(person.get('support_received',0))
                access=q(person.get('disability_cost',0))
                earned=q(d['insurance']['monthly_earned']) if kind=='older' else F(0)
                survivor=F(*d['insurance']['survivor_monthly_exact']) if group['label']==d['insurance']['survivor_group'] and kind=='child' else F(0)
                tax, contribution, net = im.tax_and_net(g, income['policy'])
                if case == 'B':
                    contribution=g/10; tax=g*q(settings['universal_gross_wage_tax']); net=g-tax-contribution
                    grosscap=(dh+interest_h)*10**6/(5000*12) if g>=10000 else F(0)
                    capnet=grosscap*(1-ct_rate); cap_tax=grosscap*ct_rate
                    base=m+300; bonus=min(F(300),(g-contribution)/2)
                    before=net+base+bonus+earned+survivor+received+capnet-paid
                    hardship=max(F(0),m+300-before)
                    transfer=base+bonus+hardship+access
                    disp=before+hardship+access
                elif case == 'C':
                    shared=common*10**6/(100000*12)
                    owner=(1-ct_rate)*(coupon+interest_h)+repayment if g>=10000 else F(0)
                    capnet=shared+owner*10**6/(5000*12)
                    # Pass-through tax precedes principal. Internal H principal is not income.
                    cap_tax=ct_rate*(dh-coupon)*10**6/(100000*12)
                    if g>=10000: cap_tax+=ct_rate*(coupon+interest_h)*10**6/(5000*12)
                    vat=F(40)*10**6/(100000*12); basic=m if kind=='older' else F(0)
                    credit=earned-min(earned/5,m/5)
                    top=max(F(0),m+300+min(paid,F(900))-basic-credit-survivor-received-vat-capnet-max(F(0),net-m/5)/2)
                    transfer=basic+vat+top+access
                    disp=net+transfer+earned+survivor+received+capnet-paid
                else: raise ValueError('Unsupported institution')
                mul=group['count']*12/F(10**6)
                for key,value in [('work_tax',tax),('capital_tax',cap_tax),('contribution',contribution),('general_transfers',transfer),('consumption',disp),('earned',earned),('survivors',survivor)]:
                    totals[key]+=value*mul
                rows.append({'group':group['label'],'count':group['count'],'kind':kind,'ordinary_margin':disp-access-m-300})
        return {**totals,'dividend_G':dg,'dividend_H':dh,
                'corporate_tax':taxable_profit*q(d['rates']['corporate']),'person_margins':rows}
    return personal

def calculate(settings=None):
    if settings is None: settings=json.loads((HERE/'inputs.json').read_text())
    allowed={'edition','date','pinned_sources','universal_gross_wage_tax','universal_capital_personal_tax','mutual_purchase_price','seller_loan_rate','seller_loan_years','limits'}
    if set(settings)!=allowed: raise ValueError('Unknown or absent comparison semantics')
    for path,h in settings['pinned_sources'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
    assert 0<=q(settings['universal_gross_wage_tax'])<=F('.9')
    assert 0<=q(settings['universal_capital_personal_tax'])<=1
    assert q(settings['mutual_purchase_price'])>0 and q(settings['seller_loan_rate'])>=0 and q(settings['seller_loan_years'])>0
    base=json.loads((ROOT/'2026-10-country-operating-book/inputs.json').read_text())
    income=json.loads((ROOT/'2026-10-income-floor/inputs.json').read_text())
    im=module('income69',ROOT/'2026-10-income-floor/model.py')
    cases={}; modules={}; data={}
    for case in ['A','B','C']:
        book=book_module(case)
        d=copy.deepcopy(base)
        if case=='B': d['rates']['capital_personal']=settings['universal_capital_personal_tax']
        if case!='A':
            book.personal=adapter(case,settings)
            d['limits']=[x for x in d['limits'] if 'under unchanged I05' not in x]+settings['limits']
        result=book.calculate(d)
        if case!='A':
            result['edition']=69;result['case']=case
            result['book_status']='Alternative income/ownership mechanism under unchanged resource bids; not a qualified country'
        cases[case]=result; modules[case]=book; data[case]=d
    benchmark=cases['A']; common={}; baseline_rows=None; incidence={}
    for case in ['A','B','C']:
        people=modules[case].personal(data[case],income,im,q(benchmark['taxable_market_profit']),F('21.25'))
        rows=people['person_margins'];common[case]=people
        if case=='A': baseline_rows=rows
        differences=[];winners=losers=unchanged=0;bridge=F(0)
        for old,new in zip(baseline_rows,rows):
            assert (old['group'],old['kind'],old['count'])==(new['group'],new['kind'],new['count'])
            delta=new['ordinary_margin']-old['ordinary_margin'];n=new['count']
            if delta>0:winners+=n
            elif delta<0:losers+=n;bridge-=delta*n*12/F(10**6)
            else:unchanged+=n
            differences.append({**new,'monthly_change':delta,'ordinary_monthly_cash':new['ordinary_margin']+(900 if new['kind']=='child' else 1300)})
        incidence[case]={'people_gaining':winners,'people_losing':losers,'people_unchanged':unchanged,'one_year_no_cash_loss_sensitivity':bridge,'rows':differences}
    dh=q(benchmark['people']['dividend_H']);price=q(settings['mutual_purchase_price'])
    rate=q(settings['seller_loan_rate']);years=q(settings['seller_loan_years']);net=F('.6')
    stress_price=20*dh
    ownership={'purchase_price':price,'seller_coupon':price*rate,'year_one_principal':price/years,'closing_seller_debt':price-price/years,
       'minimum_dividend_for_debt_service':price*(rate+1/(net*years)),
       'benchmark_dividend_to_book_price':dh/price,
       'authored_20_times_dividend_price':stress_price,
       'cash_after_debt_at_20_times_price_and_benchmark_dividend':net*(dh-stress_price*rate)-stress_price/years,
       'actual_market_price':None,'actual_seller_consent':None,'actual_transaction_tax':None}
    return clean({'edition':69,'cases':cases,'common_output_people':common,'incidence_at_common_output':incidence,
       'ownership':ownership,'selection':'Retain conditional I05; neither rival nor the baseline qualifies an operating country',
       'actual_affected_participation':None,'independent_review':None,'legal_adoption':None,'actual_readiness':False,'observed_superiority':None,'limits':settings['limits']})

if __name__=='__main__': print(json.dumps(calculate(),indent=2))
