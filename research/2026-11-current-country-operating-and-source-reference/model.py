"""Source-conditioned current country reference: compatible replacements do not prove a financed nation."""
from pathlib import Path
from decimal import Decimal as Q
from copy import deepcopy
import json,hashlib
from supply import compute as supply_compute
from book import build as book_build,q
from households import reprice,extra_people
from people import compute as people_compute
from cash import compute as cash_compute
from sources_schedule import compute as schedule_compute
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text())
def clean(v):
 if isinstance(v,Q):return str(v)
 if isinstance(v,dict):return {k:clean(a) for k,a in v.items()}
 if isinstance(v,list):return [clean(a) for a in v]
 return v
def matches(v,s):
 if 'dict' in s:return type(v) is dict and set(v)==set(s['dict']) and all(matches(v[k],a) for k,a in s['dict'].items())
 if 'list' in s:return type(v) is list and all(matches(a,s['list']) for a in v)
 if 'null' in s:return v is None
 return type(v).__name__==s['type']
def compute(cfg):
 if not matches(cfg,read(D/'input-shape.json')):raise ValueError('Unknown or missing future concepts need scoped interpretation, not omission')
 def unknown(v):
  if type(v) is dict:return all((a is None if k.startswith('actual_') else unknown(a)) for k,a in v.items())
  if type(v) is list:return all(unknown(a) for a in v)
  return True
 if cfg['edition']!=130 or cfg['year']!=2030 or not unknown(cfg):raise ValueError('No actual country/authority/source classifier supplied')
 if cfg['local_cash_advance_mode'] not in ['bounded_first_receipt','none']:raise ValueError('Uninterpreted local financing permission')
 if cfg['housing_reserve_funding_timing'] not in ['quarter_start','month_end']:raise ValueError('Uninterpreted funding calendar')
 for value in [cfg['private_wage_received_fraction'],cfg['station_baseline_compatible_fraction_hypothesis'],cfg['public_input_credit_fraction_hypothesis'],*cfg['food_VAT_sensitivity_by_product'].values()]:
  if not 0<=q(value)<=1:raise ValueError('Invalid hypothesis fraction')
 if any(q(cfg['food_VAT_sensitivity_by_product'][k])!=0 for k in ['cereals','roots','vegetables','fruit','pulses','nuts']):raise ValueError('Known plain-food zero-rate scope cannot silently become a new tax')
 if not 0<=q(cfg['finance']['new_capital_interest'])<1 or cfg['finance']['equal_principal_years']<=0:raise ValueError('Invalid financing sensitivity')
 contract=read(D/'source-contract.json')
 if cfg['sources']!=contract['paths'] or any(hashlib.sha256((R/n).read_bytes()).hexdigest()!=h for n,h in contract['sha256'].items()):raise ValueError('Changed supporting source needs fresh dependency-scope review')
 functions=read(R/'settlement/commitments/inventory.json')['functions']
 if hashlib.sha256(json.dumps(functions,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=contract['original_complete_functions_sha256']:raise ValueError('Changed country functions need explicit denominator and obligation reconciliation')
 src={k:read(R/n) for k,n in cfg['sources'].items()};pub=src['public_results'];pubinputs=src['public_inputs'];pers=deepcopy(src['personal_inputs']);pers['local_teacher_component_ids'].append('labor:local_elected_roles');pb=src['household_inputs'];pbr=src['household_results'];pin=src['physical_inputs'];pr=src['physical_results'];er=src['election_results'];ein=src['election_inputs'];housing=src['housing_results']['housing_integer_peak_corrected_quote'];hin=src['housing_inputs']
 if [pub['edition'],pers['edition'],pbr['edition'],pr['edition'],er['edition']]!=[125,126,124,127,128]:raise ValueError('Changed source editions require fresh compatible-scope review')
 if set(cfg['physical_cases'])!={'water_limited/firm_seven_extended','water_limited/storage_extended'} or len(cfg['physical_cases'])!=2 or set(cfg['service_cases'])!=set(pub['service_cases']) or len(cfg['service_cases'])!=2 or set(cfg['packages'])!={'A','C1'} or len(cfg['packages'])!=2:raise ValueError('Changed comparative scope requires explicit rights/source reconciliation')
 if cfg['helper_case']!='prospective_wholeposts' or set(cfg['food_VAT_sensitivity_by_product'])!=set(pin['food']['products']):raise ValueError('Uninterpreted helper/product scope')
 baseline=sum(q(r['paid_role_equivalents']) for r in read(R/pubinputs['public_base'])['cases']['A']['labor_components'] if r['family']=='QE_named_current_demand');cases={}
 for physical_case in cfg['physical_cases']:
  ph=pr['cases'][physical_case];supply=supply_compute(cfg,ph,pin,housing,hin,pub,pb);newpb,newpbr,private,houseprice=reprice(cfg,pb,pbr,supply,ph,pin,pub);extra=extra_people(cfg,ph,pin,housing,pub)
  for service_case in cfg['service_cases']:
   book=book_build(cfg,{**pub['service_cases'][service_case],'case_name':service_case},er,ein,supply,pubinputs,baseline);services={**pub,'service_cases':{service_case:book},'private_learning_and_reprice':private,'unused_goods':newpbr['goods_base'],'housing_reserve_funding_timing':cfg['housing_reserve_funding_timing'],'local_cash_advance_mode':cfg['local_cash_advance_mode']}
   for package in cfg['packages']:
    label=physical_case+'/'+service_case+'/'+package;case={'id':label,'service':service_case,'package':package,'helper':cfg['helper_case'],'private_wage_received_fraction':cfg['private_wage_received_fraction'],'higher_prior_units':cfg['higher_prior_units_hypothesis'],'net_makewhole_hypothesis':cfg['net_makewhole_hypothesis']};personal=people_compute(pers,case,services,newpb,newpbr,extra);pcfg=deepcopy(pers);pcfg['opening_CU'].update(Renewal_housing_G=0,Renewal_other_G=0,Continuing_scope_G=0);cash=cash_compute(pcfg,case,personal,services,False)
    frows=[]
    for function in functions:
     rr=[r for r in book['component_rows'] if r['owner']==function['id']];frows.append({'id':function['id'],'function':function['function'],'components':[r['id'] for r in rr],'named_current_allocation_CU':str(sum(q(r['named_allocation_CU']) for r in rr)),'actual_full_current_cost':None,'actual_owned_source_or_received_remedy':None})
    vat={'food_consumer_output_sensitivity_CU':supply['bills']['private_food_consumer_VAT_sensitivity_CU']-supply['bills']['private_food_exVAT_CU'],'actual_net_VAT_yield_input_refund_company_or_transfer_source':None};cases[label]={'assumptions':case,'public_book':book,'function_rows':frows,'supply':supply,'personal':personal,'cash_required_not_paid':cash,'household_prices':{'named_component_quotes_CU':newpbr['ordinary']['per_person_component_quotes_CU'],'protected_B_used':personal['B'],'unmapped_adequacy_or_due_replacement':None,'helper_customer_unit_CU':private[cfg['helper_case']]['new_helper_customer_unit_CU'],'goods_with_instruction':private[cfg['helper_case']]['repriced_retail_with_learning'],**houseprice},'source_calls':schedule_compute(supply,ph,book,newpbr,cfg),'tax_scope':vat,'actual_complete_financed_country_or_safe_receiving':None}
 return clean({'edition':130,'format_revision':'130-current-country-v1','component_semantics':{'staff':'Paid annual-role equivalents and distinct-person requirements differ; actual workers are unqualified.','purchase':'Named quoted supplier/direct nonpay call, not proof of receipt.','asset':'Separate capital stock quote, annual upkeep and renewal reservation; not a second capital purchase.','reservation':'Earmarked proposed renewal formation, with separate actual eligible draws.','hold':'Unmatched part of a previous provision envelope; not invoice, saving, actual liability or permanent spending right.'},'date':'2026-11-03','scope':cfg['scope'],'cases':cases,'unpriced_current_scope':['Actual original observations, adequate B/clinical/nutritional quality, chosen needs, private other income/production/buyers/profits and current full taxable bases.','Housing title, programme/other/input/capital classification, old upkeep overlap, professional safety and full continuing debt/pension/foreign claims.','Working capital, supplier acceptance, paid input VAT/refunds, actual financing and owned foreign currencies, facilities/access/transition overlap and all later duties.','Actual simultaneous independent rosters, useful-time courts/elections/receiving, legitimate affected authority and better lives.'],'actual_national_GDP_full_cost_deficit_or_source_yield':None,'actual_independent_or_affected_authority':None,'actual_ready_country_or_better_lives':None})
def write_results(x):
 (D/'cases').mkdir(exist_ok=True);index={k:v for k,v in x.items() if k!='cases'};index['cases']={}
 for label,c in x['cases'].items():
  name=('firm' if 'firm_seven' in label else 'storage')+'_'+('plural' if 'plural_public' in label else 'direct')+'_'+('I05' if c['assumptions']['package']=='A' else 'U')+'.json';path='cases/'+name;(D/path).write_text(json.dumps(c,indent=2)+'\n');index['cases'][label]={'artifact':path,'summary':{'named_public_allocation_CU':c['public_book']['named_annual_allocation_CU'],'held_unmatched_scope_CU':c['public_book']['continuing_scope_reservation_CU'],'I05_CU':c['personal']['totals']['I05'],'nonolder_U_CU':c['personal']['totals']['nonolder_U'],'first_unfunded_G_date_in_named_stress':c['cash_required_not_paid']['first_unfunded_date']['G'],'actual_complete_country':None}}
 (D/'results.json').write_text(json.dumps(index,indent=2)+'\n')
def read_results():
 x=read(D/'results.json');return {**x,'cases':{k:read(D/v['artifact']) for k,v in x['cases'].items()}}
if __name__=='__main__':write_results(compute(read(D/'inputs.json')))
