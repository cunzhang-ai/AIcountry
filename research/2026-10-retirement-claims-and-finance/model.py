"""Authored pension formula/boundary examples; not an actuarial population forecast."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def q(x):return F(str(x))
def clean(x):
 if isinstance(x,F):return float(x)
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,list):return [clean(v) for v in x]
 return x

def year_base(y,p):
 w=q(y['reference_wage']);assert w>0
 earned=F(0);raw_credit=F(0);months=set()
 for period in y['periods']:
  start,end=period['from_month'],period['until_month'];assert 0<=start<end<=12
  occupied=set(range(start,end));assert not occupied & months,'overlapping service period'
  months|=occupied;f=F(end-start,12);pay=q(period['annualized_labor_pay']);assert pay>=0
  receipt=pay*f;earned+=receipt
  if period.get('eligible_credit',False):raw_credit+=max(F(0),q(p['credit_reference_fraction'])*w*f-receipt)
 cap=q(p['annual_accrual_base_multiple'])*w*F(len(months),12)
 base=min(cap,earned+raw_credit);recognized_credit=base-min(cap,earned)
 inflation=F(1)
 for ratio in y.get('price_ratios_since_service',[1]):
  assert q(ratio)>0
  inflation*=max(F(1),q(ratio))
 return {'service_year':y['year'],'cash_earnings':earned,'covered_months':len(months),
  'benefit_base':base,'revalued_base':base*inflation,'recognized_credit_base':recognized_credit,
  'worker_contribution':earned*q(p['worker_contribution_rate']),
  'public_credit_transfer':recognized_credit*q(p['worker_contribution_rate'])}

def career(records,p):
 assert len({y['year'] for y in records})==len(records),'duplicate service year'
 rows=[year_base(y,p) for y in records]
 selected=sorted(rows,key=lambda x:x['revalued_base'],reverse=True)[:p['maximum_calendar_bases']]
 annual=sum((y['revalued_base'] for y in selected),F(0))*q(p['annual_accrual_rate'])
 return {'annual_earned_at_standard_age':annual,'monthly_earned_exact':annual/12,'service_calendar_years':len(rows),
  'used_calendar_bases':len(selected),'service_year_worker_contributions':sum((y['worker_contribution'] for y in rows),F(0)),
  'service_year_public_credit_transfers':sum((y['public_credit_transfer'] for y in rows),F(0)),
  'annual_records':rows,'actual_claim_or_funding':None}

def survivors(annual,losses,p):
 losses=[q(v) for v in losses];assert all(v>=0 for v in losses)
 pot=q(annual)*q(p['survivor_pot_fraction']);total=sum(losses,F(0));paid=min(pot,total)
 shares=[paid*x/total if total else F(0) for x in losses]
 return {'maximum_annual_pot':pot,'actual_lost_support':total,'annual_shares':shares,'unallocated_pot':pot-paid,'eligibility_and_receipt_actually_verified':None}

def annuity_quote(survival,chosen,tail_known=True):
 assert 60<=chosen<=70
 if chosen==65:return F(1)
 # One common base age; omission of deferred-start survival would misprice shares.
 if survival is None or not tail_known:return None
 assert 60<=chosen<=70 and 65 in survival and chosen in survival
 ages=sorted(survival);assert ages[0]==60
 probabilities=[q(survival[a]) for a in ages]
 assert all(0<=v<=1 for v in probabilities) and all(a>=b for a,b in zip(probabilities,probabilities[1:]))
 assert probabilities[-1]==0,'authored finite tail must explicitly close'
 standard=sum((q(v) for age,v in survival.items() if age>=65),F(0))
 elected=sum((q(v) for age,v in survival.items() if age>=chosen),F(0))
 assert standard>0 and elected>0
 return standard/elected

def calculate():
 d=json.loads((HERE/'inputs.json').read_text());p=d['parameters']
 for path,h in d['pinned_sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
 results={}
 for c in d['career_cases']:
  records=[]
  for block in c['blocks']:
   for _ in range(block['years']):records.append({'year':len(records)+1,'reference_wage':block.get('reference_wage',30000),'price_ratios_since_service':block.get('price_ratios_since_service',[1]),'periods':block['periods']})
  results[c['name']]=career(records,p)
 finance=[]
 for c in d['finance_histories']:
  annual=q(c['monthly_earned'])*12 if 'monthly_earned' in c else results[c['career']]['annual_earned_at_standard_age']
  paid=annual*d['aggregate']['retired_people']/10**6
  due=paid/12;floor=due*p['reserve_months'];cash=q(d['aggregate']['restricted_opening_cash'])
  finance.append({'case':c['name'],'annual_earned_payment_million':paid,
   'known_receipts_less_earned_payments_before_omissions':q(d['aggregate']['known_worker_receipts'])+q(d['aggregate']['known_bond_interest'])-paid,
   'day1_payment_due':due,'day1_cash_paid_without_new_source':min(cash,due),
   'day1_unpaid_without_new_source':max(F(0),due-cash),'cash_after_actual_day1_payment':max(F(0),cash-due),
   'four_month_normal_cash_floor_before_omitted_costs':floor,
   'extra_cash_needed_to_pay_and_retain_floor':max(F(0),due+floor-cash),
   'actual_administration_survivor_credit_costs':None,'actual_asset_liability_valuation':None,'actual_readiness':False})
 alive={a:(1 if a<85 else 0) for a in range(60,86)}
 declining={a:(F(1) if a<65 else F('0.9') if a<85 else F(0)) for a in range(60,86)}
 return clean({'edition':65,'status':'Authored formula and alternative-history checks only; no population or solvency forecast',
  'careers':results,'survivors':{'two_dependants':survivors(15000,[4000,8000],p),'loss_below_pot':survivors(15000,[300,1200],p),'zero_proven_loss':survivors(15000,[0,0],p)},
  'toy_annuity_quotes':{'certain_alive_to_85_age60':annuity_quote(alive,60),'certain_alive_to_85_age65':annuity_quote(alive,65),'certain_alive_to_85_age70':annuity_quote(alive,70),'explicit_survival_to_65_age60':annuity_quote(declining,60),'missing_real_life_table':annuity_quote(None,60),'ordinary_age_without_life_table':annuity_quote(None,65),'unbounded_tail':annuity_quote(alive,60,False)},
  'finance_histories':finance,'basic_annual_million_at_reference_basket':q(d['aggregate']['adult_ordinary_monthly'])*12*d['aggregate']['retired_people']/10**6,
  'actual_lifetime_claims':None,'actual_population_histories':None,'actual_observed_outcomes':None,'limits':d['limits']})
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
