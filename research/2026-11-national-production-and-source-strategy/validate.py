"""Bounded exact-scope and authored circuit checks; no economic calibration or policy certification."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal as Q
import json,hashlib,subprocess,sys
import model
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text());q=lambda x:Q(str(x));checks=[]
def check(name,c):
 if not c:raise AssertionError(name)
 checks.append(name)
base=read(D/'baseline.json');check('1024 exact predecessor artifacts',len(base['sha256'])==1024)
for n,h in base['sha256'].items():check('snapshot:'+n,hashlib.sha256((D/'predecessor-design-132'/n).read_bytes()).hexdigest()==h)
pins=read(D/'source-manifest.json')
for n,h in pins['sha256'].items():check('pin:'+n,hashlib.sha256((R/n).read_bytes()).hexdigest()==h)
old=read(D/'predecessor-design-132/settlement/commitments/inventory.json');now=read(R/'settlement/commitments/inventory.json')
check('37 complete function objects exact',now['functions']==old['functions'] and len(now['functions'])==37)
check('61 selection objects exact',now['selections']==old['selections'] and len(now['selections'])==61)
refs={k:v for k,v in old.items() if k.endswith('_reference')};check('72 inherited references exact',len(refs)==72 and all(now[k]==v for k,v in refs.items()))
for n in ['FRAMEWORK.md','DECISION-TEMPLATE.md']:check('common method unchanged:'+n,(R/n).read_bytes()==(D/'predecessor-design-132'/n).read_bytes())
cfg=read(D/'inputs.json');result=model.compute();check('fresh circuit reproduction',result==read(D/'results.json'))
check('seven distinct authored circuits',len(result['cases'])==7 and len({x['id'] for x in result['cases']})==7)
cases={x['id']:x for x in result['cases']}
for x in result['cases']:
 name=x['id'];s=next(z for z in cfg['scenarios'] if z['id']==name);rate=q(s['u_per_f']);Dnet=q(x['net_public_nonfinancial_borrowing_u']);H=q(x['household_net_financial_lending_u']);F=q(x['firm_and_financial_sector_net_financial_lending_u']);W=q(x['rest_of_world_net_financial_lending_u']);new=q(x['new_public_domestic_claims_needed_u']);sold=q(x['public_owned_FX_sold_f']);retained=q(x['private_owned_surplus_retained_f'])
 check('complete stated sector-flow identity:'+name,-Dnet+H+F+W==0 and q(x['balance_identity_residual_u'])==0)
 check('asset disposal not revenue or duplicated financing:'+name,new+sold*rate==Dnet)
 check('domestic holder claims match:'+name,H+q(x['firm_sector_domestic_claim_increase_u'])==new)
 check('private retained FX remains its asset:'+name,q(x['firm_sector_domestic_claim_increase_u'])+retained*rate==F)
 check('national external flow matches separate titles:'+name,(sold-retained)*rate==W)
 check('public sales attributed once:'+name,sold==q(x['household_FX_from_public_f'])+q(x['firm_FX_from_public_f']))
 check('private own foreign receipts used once:'+name,q(s['export_f'])+q(x['firm_FX_from_public_f'])==q(cfg['flows']['firm_import_f'])+q(x['private_owned_surplus_voluntarily_sold_f'])+retained)
 check('household imports have actual authored owner sources:'+name,q(x['household_FX_from_public_f'])+q(x['private_owned_surplus_voluntarily_sold_f'])==q(cfg['flows']['household_import_f']))
 check('no calibration or current authority certificate:'+name,x['actual_suppliers_receipts_sources_holders_authority_output_or_inflation'] is None)
 for p in x['periods']:
  check('failed foreign path never books negative stock:'+name+str(p['period']),p['foreign_only_stress_closing_f'] is None or q(p['foreign_only_stress_closing_f'])>=q(s['public_floor_f']))
check('known base financing/private/foreign values',all(q(cases['base_bonds'][k])==v for k,v in [('net_public_nonfinancial_borrowing_u',150),('household_net_financial_lending_u',80),('firm_and_financial_sector_net_financial_lending_u',40),('rest_of_world_net_financial_lending_u',30),('new_public_domestic_claims_needed_u',120)]))
check('bond and issue same stated real flow/financial aggregate',all(cases['base_bonds'][k]==cases['base_finite_issue'][k] for k in ['net_public_nonfinancial_borrowing_u','household_net_financial_lending_u','firm_and_financial_sector_net_financial_lending_u','rest_of_world_net_financial_lending_u','new_public_domestic_claims_needed_u','first_foreign_stock_or_gross_limit_failure_in_conditional_repetition']))
check('neither one-period mandate renews itself',all(cases[k]['first_separate_finance_failure_before_foreign_stress_stops']==2 for k in ['base_bonds','base_finite_issue']))
check('insufficient accepted bond offer defeats settlement',cases['insufficient_bond_offer']['first_separate_finance_failure_before_foreign_stress_stops']==1)
check('base foreign runoff period4',cases['base_bonds']['first_foreign_stock_or_gross_limit_failure_in_conditional_repetition']==4)
check('worse exports can lower domestic finance while worsening foreign resilience',q(cases['export_receipt_shock']['new_public_domestic_claims_needed_u'])<120 and cases['export_receipt_shock']['first_foreign_stock_or_gross_limit_failure_in_conditional_repetition']==3)
check('FX repricing harms private resources while cash requirement falls',q(cases['direct_FX_repricing']['household_net_financial_lending_u'])==70 and q(cases['direct_FX_repricing']['firm_and_financial_sector_net_financial_lending_u'])==35 and q(cases['direct_FX_repricing']['new_public_domestic_claims_needed_u'])==105)
check('private offer matters to public-owned stock',cases['private_surplus_not_offered']['first_foreign_stock_or_gross_limit_failure_in_conditional_repetition']==5 and cases['private_surplus_voluntarily_offered']['first_foreign_stock_or_gross_limit_failure_in_conditional_repetition'] is None)
long=deepcopy(cfg);long['repeat_periods_for_conditional_foreign_stress']=10;longcase={x['id']:x for x in model.compute(long)['cases']}
check('six-period survival is not perpetual capacity',longcase['private_surplus_voluntarily_offered']['first_foreign_stock_or_gross_limit_failure_in_conditional_repetition']==10)
empty=deepcopy(cfg['scenarios'][0]);empty['public_owned_opening_f']='0';empty['public_floor_f']='0';check('no public title defeats first foreign payment',model.circuit(cfg,empty)['first_foreign_stock_or_gross_limit_failure_in_conditional_repetition']==1)
capped=deepcopy(cfg['scenarios'][0]);capped['gross_annual_public_sale_cap_f']='20';check('ample stock does not create gross legal headroom',model.circuit(cfg,capped)['first_foreign_stock_or_gross_limit_failure_in_conditional_repetition']==1)
for label,mutate in [('unknown future meaning',lambda c:c.update(future_context={'unmapped':True})),('new unrecognized transaction',lambda c:c['flows'].update(private_work='unmapped')),('unsupported fiscal authority',lambda c:c['scenarios'][0].update(finance='AI_approved')),('negative owned stock',lambda c:c['scenarios'][0].update(public_owned_opening_f='-1'))]:
 bad=deepcopy(cfg);mutate(bad)
 try:model.compute(bad)
 except ValueError:check('uninterpreted inputs rejected:'+label,True)
 else:raise AssertionError(label)
check('no invented actual national source',result['actual_country_net_borrowing_or_output_or_ready_source'] is None)
proc=subprocess.run([sys.executable,str(R.parent/'scripts/check-research-structure.py')],text=True,capture_output=True);check('current organization/links',proc.returncode==0)
report={'edition':133,'status':'pass','substantive_checks':sum(not n.startswith(('snapshot:','pin:')) for n in checks),'predecessor_artifacts':1024,'source_pins':len(pins['sha256']),'structure':proc.stdout.strip(),'scope':'Exact predecessor/current-input preservation and independent authored sector/holder/FX/authority arithmetic plus adverse cases. Not country deficit/output/tax/saving forecasts, full statistical accounting, actual title/mandate, inflation, qualified independent delivery or better lives.'}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
