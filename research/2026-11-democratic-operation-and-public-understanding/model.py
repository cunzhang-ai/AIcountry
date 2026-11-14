"""Democratic operating hypotheses and finite counterexamples; no actual country classifier."""
from pathlib import Path
from decimal import Decimal as Q
import json
from capacity import compute as capacity_compute,q
from proofs import compute as proof_compute
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text())
def clean(v):
 if isinstance(v,Q):return str(v)
 if isinstance(v,dict):return {k:clean(a) for k,a in v.items()}
 if isinstance(v,list):return [clean(a) for a in v]
 return v
def matches(v,s):
 if 'dict' in s:return isinstance(v,dict) and set(v)==set(s['dict']) and all(matches(v[k],a) for k,a in s['dict'].items())
 if 'list' in s:return isinstance(v,list) and all(matches(a,s['list']) for a in v)
 if 'null' in s:return v is None
 return type(v).__name__==s['type']
def compute(cfg):
 if not matches(cfg,read(D/'input-shape.json')):raise ValueError('Unknown/missing concepts or changed types require scoped interpretation')
 def unknown(v):
  if isinstance(v,dict):return all((a is None if k.startswith('actual_') else unknown(a)) for k,a in v.items())
  if isinstance(v,list):return all(unknown(a) for a in v)
  return True
 if cfg['edition']!=128 or not unknown(cfg):raise ValueError('No actual law/capacity/consent or readiness supplied')
 if cfg['source_service']!='2026-11-joined-country-operating-book/results.json' or cfg['old_electoral_model']!='2026-11-equal-franchise-and-usable-elections/model.py':raise ValueError('Changed source requires qualified dependency review')
 for key in ['nominee_challenge_fraction','list_or_committee_challenge_fraction','opt_in_common_fraction']:
  if not 0<=q(cfg['judicial'][key])<=1:raise ValueError('Invalid hypothetical fraction')
 if not 0<=q(cfg['information']['help_request_fraction'])<=1:raise ValueError('Invalid request fraction')
 if len(cfg['questions'])!=1 or len(cfg['local_bodies'])!=4 or len({a['id'] for a in cfg['local_bodies']})!=4:raise ValueError('Different scope requires person-source/reuse analysis')
 if cfg['matched_person_identity_count']!=cfg['R_cutoff'] or sum(a['R_cutoff'] for a in cfg['local_bodies'])!=cfg['R_cutoff'] or cfg['questions'][0]['R_cutoff']!=cfg['R_cutoff']:raise ValueError('Authored matched-person fixture scope not established')
 for obj in [cfg['source_hours'],cfg['information'],cfg['pay'],cfg['trainer']]:
  if any(q(a)<=0 for k,a in obj.items() if not k.startswith('actual_')):raise ValueError('Positive task/cost assumptions required')
 if any(q(a)<0 for k,a in cfg['judicial'].items() if not k.startswith('actual_')):raise ValueError('Nonnegative judicial work required')
 c=capacity_compute(cfg);old=read(R/cfg['source_service']);rows=old['service_cases']['plural_public_backbone']['component_rows'];expected=['labor:EL_fullfield_source','labor:EL_judicial_peak','labor:EL_legal_aid_peak','labor:EL_clerk_peak']
 if cfg['old_component_ids']!=expected:raise ValueError('Do not silently retain/erase/replace unrelated source components')
 oldpay=sum(q(r['named_allocation_CU']) for r in rows if r['id'] in expected);oldpaper=next(q(r['named_allocation_CU']) for r in rows if r['id']=='op:EL_fullscope_paper');pay=c['named_work_plan']['gross_pay_quote_CU'];paper=c['paper']['fullrequest_including_choice_CU']
 return clean({'edition':128,'scope':cfg['scope'],'capacity':c,'proofs':proof_compute(cfg['conditional_world_fixture']),'scoped_replacement':{'removed_125_component_ids':expected,'removed_pay_quote_CU':oldpay,'new_scoped_pay_quote_CU':pay,'incremental_pay_quote_CU':pay-oldpay,'old_fullguide_paper_quote_CU':oldpaper,'new_choice_plus_fullrequest_paper_quote_CU':paper,'incremental_paper_quote_CU':paper-oldpaper,'scoped_named_pay_and_paper_delta_CU':pay-oldpay+paper-oldpaper,'unreplaced_other_125_components_and_ordinary_librarians_retained':True,'actual_full_national_source_or_deficit':None},'actual_legal_authority':None,'actual_independent_affected_participation':None,'actual_qualified_released_roster_or_received_remedy':None,'actual_public_understanding_or_better_lives':None})
if __name__=='__main__':(D/'results.json').write_text(json.dumps(compute(read(D/'inputs.json')),indent=2)+'\n')
