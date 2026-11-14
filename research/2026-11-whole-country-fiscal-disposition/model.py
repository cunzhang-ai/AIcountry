"""Historical required-cash account views, not a complete fiscal/expense forecast."""
from pathlib import Path
from decimal import Decimal as Q,localcontext
from datetime import date
import json
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text())
def q(x):
 if x is None or isinstance(x,bool):raise ValueError('explicit finite monetary quantity required')
 v=Q(str(x))
 if not v.is_finite():raise ValueError('finite monetary quantity required')
 return v

def analyze(case,cfg):
 events=case['cash_required_not_paid']['events'];classes=cfg['event_classes'];year=cfg['year'];this=[];later=[];counts={};unresolved=0
 for index,e in enumerate(events):
  if set(e)!={'date','from','to','CU','kind'} or e['kind'] not in classes:raise ValueError('unmapped event meaning')
  if any(not isinstance(e[k],str) or not e[k] for k in ['from','to','kind']):raise ValueError('explicit parties and event meaning required')
  when=date.fromisoformat(e['date']);amount=q(e['CU'])
  if amount<0:raise ValueError('negative directed amount')
  if when.year<year:raise ValueError('unmapped prior-period event')
  row={**e,'ordinal':index,'class':classes[e['kind']]};(this if when.year==year else later).append(row);counts[e['kind']]=counts.get(e['kind'],0)+1
  if row['class']=='unresolved_supplier_or_service_prepay' and when.year==year:unresolved+=1
 opening=read(R/cfg['opening_source'])['opening_CU'];views={}
 with localcontext() as ctx:
  ctx.prec=50
  for name,accounts in cfg['account_sets'].items():
   inside=set(accounts)
   if len(inside)!=len(accounts):raise ValueError('duplicate account in reporting boundary')
   start=sum((q(opening.get(a,0)) for a in inside),Q(0));incoming=Q(0);outgoing=Q(0);internal=Q(0);aggregate_delta=Q(0);categories={}
   for e in this:
    amount=q(e['CU']);src=e['from'] in inside;dst=e['to'] in inside
    if src and dst:internal+=amount
    if dst and not src:incoming+=amount
    if src and not dst:outgoing+=amount
    aggregate_delta+=amount*int(dst)-amount*int(src)
    if src or dst:
     c=categories.setdefault(e['class'],{'gross_from_accounts':Q(0),'gross_to_accounts':Q(0),'internal':Q(0)})
     c['gross_from_accounts']+=amount*int(src);c['gross_to_accounts']+=amount*int(dst);c['internal']+=amount*int(src and dst)
   views[name]={'accounts':accounts,'opening_modeled_CU':str(start),'external_conditional_receipts':str(incoming),'external_required_outflows':str(outgoing),'internal_equal_in_out':str(internal),'sum_of_account_changes':str(aggregate_delta),'external_net_change':str(incoming-outgoing),'elimination_residue':str(aggregate_delta-incoming+outgoing),'closing_required_position_not_owned_available_cash':str(start+incoming-outgoing),'categories':{k:{a:str(v) for a,v in z.items()} for k,z in categories.items()},'actual_available_source_or_legal_sweep':None}
  balances={}
  for a in set(z for v in cfg['account_sets'].values() for z in v):
   delta=sum((q(e['CU'])*(int(e['to']==a)-int(e['from']==a)) for e in this),Q(0));balances[a]=str(q(opening.get(a,0))+delta)
  G=views['G_only'];gross_by_kind={}
  for e in this:
   if e['from']!='G' and e['to']!='G':continue
   z=gross_by_kind.setdefault(e['kind'],{'class':e['class'],'from_G':Q(0),'to_G':Q(0),'count':0});z['from_G']+=q(e['CU'])*(e['from']=='G');z['to_G']+=q(e['CU'])*(e['to']=='G');z['count']+=1
  gross_by_kind={k:{a:str(v) if isinstance(v,Q) else v for a,v in z.items()} for k,z in gross_by_kind.items()}
 return {'id':case['assumptions']['id'],'source_year':year,'all_event_count':len(events),'year_event_count':len(this),'later_known_only_event_count':len(later),'later_kind_counts':{k:sum(e['kind']==k for e in later) for k in sorted({e['kind'] for e in later})},'all_kind_counts':counts,'stress_people_without_ordinary_private_work_recipe':case['personal']['unsupplied_resource_stress_people'],'account_views':views,'yearend_individual_required_positions':balances,'G_gross_by_kind':gross_by_kind,'unresolved_prepayment_event_count':unresolved,'legacy_reported_G_closing':case['cash_required_not_paid']['yearend_before_next_due']['G'],'legacy_peak_G_source_stress_not_deficit':case['cash_required_not_paid']['peak_additional_source_over_required_accounts_CU']['G'],'actual_complete_revenue_expense_capital_financing_or_additional_tax':None,'actual_full_recurring_gap_or_country_readiness':None,'actual_source_legal_authority_or_better_lives':None}

def compute(config=None):
 saved=read(D/'inputs.json');cfg=saved if config is None else config
 if set(cfg)!=set(saved) or cfg['edition']!=138 or cfg['year']!=2030 or cfg['context']!=saved['context'] or cfg['opening_source']!=saved['opening_source'] or cfg['event_classes']!=saved['event_classes'] or cfg['account_sets']!=saved['account_sets'] or cfg['cases']!=saved['cases']:raise ValueError('unmapped context/boundary or unreviewed source change')
 coverage=read(D/'source-coverage.json')
 if set(coverage)!={'edition','meaning','rows'} or coverage['edition']!=138:raise ValueError('unmapped source scope')
 for r in coverage['rows']:
  if set(r)!={'id','diagnostic_coverage','canonical','required_scope','actual_full_base_amount_source_dates_and_receiving'} or r['actual_full_base_amount_source_dates_and_receiving'] is not None:raise ValueError('unreviewed source qualification')
 return {'edition':138,'context':cfg['context'],'source_interface_count':len(coverage['rows']),'source_actual_full_amounts_unknown':[r['id'] for r in coverage['rows'] if r['actual_full_base_amount_source_dates_and_receiving'] is None],'cases':[analyze(read(R/e['path']),cfg) for e in cfg['cases']],'research_disposition':'Retain service-first individual guarantee and recurring-tax/insurance/bounded-debt architecture; retire 130/131 scale/dated book as selected national financial reference, retain diagnostics and old rights. No invented yield or cut.','actual_complete_country_fiscal_package':None}
if __name__=='__main__':(D/'results.json').write_text(json.dumps(compute(),indent=2)+'\n')
