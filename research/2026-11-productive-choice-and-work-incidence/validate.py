"""Finite preservation, changed-scope arithmetic and adverse checks; no social certification."""
from pathlib import Path
from decimal import Decimal as Q
from copy import deepcopy
import hashlib, json, subprocess, sys
import model

D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text())
q=lambda x:Q(str(x))
checks=[]
def check(label,condition):
    if not condition:raise AssertionError(label)
    checks.append(label)
def equal(a,b):return abs(q(a)-q(b))<q('.00000001')

baseline=read(D/'baseline.json')
check('1007 exact predecessor artifacts retained',len(baseline['sha256'])==1007)
for n,h in baseline['sha256'].items():
    check('predecessor:'+n,hashlib.sha256((D/'predecessor-design-130'/n).read_bytes()).hexdigest()==h)
pins=read(D/'source-manifest.json')
for n,h in pins['sha256'].items():check('source:'+n,hashlib.sha256((R/n).read_bytes()).hexdigest()==h)
old=read(D/'predecessor-design-130/settlement/commitments/inventory.json')
now=read(R/'settlement/commitments/inventory.json')
check('37 original function objects exactly retained',now['functions']==old['functions'] and len(now['functions'])==37)
check('61 original selections exactly retained',now['selections']==old['selections'] and len(now['selections'])==61)
refs={k:v for k,v in old.items() if k.endswith('_reference')}
check('70 inherited reference objects exactly retained',len(refs)==70 and all(now[k]==v for k,v in refs.items()))
for n in ['FRAMEWORK.md','DECISION-TEMPLATE.md']:
    check('common method unchanged:'+n,(R/n).read_bytes()==(D/'predecessor-design-130'/n).read_bytes())

fresh,cases=model.compute()
stored=read(D/'results.json')
check('results reproduce with fresh computations',{k:v for k,v in stored.items() if k!='country_C2_cases'}==fresh)
check('four current C2 cases',len(cases)==4 and len(fresh['country_C2_summaries'])==4)
for name,c in cases.items():
    check('fresh full case:'+name,read(D/'cases'/name)==c)
    prior=read(model.BASE/'cases'/name.replace('_C2','_U'))
    check('public and physical interfaces unchanged:'+name,all(c[k]==prior[k] for k in ['public_book','function_rows','supply','household_prices','source_calls','tax_scope']))
    check('all function full-cost/source fields unknown:'+name,all(x['actual_full_current_cost'] is None and x['actual_owned_source_or_received_remedy'] is None for x in c['function_rows']))
    check('population and unprovided resources unchanged:'+name,c['personal']['population']==100000 and c['personal']['unsupplied_resource_stress_people']==prior['personal']['unsupplied_resource_stress_people'])
    check('no source certificate:'+name,c['actual_complete_financed_country_or_safe_receiving'] is None and c['cash_required_not_paid']['first_unfunded_date']['G']=='2030-01-01')
    a=prior['personal']['totals'];b=c['personal']['totals']
    check('U/Y/I05/earnings held in current cases:'+name,all(equal(a[k],b[k]) for k in ['I05','nonolder_U','Y_basic','insurance_gross','Y_withheld','worked_gross_due','worked_gross_received']))
    check('C2 tax equals same-function A tax:'+name,equal(b['PA_assessed'],read(model.BASE/'cases'/name.replace('_C2','_I05'))['personal']['totals']['PA_assessed']))

for r in fresh['country_C2_summaries']:
    check('larger unfunded incidence disclosed:'+r['case'],q('17150400')<=q(r['additional_net_G_annual_personal_incidence_CU'])<=q('17245440'))

def retention(wage,package,extra=Q(30000)):
    a=model.person(Q(wage),package,Q(6000),extra)
    b=model.person(Q(wage)+1,package,Q(6000),extra)
    return b['cash_after_named_housing_and_extra']-a['cash_after_named_housing_and_extra']
check('old active-I05 severe wedge reproduced',equal(retention(60000,'C1'),'.1665'))
check('C2 improves that particular wedge',equal(retention(60000,'C2'),'.2475'))
check('remaining C2 active-I05 high-band burden exposed',equal(retention(120000,'C2'),'.2025'))
for wage in [0,1000,10000,30000,40000,50000,60000,80000,120000,1000000]:
    check('A and C2 same allowance/transition function:'+str(wage),model.tax(Q(wage),'A')==model.tax(Q(wage),'C2'))
    for p in ['A','C1','C2']:
        unpaid=model.person(Q(wage),p,Q(6000),received=Q(0))
        check('unreceived wages no Y/tax/means:'+p+str(wage),unpaid['Y']==0 and unpaid['PA']==0 and unpaid['cash_after_named_housing_and_extra']==13248)
for package in ['A','C1','C2']:
    for boundary in [12000,27000,30000,42000,60000,72000]:
        # Near each allowance/band boundary: no finite jump hidden by annual rounding.
        left=model.tax(Q(boundary)-q('.0001'),package);right=model.tax(Q(boundary)+q('.0001'),package)
        check('continuous monotone tax:'+package+str(boundary),0<=right-left<=q('.0002'))

offers=fresh['garment_offers'];check('two recipes by two direct-FX by three paid-demand cases',len(offers)==12)
for row in offers:
    name=row['choice']+'/'+row['CU_per_FU']+'/'+row['demand_fraction']
    check('same age-weighted quantity:'+name,q(row['reference_items_not_orders'])==1213200)
    revenue=q(row['performance_revenue_exVAT']);variable=q(row['variable_inputs_exVAT']);fixed=q(row['fixed_cost_exVAT']);profit=q(row['profit_before_company_tax'])
    check('buyer cost and producer performance match:'+name,equal(revenue,q(row['sold_if_demand_is_paid'])*q(row['consumer_unit_offer_incVAT'])/q('1.1')))
    check('named profit identity:'+name,equal(revenue-variable-fixed,profit))
    check('next-April tax never on a loss:'+name,equal(row['company_assessment_due_next_April'],max(Q(0),profit)*q('.25')))
    check('retained profit distinct from tax and personal income:'+name,equal(row['after_company_profit_or_loss_retained_not_personal_income'],profit-q(row['company_assessment_due_next_April'])))
    recipe=model.read(D/'inputs.json')['garment_recipes'][row['choice']]
    expected_asset=q(recipe['new_asset_CU'])+q(row['capital_import_FU_included_in_asset_quote'])*(q(row['CU_per_FU'])-1)
    check('capital import not added twice:'+name,equal(row['initial_capital_stock_CU'],expected_asset))
    check('actual output/source/physical fit remains unqualified:'+name,row['actual_orders_staff_title_finance_owned_FX_or_received_refunds'] is None and row['whole_country_source_increment_or_net_physical_change'] is None)
    if q(row['demand_fraction'])==q('.6'):
        check('lower demand exposes loss and cash shortfall:'+name,profit<0 and q(row['operating_cash_before_stock_capital_VAT_and_distributions'])<0)
    if q(row['demand_fraction'])>1:
        check('excess demand cannot manufacture capacity:'+name,q(row['sold_if_demand_is_paid'])==q(row['capacity_items']) and equal(row['unserved_if_demand_exceeds_capacity'],q(row['capacity_items'])*q('.2')))
for choice in ['local_making_and_retail','finished_import_and_retail']:
    rows=[x for x in offers if x['choice']==choice]
    check('wage/worker dues survive demand fall:'+choice,len({(x['worker_posts_not_actual_hires'],x['annual_gross_pay_due']) for x in rows})==1)
    base=next(x for x in rows if q(x['CU_per_FU'])==1 and q(x['demand_fraction'])==1)
    dear=next(x for x in rows if q(x['CU_per_FU'])==q('1.5') and q(x['demand_fraction'])==1)
    check('direct foreign price affects capital/offer:'+choice,q(dear['initial_capital_stock_CU'])>q(base['initial_capital_stock_CU']) and q(dear['consumer_unit_offer_incVAT'])>q(base['consumer_unit_offer_incVAT']))

cfg=read(D/'inputs.json')
for label,mutate in [('unknown top-level concept',lambda x:x.update(unfamiliar_future_media={'meaning':'retain for review'})),('unknown recipe concept',lambda x:x['garment_recipes']['local_making_and_retail'].update(shared_situation='uninterpreted')),('unqualified actual observations',lambda x:x.update(actual_observed_recipes_or_qualified_buyers='observed'))]:
    bad=deepcopy(cfg);mutate(bad)
    try:model.compute(False,bad)
    except ValueError:check('unsupported semantics rejected without source deletion:'+label,True)
    else:raise AssertionError(label)

result=subprocess.run([sys.executable,str(R.parent/'scripts/check-research-structure.py')],capture_output=True,text=True)
check('current organization and links',result.returncode==0)
report={'edition':131,'status':'pass','bounded_assertions':len(checks),'substantive_assertions_excluding_hashes':len([x for x in checks if not x.startswith(('predecessor:','source:'))]),'predecessor_artifacts':1007,'source_pins':len(pins['sha256']),'structure':result.stdout.strip(),'scope':'Preservation, fresh fixed-price C2/current A equality and person/source identities, authored partial producer/direct-FX/demand/loss and semantic-rejection checks. Not calibrated output, actual source/tax yield, authority, affected/independent judgment, safe paid capacity or better lives.'}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
