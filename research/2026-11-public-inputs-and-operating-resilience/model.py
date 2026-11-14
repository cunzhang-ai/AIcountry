"""Finite purchase boundary and abstract receipt/expiry/common-node counterexamples."""
from pathlib import Path
from decimal import Decimal as Q
import json
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text())
def q(x):
 if x is None or isinstance(x,bool):raise ValueError('explicit nonnegative finite quantity required')
 v=Q(str(x))
 if not v.is_finite() or v<0:raise ValueError('explicit nonnegative finite quantity required')
 return v
def integer(x):
 if type(x) is not int:raise ValueError('whole day required')
 return x

def inventory_case(row):
 expected={'id','daily_requirement_units','batches','routes','failed_nodes','finance'}
 if set(row)!=expected:raise ValueError('unmapped future supply semantics')
 if not row['daily_requirement_units']:raise ValueError('bounded horizon required')
 demand=[q(z) for z in row['daily_requirement_units']];lots=[];ids=[];received=Q(0);blocked=[]
 for z in row['batches']:
  if set(z)!={'id','quantity','usable_from_day','usable_through_day','status'} or z['status'] not in ['accepted','pending','recalled']:raise ValueError('unmapped lot qualification')
  integer(z['usable_from_day']);integer(z['usable_through_day'])
  if z['usable_from_day']!=0:raise ValueError('opening physical stock must be present at day0')
  qty=q(z['quantity']);received+=qty;lots.append({**z,'quantity':qty});ids.append(z['id'])
 if len(ids)!=len(set(ids)):raise ValueError('duplicate opening batch')
 opening=received;routeids=[];nodes=set()
 for z in row['routes']:
  if set(z)!={'id','dependency_nodes','arrival_day','quantity','usable_through_day','assumed_qualified'} or type(z['assumed_qualified']) is not bool:raise ValueError('unmapped route qualification')
  if not z['dependency_nodes'] or len(z['dependency_nodes'])!=len(set(z['dependency_nodes'])):raise ValueError('explicit unique dependency nodes required')
  nodes.update(z['dependency_nodes']);routeids.append(z['id']);integer(z['arrival_day']);integer(z['usable_through_day']);q(z['quantity'])
  if not (0<=z['arrival_day']<len(demand)) or z['usable_through_day']<z['arrival_day']:raise ValueError('out-of-scope or expired route')
 if len(routeids)!=len(set(routeids)) or any('delivery:'+z in ids for z in routeids):raise ValueError('duplicate route/delivery identity')
 if not set(row['failed_nodes'])<=nodes:raise ValueError('unmapped failed node')
 served=Q(0);logs=[]
 for day,need in enumerate(demand):
  for z in row['routes']:
   if z['arrival_day']!=day:continue
   if not z['assumed_qualified'] or set(z['dependency_nodes'])&set(row['failed_nodes']):blocked.append(z['id']);continue
   qty=q(z['quantity']);received+=qty;lots.append({'id':'delivery:'+z['id'],'quantity':qty,'usable_from_day':day,'usable_through_day':z['usable_through_day'],'status':'accepted'})
  available=sum(z['quantity'] for z in lots if z['status']=='accepted' and z['usable_from_day']<=day<=z['usable_through_day'])
  left=need;used=[]
  for z in sorted(lots,key=lambda z:(z['usable_through_day'],z['id'])):
   if z['status']!='accepted' or not(z['usable_from_day']<=day<=z['usable_through_day']):continue
   take=min(left,z['quantity']);z['quantity']-=take;left-=take
   if take:used.append({'batch':z['id'],'units':str(take)})
  served+=need-left;logs.append({'day':day,'usable_before_issue':str(available),'requirement':str(need),'served':str(need-left),'unmet':str(left),'issued':used})
 held=sum(z['quantity'] for z in lots);last=len(demand)-1
 expired=sum(z['quantity'] for z in lots if z['status']=='accepted' and z['usable_through_day']<last)
 otherheld=sum(z['quantity'] for z in lots if z['status']!='accepted')
 f=row['finance']
 if set(f)!={'due_currency','gross_due','source_currency','assumed_owned_source_amount','actual_received_source'}:raise ValueError('unmapped funding ownership or source')
 if f['due_currency'] not in ['CU','FU'] or f['source_currency'] not in ['CU','FU']:raise ValueError('uninterpreted currency')
 due=q(f['gross_due']);source=q(f['assumed_owned_source_amount'])
 if f['actual_received_source'] is not None:q(f['actual_received_source'])
 gap=max(Q(0),due-source) if f['due_currency']==f['source_currency'] else None
 return {'id':row['id'],'opening_physical_units':str(opening),'conditional_received_units':str(received),'daily':logs,'served_units':str(served),'unmet_units':str(sum(demand)-served),'held_units_not_disposed':str(held),'expired_held_units':str(expired),'pending_or_recalled_held_units':str(otherheld),'physical_conservation_residue':str(received-served-held),'blocked_routes':blocked,'same_currency_hypothetical_source_gap':None if gap is None else str(gap),'unconverted_source_currency':f['source_currency'] if gap is None else None,'actual_received_source':f['actual_received_source'],'actual_safe_clinical_receipt_or_funded_operation':None}

def compute(config=None,register=None):
 cfg=read(D/'inputs.json') if config is None else config
 if set(cfg)!={'edition','context','register','cases'} or cfg['edition']!=137 or cfg['register']!='input-register.json' or cfg['context']!='Authored abstract critical-input units and CU/FU finance counterexamples, not clinical doses, medicine forecasts, suppliers or prices':raise ValueError('unmapped context or foreign calibration')
 reg=read(D/cfg['register']) if register is None else register
 if set(reg)!={'edition','context','rows','meaning'} or reg['edition']!=137 or reg['context']!='Same 130 firm/plural/A purchase-row scope as132; authored CU quotes, not demand or current adequate prices' or reg['meaning']!='Families organize inquiry, not disjoint actual resources or qualifications. All later duties continue; this is no national catalogue.':raise ValueError('unmapped register semantics')
 rows=reg['rows'];old=read(R/'2026-11-public-supply-and-procurement/results.json')['public_purchase_scope']
 families={'clinical_products','specialist_care_and_employer_support','fuel','equipment_materials_and_repairs','sanitation_environment_and_testing','knowledge_digital_and_protected_sources','purchased_independent_expertise','access_notices_and_democratic_materials','care_custody_and_external_support','linked_food','linked_utilities','linked_housing_programme'}
 known={'id','function_owner','named_allocation_CU','prior_coverage','primary_analysis_family','actual_item_service_quantity_or_receiving_scope','actual_upstream_capacity_and_shared_dependencies','actual_labor_lifecycle_source_and_owned_FX','actual_qualified_usable_receipt_or_buffer','actual_funded_transition_and_successor'}
 prior={z['id']:z for z in old['rows']}
 for z in rows:
  if set(z)!=known or z['primary_analysis_family'] not in families:raise ValueError('unmapped item/service meaning')
  if z['id'] not in prior or any(z[k]!=prior[z['id']][k] for k in ['function_owner','named_allocation_CU']) or z['prior_coverage']!=prior[z['id']]['coverage']:raise ValueError('changed retained scope or quote')
  if any(v is not None for k,v in z.items() if k.startswith('actual_')):raise ValueError('actual evidence requires new scoped review')
 if len(rows)!=66 or len({z['id'] for z in rows})!=66:raise ValueError('changed purchase denominator')
 groups={}
 for z in rows:
  family=z['primary_analysis_family'];groups.setdefault(family,{'count':0,'named_quote_CU':Q(0)});groups[family]['count']+=1;groups[family]['named_quote_CU']+=q(z['named_allocation_CU'])
 groups={k:{'count':v['count'],'named_quote_CU':str(v['named_quote_CU'])} for k,v in groups.items()}
 if len({c['id'] for c in cfg['cases']})!=len(cfg['cases']):raise ValueError('duplicate scenario')
 return {'edition':137,'register_summary':{'count':len(rows),'primary_analysis_families':groups,'named_total_CU':str(sum(q(z['named_allocation_CU']) for z in rows)),'previous_unmatched_quote_CU_not_new_cost':old['remaining_budget_or_task_scope_CU'],'six_clinical_legacy_quote_CU_not_adequacy':old['six_clinical_budget_rows_CU'],'actual_matched_current_recipes_sources_or_receipts':None},'counterexamples':[inventory_case(z) for z in cfg['cases']],'country_selection':'Retain public critical-input competence and accountable plural procurement, conditional nonexclusive pooling, qualified usable buffers and paid alternative routes; reject clinical budget quotes as adequate source prices. No assumed foreign access or domestic self-sufficiency.','actual_full_country_cost_authority_capacity_or_better_lives':None}
if __name__=='__main__':(D/'results.json').write_text(json.dumps(compute(),indent=2)+'\n')
