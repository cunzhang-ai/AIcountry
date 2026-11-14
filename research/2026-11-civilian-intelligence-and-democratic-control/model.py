"""Independent declared arithmetic/provenance/date probes, not a security engine."""
from pathlib import Path
from datetime import date,datetime,timedelta,timezone
import json,math
HERE=Path(__file__).resolve().parent
SCOPE='independent invented committee, lineage, cash, FX, shift and date probes; no real intelligence operation'
def keys(x,n):
 if not isinstance(x,dict) or set(x)!=set(n.split()):raise ValueError('Missing or unsupported semantics')
def number(x):
 if type(x) not in (int,float) or not math.isfinite(x) or x<0:raise ValueError('Unknown/invalid amount is not zero')
 return x
def integer(x,positive=False):
 number(x)
 if type(x) is not int or (positive and x<=0):raise ValueError('Invalid actual-count fixture')
 return x
def day(x):
 if not isinstance(x,str):raise ValueError('Missing date')
 try:d=date.fromisoformat(x)
 except (ValueError,TypeError):raise ValueError('Unsupported date')
 if d.isoformat()!=x:raise ValueError('Noncanonical Gregorian date')
 return d
def instant(x):
 if not isinstance(x,str) or not x.endswith('+00:00'):raise ValueError('Fixture requires explicit UTC')
 try:d=datetime.fromisoformat(x)
 except (ValueError,TypeError):raise ValueError('Unsupported time')
 if d.tzinfo!=timezone.utc:raise ValueError('Different clock semantics')
 return d
def committee(N,G,O):
 integer(N,True);integer(G);integer(O)
 if G+O>N:raise ValueError('Eligible people exceed full seats')
 K=min(5,N);A=G+O;k=min(K,A);votes=K//2+1
 if A:
  nearest=(2*k*O+A)//(2*A);low=max(k-G,min(2,O,k-min(1,G)));high=min(O,k-min(1,G));o=min(high,max(low,nearest))
 else:o=0
 return {'authorized_K':K,'allocatable_k':k,'governing_places':k-o,'nongoverning_places':o,'vacant_authorized':K-k,'fixed_present_and_yes':votes,'could_report_if_all_allocated_present_and_agree':k>=votes,'actual_cohort_independence_or_appointments':None}
def groups(rows,seats,total):
 if not isinstance(rows,dict) or any(not isinstance(k,str) or not k for k in rows):raise ValueError('Unsupported group identity')
 if sum(integer(v,True) for v in rows.values())!=total:raise ValueError('Group people do not match cohort')
 if not total:return {'conditional_places':{},'public_lot_needed':False,'actual_representatives':None}
 floor_alloc={k:v*seats//total for k,v in rows.items()};left=seats-sum(floor_alloc.values());order=sorted(rows,key=lambda k:(-(rows[k]*seats%total),k))
 tied=left>0 and left<len(order) and rows[order[left-1]]*seats%total==rows[order[left]]*seats%total
 if not tied:
  for k in order[:left]:floor_alloc[k]+=1
 return {'conditional_places':None if tied else floor_alloc,'floor_places_before_remainders':{k:v*seats//total for k,v in rows.items()},'public_lot_needed':tied,'actual_representatives':None}
def lineage(x):
 keys(x,'nodes selected_reports contrary_reports')
 if not isinstance(x['nodes'],list) or not x['nodes']:raise ValueError('Missing lineage')
 nodes={}
 for n in x['nodes']:
  keys(n,'id kind family parents')
  if not isinstance(n['id'],str) or not n['id'] or n['id'] in nodes:raise ValueError('Invalid repeated source ID')
  if not isinstance(n['parents'],list) or any(not isinstance(p,str) for p in n['parents']) or len(set(n['parents']))!=len(n['parents']):raise ValueError('Unsupported dependency scope')
  if n['kind']=='original':
   if n['parents'] or (n['family'] is not None and (not isinstance(n['family'],str) or not n['family'])):raise ValueError('Invalid original family')
  elif n['kind']=='derived':
   if not n['parents'] or n['family'] is not None:raise ValueError('Derived output is not its own origin')
  else:raise ValueError('Unfamiliar provenance role, not silently counted')
  nodes[n['id']]=n
 memo={}
 def walk(k,path):
  if k not in nodes or k in path:raise ValueError('Missing/circular original dependency')
  if k in memo:return memo[k]
  n=nodes[k]
  if n['kind']=='original':result=({n['family']} if n['family'] is not None else set(),{k} if n['family'] is None else set(),{k})
  else:
   known=set();unknown=set();used={k}
   for p in n['parents']:
    a,b,z=walk(p,path|{k});known|=a;unknown|=b;used|=z
   result=(known,unknown,used)
  memo[k]=result;return result
 for k in nodes:walk(k,set())
 def merge(ids):
  if not isinstance(ids,list) or len(ids)!=len(set(ids)) or any(not isinstance(k,str) for k in ids):raise ValueError('Invalid report selection')
  a=set();b=set();u=set()
  for k in ids:
   aa,bb,uu=walk(k,set());a|=aa;b|=bb;u|=uu
  return a,b,u
 a,b,u=merge(x['selected_reports']);ca,cb,cu=merge(x['contrary_reports'])
 return {'selected_report_count':len(x['selected_reports']),'known_declared_origin_families':sorted(a),'unknown_origin_ids':sorted(b),'contrary_declared_families':sorted(ca),'contrary_unknown_origin_ids':sorted(cb),'unexamined_node_ids':sorted(set(nodes)-u-cu),'actual_independence_truth_or_warning_authority':None}
def calculate(c=None):
 if c is None:c=json.loads((HERE/'inputs.json').read_text())
 keys(c,'edition declared_scope committee lineage resources shifts calendar handover')
 if type(c['edition']) is not int or c['edition']!=102 or c['declared_scope']!=SCOPE:raise ValueError('Different research meaning')
 a=c['committee'];keys(a,'N governing_eligible nongoverning_eligible governing_groups nongoverning_groups');p=committee(a['N'],a['governing_eligible'],a['nongoverning_eligible'])
 p['governing_groups']=groups(a['governing_groups'],p['governing_places'],a['governing_eligible']);p['nongoverning_groups']=groups(a['nongoverning_groups'],p['nongoverning_places'],a['nongoverning_eligible'])
 out={'committee':p,'lineage':lineage(c['lineage'])}
 a=c['resources'];keys(a,'declared_ownership treasury_cash prior_election_due prior_clinic_due new_analysis new_translation new_custody new_independent_review owned_FX_after_prior_dues new_FX_due private_exporter_FX insurer_F SF_G_standby SF_S_standby')
 if a['declared_ownership']!='distinct hypothetical Treasury cash, prior dues, usable owned FX and protected other owners; no hidden overlap':raise ValueError('Different ownership scope')
 for k,v in a.items():
  if k!='declared_ownership':number(v)
 prior=a['prior_election_due']+a['prior_clinic_due'];free=max(0,a['treasury_cash']-prior);need=sum(a[k] for k in ['new_analysis','new_translation','new_custody','new_independent_review'])
 out['resources']={'prior_due':prior,'prior_unpaid':max(0,prior-a['treasury_cash']),'remaining_cash_after_prior':free,'new_need':need,'new_cash_gap':max(0,need-free),'new_FX_gap':max(0,a['new_FX_due']-a['owned_FX_after_prior_dues']),'actual_owned_source_or_prices_or_appropriation':None}
 a=c['shifts'];keys(a,'declared_skill_scope language_available language_election_committed language_cyber_committed language_new_need legal_available legal_new_need hours_per_shift')
 if a['declared_skill_scope']!='one eight-hour shift per hypothetical qualified worker in this window; language and legal source skills distinct':raise ValueError('Different skills scope')
 for k,v in a.items():
  if k!='declared_skill_scope':integer(v)
 integer(a['hours_per_shift'],True)
 if a['hours_per_shift']!=8:raise ValueError('Different declared eight-hour skill window')
 prior=a['language_election_committed']+a['language_cyber_committed'];free=max(0,a['language_available']-prior);gap=max(0,a['language_new_need']-free)
 out['shifts']={'language_remaining':free,'language_gap_shifts':gap,'language_gap_hours':gap*a['hours_per_shift'],'prior_language_shortfall':max(0,prior-a['language_available']),'legal_gap_shifts':max(0,a['legal_new_need']-a['legal_available']),'actual_qualification_or_released_roster':None}
 a=c['calendar'];keys(a,'hypothetical_Act aggregate_programme_start identifiable_task_start same_task_renamed proposed_continuation first_identifiable_receipt later_screening unjustified_copy_removed notice_ground_ends notice_given declared_task_identity')
 if a['declared_task_identity']!='same identifiable task despite renamed actor or source':raise ValueError('Different task semantics')
 d={k:day(v) for k,v in a.items() if k!='declared_task_identity'};start=d['identifiable_task_start'];outer=start+timedelta(days=180);receipt=d['first_identifiable_receipt'];ordinary=receipt+timedelta(days=30);programme=d['aggregate_programme_start'];qmonth=((programme.month-1)//3+1)*3;nextq=date(programme.year+1,1,1) if qmonth==12 else date(programme.year,qmonth+1,1);qend=nextq-timedelta(days=1)
 if d['later_screening']<receipt or d['unjustified_copy_removed']<receipt or d['same_task_renamed']<start:raise ValueError('Invalid original chronology')
 out['calendar']={'fixed_180day_commencement':(d['hypothetical_Act']+timedelta(days=180)).isoformat(),'aggregate_first90_review':(programme+timedelta(days=90)).isoformat(),'first_quarter_report':(qend+timedelta(days=15)).isoformat(),'annual_safe_outlook':date(programme.year+1,3,1).isoformat(),'identifiable_first90_outer':(start+timedelta(days=90)).isoformat(),'identifiable_original180_outer':outer.isoformat(),'proposed_within_original_outer':start<=d['proposed_continuation']<=outer,'misleading_renamed180_outer':(d['same_task_renamed']+timedelta(days=180)).isoformat(),'misleading_rename_pass':d['proposed_continuation']<=d['same_task_renamed']+timedelta(days=180),'unjustified_original30_due':ordinary.isoformat(),'removed_within_original30':d['unjustified_copy_removed']<=ordinary,'misleading_screening_reset_pass':d['unjustified_copy_removed']<=d['later_screening']+timedelta(days=30),'PD25_initial30_review_fixture':(start+timedelta(days=30)).isoformat(),'ground_end_notice7_due':(d['notice_ground_ends']+timedelta(days=7)).isoformat(),'notice_within_ground_end7':d['notice_ground_ends']<=d['notice_given']<=d['notice_ground_ends']+timedelta(days=7),'actual_task_necessity_notice_ground_or_order':None}
 a=c['handover'];keys(a,'original_succession_UTC renamed_receipt_UTC inventory_given_UTC');original=instant(a['original_succession_UTC']);renamed=instant(a['renamed_receipt_UTC']);given=instant(a['inventory_given_UTC'])
 out['handover']={'original_elapsed_h':(given-original).total_seconds()/3600,'within_original24h':0<=(given-original).total_seconds()<=86400,'misleading_later_receipt24h':0<=(given-renamed).total_seconds()<=86400,'actual_lawful_succession_or_received_inventory':None}
 out['actual']={k:None for k in ['legitimate_authority','qualified_independent_review','affected_participation','original_threat_and_rights_evidence','funded_qualified_service_and_oversight','received_warning_or_correction_or_compensation','observed_better_lives']}
 return out
if __name__=='__main__':(HERE/'results.json').write_text(json.dumps(calculate(),indent=2,allow_nan=False)+'\n')
