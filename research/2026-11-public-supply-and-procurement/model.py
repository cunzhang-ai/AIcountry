"""Finite current-input coverage and proposed procurement-clock counterexamples."""
from pathlib import Path
from decimal import Decimal as Q
from datetime import date, timedelta
import json
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text())
q=lambda x:Q(str(x))
LINKED={
 'op:national_service_electricity':'130 supply/public meter; not executed purchase',
 'op:national_service_water':'130 supply/public meter; not executed purchase',
 'op:current_institutional_ingredients':'127/130 literal food/scope allocation; not accepted quality or source',
 'op:current_public_housing_programme':'130 repair/rebuild attribution; not verified material recipe or paid supplier'}
CLINICAL={'op:medicines_devices','op:laboratory_reagents','op:imaging_consumables','op:theatre_supplies','op:health_hygiene','op:care_supplies'}

def clean(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,list):return [clean(v) for v in x]
 return x

def working_after(start,n,holidays=()):
 current=date.fromisoformat(start);closed={date.fromisoformat(x) for x in holidays}
 for _ in range(n):
  current+=timedelta(days=1)
  while current.weekday()>4 or current in closed:current+=timedelta(days=1)
 return current.isoformat()

def procurement_case(cfg):
 expected={'id','M','related_expected_gross_commitments','usable_notice','usable_award_notice','unresolved_timely_challenge','urgency','holiday_dates'}
 if set(cfg)!=expected:raise ValueError('Uninterpreted future procurement meaning; preserve for scoped review')
 if cfg['urgency'] not in ['ordinary','separately_authorized_continuity']:raise ValueError('Unsupported exception is not authority')
 if q(cfg['M'])<=0 or any(q(x)<0 for x in cfg['related_expected_gross_commitments']):raise ValueError('Invalid unit or commitment')
 gross=sum(q(x) for x in cfg['related_expected_gross_commitments']);material=gross>=5*q(cfg['M'])
 notice=date.fromisoformat(cfg['usable_notice']);micro=gross<q('.5')*q(cfg['M'])
 earliest_bid=(notice+timedelta(days=30)).isoformat() if material else cfg['usable_notice'] if micro else working_after(cfg['usable_notice'],5,cfg['holiday_dates'])
 if date.fromisoformat(cfg['usable_award_notice'])<date.fromisoformat(earliest_bid):raise ValueError('Award cannot precede the bid opportunity')
 end=working_after(cfg['usable_award_notice'],10,cfg['holiday_dates']) if material else None
 eligible_award=(date.fromisoformat(end)+timedelta(days=1)).isoformat() if end else cfg['usable_award_notice']
 if cfg['unresolved_timely_challenge']:eligible_award=None
 return {'id':cfg['id'],'aggregated_gross_commitment_CU':gross,'material':material,'micro':micro,
         'earliest_bid_date_without_material_revision':earliest_bid,
         'standstill_ends_at_close_of_day':end,
         'ordinary_contract_not_before':eligible_award,
         'ordinary_contract_remains_blocked_pending_interim_court_decision':cfg['unresolved_timely_challenge'],
         'continuity_contract_is_separate_limited_source_authority_not_main_award':cfg['urgency']=='separately_authorized_continuity',
         'actual_judge_source_notice_or_receiving':None}

def compute():
 case=read(R/'2026-11-current-country-operating-and-source-reference/cases/firm_plural_I05.json')
 rows=[]
 for r in case['public_book']['component_rows']:
  if r['kind']!='purchase':continue
  rows.append({'id':r['id'],'function_owner':r['owner'],'named_allocation_CU':r['named_allocation_CU'],
               'coverage':'linked_current_partial_scope' if r['id'] in LINKED else 'budget_or_task_quote_without_current_matched_supplier_recipe',
               'linked_scope':LINKED.get(r['id']),
               'actual_output_quantity_recipe_acceptance_or_paid_source':None})
 pb=read(R/'2026-11-ordinary-life-and-household-production/inputs.json')
 prior=read(R/'2026-11-ordinary-life-and-household-production/results.json')
 ordinary={x['id']:x for x in prior['ordinary']['rows']};private=[]
 for row in pb['basket']:
  if row['purpose']=='01':continue
  private.append({'id':row['id'],'kind':row['kind'],'reference_quantity':ordinary[row['id']]['quantity'],
                  'unit':row['unit'],'reference_purchaser_quote_CU':ordinary[row['id']]['purchaser_quote_CU'],
                  'coverage':'not_output_or_tax_base' if row['kind']=='unassigned_choice_envelope' else '131_partial_garment_offer_not_in_national_book' if row['id']=='garments' else 'unmatched_current_private_recipe',
                  'actual_need_buyer_recipe_order_receipt_or_source':None})
 cfg=read(D/'inputs.json')
 if set(cfg)!={'edition','scope','procurement_cases'} or cfg['edition']!=132:raise ValueError('Unsupported study input')
 return clean({'edition':132,'format_revision':'132-input-coverage-and-proposed-clocks-v1',
  'public_purchase_scope':{'rows':rows,'count':len(rows),'named_total_CU':sum(q(x['named_allocation_CU']) for x in rows),
   'linked_partial_scope_CU':sum(q(x['named_allocation_CU']) for x in rows if x['linked_scope']),
   'remaining_budget_or_task_scope_CU':sum(q(x['named_allocation_CU']) for x in rows if not x['linked_scope']),
   'six_clinical_budget_rows_CU':sum(q(x['named_allocation_CU']) for x in rows if x['id'] in CLINICAL),
   'scope':'Every purchase row in one 130 reference, not every national input, independent producer value added, full cost or proved minimum cost.'},
  'private_nonfood_reference':private,'proposed_clock_cases':[procurement_case(x) for x in cfg['procurement_cases']],
  'source_disposition':'Reject complete-source/ready-production inference. No new recipe, export, profit, tax yield, debt or issue fills the omitted scope.',
  'actual_national_source_capacity_authority_or_better_lives':None})

if __name__=='__main__':(D/'results.json').write_text(json.dumps(compute(),indent=2)+'\n')
