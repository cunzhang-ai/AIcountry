"""Finite counterexamples over supplied interpreted facts, never an actual adjudicator."""
from pathlib import Path
import importlib.util,itertools
R=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('el111',R/'2026-11-equal-franchise-and-usable-elections/model.py');el=importlib.util.module_from_spec(spec);spec.loader.exec_module(el)
def conditional_worlds(fixture):
 names=[n for pool in fixture['pools'].values() for n in pool];unknown=fixture['unknown_nominees']
 if len(names)!=len(set(names)) or len(unknown)!=len(set(unknown)) or not set(unknown)<=set(names):raise ValueError('Exact distinct per-body names required')
 if len(unknown)>fixture['max_executable_unknowns']:
  return {'status':'unresolved representation; another qualified complete proof required','worlds':None,'actual_certification':None,'legal_candidate_cap':None}
 worlds=[]
 for bits in itertools.product([False,True],repeat=len(unknown)):
  eligible=dict(zip(unknown,bits));pools={k:[n for n in pool if eligible.get(n,True)] for k,pool in fixture['pools'].items()};a=el.count(fixture['votes'],fixture['seats'],{k:len(v) for k,v in pools.items()},list(pools));persons=el.persons(a['allocation'],pools,{},fixture['votes'])
  worlds.append({'assumed_eligibility':eligible,'allocation':a['allocation'],'members':{k:v['elected'] for k,v in persons.items()},'unfilled':a['unfilled']})
 return {'status':'complete authored binary pool fixture, fixed interpreted votes; no actual eligibility or ballot meaning','worlds':worlds,'actual_certification':None,'legal_candidate_cap':None}
def support_reuse(support,need,events_seq):
 keys={'kind','person','scope','date','rule','original_observation_hash','complete_dependency_scope','checked_events_seq'}
 if set(support)!=keys or set(need)!=keys:raise ValueError('Unsupported future support semantics preserved for human review')
 allowed=support['kind'] in ['identity_support','eligibility_support']
 return {'support_may_be_reexamined':allowed and support['complete_dependency_scope'] is True and need['complete_dependency_scope'] is True and support==need and support['checked_events_seq']==events_seq,'fresh_final_decision_required':True,'actual_reuse_authorization_or_final_decision':None}
def future_receipt(opaque_reference,first_credible_attempt,interpreted):
 return {'original_reference':opaque_reference,'first_credible_attempt_hypothesis':first_credible_attempt,'help_and_interpretation_needed':not interpreted,'rejected_for_unfamiliar_medium':False,'actual_receipt_finding':None,'actual_qualification':None}
def compute(fixture):
 regional=[el.count({'A':10000,'B':9000,'C':1000},10,{'A':10,'B':10,'C':10},['A','B','C'])['allocation'] for _ in range(4)]
 national=el.count({'A':40000,'B':36000,'C':4000},40,{'A':40,'B':40,'C':40},['A','B','C'])['allocation']
 v={'A':60,'B':40};p={'A':['A1','A2'],'B':['B1','B2']};a=el.count(v,2,{'A':2,'B':2})['allocation']
 fact={'kind':'eligibility_support','person':'p','scope':'national-P','date':'P','rule':'hypothesis-r1','original_observation_hash':'authored-not-observation','complete_dependency_scope':True,'checked_events_seq':7};other={**fact,'scope':'local-home-P'}
 return {'structural_rival':{'national_40_seats':national,'four_10seat_regions':{k:sum(r[k] for r in regional) for k in v|{'C':0}},'actual_electorate_or_geography':None},'closed_list_rival':{'same_list_allocation':a,'optional_preference':el.persons(a,p,{'A':{'A2':30}},v),'closed_order':el.persons(a,p,{},v),'actual_voter_choice':None},'conditional_worlds':conditional_worlds(fixture),'support_probes':{'exact_checked_support':support_reuse(fact,fact,7),'local_scope_changed':support_reuse(fact,other,7),'new_event_same_hash':support_reuse(fact,fact,8),'old_final_decision':support_reuse({**fact,'kind':'final_qualification'},{**fact,'kind':'final_qualification'},7)},'future_medium':future_receipt('protected-opaque-example','hypothetical first attempt',False),'actual_adjudication_or_election_or_understanding':None}
