"""One proposed operating bid book. Allocation is not a workload or feasibility certificate."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def q(x):return F(str(x))
def clean(x):
 if isinstance(x,F):return float(x)
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,list):return [clean(v) for v in x]
 return x
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def personal(d,income,im,taxable_profit,interest_h):
 after=taxable_profit*(1-q(d['rates']['corporate']));dg=after*q(d['opening']['public_equity_share']);dh=after-dg
 capital=(dh+interest_h)*10**6/(5000*12);vat=F(40)*10**6/(100000*12)
 totals={k:F(0) for k in ['work_tax','capital_tax','contribution','general_transfers','consumption','earned','survivors']};totals['general_transfers']=40;rows=[]
 for group in income['population_groups']:
  for person in group['members']:
   g=q(person.get('gross',0));m=F(600) if person['kind']=='child' else F(1000);paid=q(person.get('support_paid',0));received=q(person.get('support_received',0))
   basic=m if person['kind']=='older' else F(0);earned=q(d['insurance']['monthly_earned']) if person['kind']=='older' else F(0)
   survivor=F(*d['insurance']['survivor_monthly_exact']) if group['label']==d['insurance']['survivor_group'] and person['kind']=='child' else F(0)
   cap=capital if g>=10000 else F(0);ct=cap*q(d['rates']['capital_personal']);capnet=cap-ct
   tax,contribution,net=im.tax_and_net(g,income['policy']);credit=earned-min(earned*F('.2'),m*F('.2'))
   n=m+300+min(paid,F(900));top=max(F(0),n-basic-credit-survivor-received-vat-capnet-F('.5')*max(F(0),net-m*F('.2')))
   access=q(person.get('disability_cost',0));disp=net+basic+earned+survivor+received+vat+top+capnet-paid+access;mul=group['count']*12/F(10**6)
   for k,value in [('work_tax',tax),('capital_tax',ct),('contribution',contribution),('general_transfers',basic+top+access),('consumption',disp),('earned',earned),('survivors',survivor)]:totals[k]+=value*mul
   rows.append({'group':group['label'],'count':group['count'],'kind':person['kind'],'ordinary_margin':disp-access-m-300})
 return {**totals,'dividend_G':dg,'dividend_H':dh,'corporate_tax':taxable_profit*q(d['rates']['corporate']),'person_margins':rows}

def calculate(d=None):
 if d is None:d=json.loads((HERE/'inputs.json').read_text())
 allowed={'edition','date','scope','pinned_sources','payroll','operating_components','rates','opening','insurance','limits'}
 if set(d)-allowed:raise ValueError('Unsupported country-book semantics')
 for path,h in d['pinned_sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
 income=json.loads((ROOT/'2026-10-income-floor/inputs.json').read_text());im=module('old_income',ROOT/'2026-10-income-floor/model.py');old=module('old_fx',ROOT/'2026-10-demand-and-steady-stocks/model.py')
 registry=json.loads((HERE/'predecessor-design-67/settlement/commitments/inventory.json').read_text());functions={f['id']:{'function':f['function'],'operator':f['operator'],'proposed_cash_bid':F(0),'components':[],'actual_quantity':None,'actual_cost':None,'workload_qualified':False} for f in registry['functions']}
 components=[];wages=F(0);heads=F(0);high=F(0)
 for group in d['payroll']:
  fraction=F(group.get('months',12),12);n=F(group['higher_people']+group['middle_people'])*fraction;cost=(F(group['higher_people'])*F('.06')+F(group['middle_people'])*F('.03'))*fraction
  heads+=n;high+=F(group['higher_people'])*fraction;wages+=cost;components.append({'id':group['id'],'kind':'payroll','cash':cost,'import_component':F(0),'person_years':n,'shares':group['shares']})
 for c in d['operating_components']:components.append({'id':c['id'],'kind':'purchases','cash':q(c['cash']),'import_component':q(c['imports']),'shares':c['shares']})
 assert len({c['id'] for c in components})==len(components)
 for c in components:
  assert sum(q(s) for s in c['shares'].values())==1 and 0<=c['import_component']<=c['cash']
  for fid,share in c['shares'].items():
   assert fid in functions
   value=c['cash']*q(share);functions[fid]['proposed_cash_bid']+=value;functions[fid]['components'].append({'component':c['id'],'share':q(share),'cash':value})
 cash=sum(c['cash'] for c in components);o=d['opening'];rates=d['rates'];cfG=q(o['public_real'])*q(rates['wear']);cfF=q(o['market_real'])*q(rates['wear']);ig=cfG;iv=cfF
 public_imports=sum(c['import_component'] for c in components)+ig/2;private_imports=F(280)+F(30)+iv/2
 ir=q(o['foreign_bonds'])*q(rates['sovereign_interest']);ih=q(o['household_bonds'])*q(rates['sovereign_interest']);is_=q(o['insurance_bonds'])*q(rates['sovereign_interest']);ib=q(o['bank_bonds'])*q(rates['sovereign_interest'])
 line_d={'opening':{'foreign_reserves':0,'reserve_floor':0,'contingent_fx_limit':64},'rates':{'fx_line_interest':.05}}
 fx=old.fx_timeline(line_d,private_imports,F(0),F(1));carry=fx['normal_line_carry'];fee=F(1)
 public_purchase=public_imports+ir;exports=public_purchase+private_imports+carry+fee;imports=public_imports+private_imports
 ratio=F(265,1800);total_wages=F(2280);prodlevy=F(155)
 def at(h):
  gdp=h+cash+cfG+ig+iv+exports-imports;op=gdp-total_wages-ratio*h-prodlevy-cfG-cfF;taxable=op+ib-carry-fee
  assert taxable>0
  return personal(d,income,im,taxable,ih),gdp,op,taxable
 p0,*_=at(F(2000));p1,*_=at(F(3000));slope=(p1['consumption']-p0['consumption'])/1000;assert 0<=slope<1
 h=(p0['consumption']-slope*2000)/(1-slope);people,gdp,op,taxable=at(h);assert people['consumption']==h
 administration=q(d['insurance']['administration']);credits=q(d['insurance']['credit_transfer']);backing=max(F(0),people['earned']+people['survivors']+administration-people['contribution']-is_-credits)
 flows=[]
 def post(a,b,n,label):
  assert n>=0;flows.append({'payer':a,'receiver':b,'amount':n,'label':label})
 public_inter_import=public_imports-ig/2
 for a,b,n,label in [('H','F',h-ratio*h-280,'domestic consumption'),('H','G',ratio*h,'product tax'),('H','R',F(280),'household imports'),('R','F',exports,'conditional delivered exports'),('G','H',wages,'proposed public payroll'),('F','H',total_wages-wages,'remaining market payroll'),('G','F',cash-wages-public_inter_import,'domestic public purchases'),('G','R',public_inter_import,'imported public purchases'),('G','F',ig/2,'domestic public replacement'),('G','R',ig/2,'imported public replacement'),('F','R',F(30)+iv/2,'market input/replacement imports'),('F','R',carry+fee,'private FX line carry/fee'),('F','G',prodlevy,'production levies'),('F','G',people['corporate_tax'],'corporate tax'),('F','G',people['dividend_G'],'owned dividend'),('F','H',people['dividend_H'],'private dividends'),('H','G',people['work_tax']+people['capital_tax'],'personal tax'),('H','S',people['contribution'],'restricted contributions'),('S','H',people['earned']+people['survivors'],'earned and survivor payments'),('G','H',people['general_transfers'],'basic, needs, access and tax relief'),('G','H',ih,'household bond coupon'),('G','S',is_,'insurance bond coupon'),('G','F',ib,'bank-held sovereign coupon'),('G','R',ir,'foreign sovereign coupon'),('G','S',credits+backing,'explicit credits and public backing'),('S','G',administration,'administration funding included once in public components')]:post(a,b,n,label)
 balances={s:F(0) for s in ['G','H','F','S','R']}
 for f in flows:balances[f['payer']]-=f['amount'];balances[f['receiver']]+=f['amount']
 assert sum(balances.values())==0
 gout=sum(f['amount'] for f in flows if f['payer']=='G');gin=sum(f['amount'] for f in flows if f['receiver']=='G');sout=sum(f['amount'] for f in flows if f['payer']=='S');sin=sum(f['amount'] for f in flows if f['receiver']=='S')
 monthly_public=[]
 for month in range(1,13):
  pay=F(0)
  for group in d['payroll']:
   active=group.get('active_months',list(range(1,13)));assert len(active)==group.get('months',12) and len(set(active))==len(active)
   if month in active:pay+=(F(group['higher_people'])*F('.06')+F(group['middle_people'])*F('.03'))/12
  monthly_public.append(pay)
 running=q(o['treasury_cash']);g_calendar=[]
 for month,pay in enumerate(monthly_public,1):
  due=(gout-wages)/12+pay;before=running-due;running=before+gin/12
  g_calendar.append({'month':month,'public_payroll_due':pay,'cash_before_receipts':before,'cash_close':running})
 assert running==q(o['treasury_cash'])+balances['G']
 private_working_peak=max(total_wages/12-pay for pay in monthly_public)
 peak_deposits=q(o['deposits'])+private_working_peak;liquidity_gap=max(F(0),peak_deposits*F('.6')-q(o['bank_reserves']));collateral=F(250)*F('.8')+F(275)*F('.6')
 net_private_shock=max(F(0),exports*F('.9')-public_purchase-fee);shock_factor=net_private_shock/fx['normal_export_contract'];shock=old.fx_timeline(line_d,private_imports,F(0),shock_factor,2)
 market_gva=gdp-cash-cfG;private_people=55000-heads;energy=F(430)+600*market_gva/2202;water=F('2.6')+4*market_gva/2202-F('1.5')
 known_net={'G':q(o['public_real'])+q(o['treasury_cash'])+F(175)+F('436.25')-(q(o['gross_bonds'])-100)-175,'H':F(425)+F('1308.75'),'S':F(100)+q(o['insurance_cash']),'F':F(1920)+175+250-q(o['deposits'])-1745,'R':F(205)-175}
 return clean({'edition':68,'book_status':'Proposed bid allocation; no function workload is fully qualified','components':components,'functions':functions,'public_person_years':heads,'public_distinct_people':sum(g['higher_people']+g['middle_people'] for g in d['payroll']),'public_higher_pay_person_years':high,'public_payroll':wages,'public_operating_cash':cash,'public_replacement':ig,'private_replacement':iv,'required_household_consumption':h,'required_GDP':gdp,'market_required_GVA':market_gva,'required_market_productivity_ratio':(market_gva/private_people)/(F(2202)/44910),'taxable_market_profit':taxable,'market_operating_profit_GDP':op,'people':people,'flows':flows,'sector_current_balances':balances,'G_receipts':gin,'G_cash_out':gout,'G_monthly_conservative_cash_trough':min(row['cash_before_receipts'] for row in g_calendar),'G_monthly_calendar':g_calendar,'S_receipts':sin,'S_out':sout,'S_backing_transfer':backing,'S_cash_after_first_payment':q(o['insurance_cash'])-sout/12,'S_four_month_normal_floor':sout/3,'opening_known_net_positions':known_net,'opening_total_known_real':q(o['public_real'])+q(o['market_real']),'pension_liability_symbol':'L(t), paired H asset/S liability; actual value and changes unknown','normal_private_FX':fx,'normal_public_FX':{'monthly_supplier_and_coupon_due':public_purchase/12,'reserve_before_contract_replenishment':F(100)-public_purchase/12,'reserve_after_conditional_private_purchase':100,'public_borrowing_or_private_reserve_pledge':0,'actual_exporter_sale_permission':None},'private_FX_under_10pct_gross_export_loss':shock,'gross_exports_required':exports,'imports':imports,'public_FX_purchase_from_private_sources':public_purchase,'private_monthly_payroll_working_need':private_working_peak,'peak_bank_deposits':peak_deposits,'bank_60pct_withdrawal_gap':liquidity_gap,'conditional_domestic_liquidity_capacity':min(F(300),collateral),'bank_residual_gap_after_conditional_capacity':max(F(0),liquidity_gap-300),'new_bank_and_old_maturity_first_month_cash_before_changed_flows':q(o['treasury_cash'])-F(330)-(gout-wages)/12-monthly_public[0],'energy_required':energy,'water_required':water,'ordinary_energy_available':1450,'loss_energy_available':1300,'ordinary_water_available':7.5,'loss_water_available':6.6,'ordinary_energy_water_fit':energy<=1450 and water<=F('7.5'),'loss_energy_water_fit':energy<=1300 and water<=F('6.6'),'actual_opening_transactions':None,'actual_full_duty_costs':None,'all_unmodeled_requirements_are_priced':False,'actual_qualified_private_output':None,'actual_operational_readiness':False,'observed_superiority':None,'limits':d['limits']})
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
