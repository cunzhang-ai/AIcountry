#!/usr/bin/env python3
"""Bounded preservation, finite democratic counterexamples and task/quote identities only."""
from pathlib import Path
from decimal import Decimal as Q
from copy import deepcopy
import hashlib,json,re,subprocess,sys
D=Path(__file__).resolve().parent;R=D.parent;sys.path.insert(0,str(D))
from model import compute
from capacity import local_size
from proofs import conditional_worlds,support_reuse
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(ok,why):
 if not ok:raise AssertionError(why)
 checks.append(why)
def near(a,b):return abs(Q(str(a))-Q(str(b)))<Q('.000001')
def rejects(fn):
 try:fn()
 except (ValueError,TypeError):return True
 return False
(D/'validation.json').write_text(json.dumps({'edition':128,'status':'incomplete'})+'\n')
b=read(D/'baseline.json');old=read(D/'predecessor-design-127/settlement/commitments/inventory.json');inv=read(R/'settlement/commitments/inventory.json')
check(len(b['sha256'])==977,'977exact127artifacts:976current Markdown and fullinventory')
check(all(sha(D/'predecessor-design-127'/n)==h for n,h in b['sha256'].items()),'Every predecessor artifact exactly preserved')
check(inv['functions']==old['functions'] and len(inv['functions'])==37,'All37complete originalfunction/bid/actualnullobjects exact')
check(inv['selections']==old['selections'] and len(inv['selections'])==61,'All61originalselections exact')
refs={k:v for k,v in old.items() if k.endswith('_reference') and isinstance(v,dict)}
check(len(refs)==67 and all(inv[k]==v for k,v in refs.items()),'All67inheritedreferences exact; changedproposals get no transferredfinalreview')
check(all(sha(R/n)==h for n,h in old['source_hashes'].items() if n.startswith('2026-')),'Every inherited datedsource/model/manifest/validation exact')
check(all(sha(R/n)==b['sha256'][n] for n in ['FRAMEWORK.md','DECISION-TEMPLATE.md']),'Commonframework/template unchanged; no newprocedureselfadoption')
check(all(sha(R/n)==h for n,h in b['sha256'].items() if n.startswith(('country/C04/','country/C05/','country/C07/','country/C08/','country/C09/'))),'Administration/personal/economy/service/justice/physicalcanonicalclauses exact')
cfg=read(D/'inputs.json');x=compute(cfg);check(x==read(D/'results.json'),'Declared all-scope capacity/quote/counterexample results reproduce')
c=x['capacity'];n=c['national'];l=c['local'];f=c['question'][0];s=c['source_profiles'];j=c['judicial_profiles'];w=c['named_work_plan'];p=c['paper'];z=x['scoped_replacement'];proof=x['proofs']
check(n['threshold']==500 and n['lists_or_committees_upper']==320 and n['nominee_entries_upper']==25600,'National EL threshold/list/pool bound under actualauthoredR and K')
check(len(l)==4 and all(v['E_ref']==20000 and v['N_fixed']==15 and v['threshold']==200 and v['nominee_entries_upper']==6000 for v in l),'Explicitcharter20k yields15seats, separatecalled/cutoffscope')
check(local_size(10000)==9 and local_size(10001)==15 and local_size(100001)==25,'ELcharterboundary sizing, not automaticcalledroll resizing')
check(f['threshold']==800 and f['lists_or_committees_upper']==200 and f['nominee_entries_upper']==0,'Questioncommittee proofscope not a secondcandidate pool')
check(c['total_lists_and_committees']==1320 and c['total_candidate_entries_not_distinct_persons']==49600 and c['total_endorsement_acts']==480000,'All sixcontests total without claiming49,600distinctpeople')
check(near(s['no_support_reuse']['task_hours'],53680) and s['no_support_reuse']['peak_distinct_people']==1820,'Meaningful no-sharing resource alternative retained')
check(near(s['matched_support_reuse']['task_hours'],38976) and s['matched_support_reuse']['peak_distinct_people']==1322,'Support/date/assent tasks stayseparate in selectedreference')
check(near(s['matched_support_reuse']['pay_quote_CU'],3966000),'1322people times.05paidroles priced, not1322fullannualposts')
check(Q(s['matched_support_reuse']['with_drill_task_hours'])==Q(38976)+Q(1322)*16,'Source drill work counted once beyond task work')
bad=deepcopy(cfg);bad['matched_national_question_P_scope_hypothesis']=False;y=compute(bad)
check(near(y['capacity']['source_profiles']['matched_support_reuse']['task_hours'],40576),'Nonmatchingquestioneligibility restores separate1600sourcehours')
bad=deepcopy(cfg);bad['source_hours']['available_final_task_days']=4;y=compute(bad)
check(y['capacity']['source_profiles']['matched_support_reuse']['peak_distinct_people']==1652,'Fouravailabletaskdays raisespeak; nolegalclockextension')
check(j['unshared']['case_entries']==5092 and j['unshared']['peak_judges']==432 and j['unshared']['peak_counsel']==432,'National/local/question10percent authoredcase reference, notobservedneed')
check(j['opt_in_common']['opt_in_common_entries']==4074 and j['opt_in_common']['assumed_common_families']==64 and j['opt_in_common']['peak_judges']==160 and j['opt_in_common']['peak_counsel']==160,'Consent/commonissue sensitivity remains explicitlyconditional')
check(j['unshared']['all_merits_immediately_due_judges']==1727 and j['unshared']['all_merits_immediately_due_counsel']==3453,'Earlieractualinjury defeats selectedmeritswindow instead of silentlywaiting')
check(j['opt_in_common']['all_merits_immediately_due_judges']==707 and j['opt_in_common']['all_merits_immediately_due_counsel']==1414,'Even hypothesizedsharing doesnotcover every useful-timepattern')
check(w['clerks']==173 and near(w['clerk_paid_role_equivalents'],17.3) and w['clerk_all_work_immediately_due_people']==1727,'Clerkpeak separated from annual10taskposts; adversebound retained')
check(c['information_help']['peak_distinct_helpers']==848 and c['information_help']['annual_task_role_bound_without_peak']==5,'One-day helppeak848 not annual5posts or ordinary22librarians')
bad=deepcopy(cfg);bad['information']['help_available_task_days']=10;y=compute(bad)
check(y['capacity']['information_help']['peak_distinct_helpers']==85,'Spreadhelp sensitivity distinct from actual lawful useful-time permission')
check(w['additional_drill_instructors']==4 and near(w['instruction_hours_before_own_learning'],4008.75),'Source/judge/counsel/clerk/helper drill pluspreparation and ownlearning instructors included')
check(near(p['mandatory_choice_pages_hypothesis'],2880000) and near(p['all_requested_fullguide_pages'],31760000),'Choicepages kept separate from optional fullguide/requestdirectory')
check(near(p['fullrequest_including_choice_CU'],1662720) and near(p['selected_request_hypothesis_including_choice_CU'],157440),'Fullrequest funding reference retained; segmentedrequest not actualsaving/accesscap')
check(near(z['removed_pay_quote_CU'],4794000) and near(z['new_scoped_pay_quote_CU'],11181000),'Exactlyfour inheritedsource/judge/counsel/clerk rows replaced once')
check(near(z['incremental_pay_quote_CU'],6387000) and near(z['incremental_paper_quote_CU'],211200) and near(z['scoped_named_pay_and_paper_delta_CU'],6598200),'Net scopedpay/paperdelta not duplicatedoldpay/fullbudget/source')
check(z['unreplaced_other_125_components_and_ordinary_librarians_retained'] is True,'Ordinary services/otherforum/records/distribution retained in scope')
pr=proof['structural_rival'];check(pr['national_40_seats']=={'A':20,'B':18,'C':2} and pr['four_10seat_regions']=={'A':20,'B':20,'C':0},'Real regionalPR rival changes representation of dispersedsmallcurrent')
pr=proof['closed_list_rival'];check(pr['optional_preference']['A']['elected']==['A2'] and pr['closed_order']['A']['elected']==['A1'],'Closed-list rival changesmemberchoice despite identical listcounts')
worlds=proof['conditional_worlds']['worlds'];check(len(worlds)==4,'Everybinarycombination enumerated for two-unknown fixture')
check(all(v['allocation']=={'A':1,'B':1} for v in worlds if any(v['assumed_eligibility'].values())) and worlds[0]['allocation']=={'A':0,'B':2},'Independentoneremovaltests miss jointpool-exhaustion change')
check(worlds[1]['members']['A']==['A2'] and worlds[2]['members']['A']==['A1'],'Samepartyseatcounts do not establish sameeligiblemember')
bad=deepcopy(cfg['conditional_world_fixture']);bad['pools']['A']=[f'A{i}' for i in range(9)];bad['unknown_nominees']=bad['pools']['A'];overflow=conditional_worlds(bad)
check(overflow['worlds'] is None and overflow['legal_candidate_cap'] is None and overflow['actual_certification'] is None,'Eight-unknown fixture bound creates no legalcap or incompletecertificate')
sp=proof['support_probes'];check(sp['exact_checked_support']['support_may_be_reexamined'] and sp['exact_checked_support']['fresh_final_decision_required'],'Exactsupport stillneeds freshfinaldecision')
check(not sp['local_scope_changed']['support_may_be_reexamined'],'Nationaleligibilitysupport cannot transfer to localhomecase')
check(not sp['new_event_same_hash']['support_may_be_reexamined'],'New event/objection sequence invalidates reusedsupport evenunchangedhash')
check(not sp['old_final_decision']['support_may_be_reexamined'],'Finalqualificationapproval never reusableassupport')
med=proof['future_medium'];check(med['original_reference']=='protected-opaque-example' and med['help_and_interpretation_needed'] and not med['rejected_for_unfamiliar_medium'] and med['actual_qualification'] is None,'Futureopaqueoriginal/firstattempt preserved for help, no automaticqualification')
for mutate,why in [(lambda v:v.update(future_medium='uninterpreted'),'Unknownfuture top-levelconcept notsilentlydropped'),(lambda v:v['local_bodies'][0].update(future_home='uninterpreted'),'Unknown nestedhomesemantics require interpretation'),(lambda v:v['judicial'].update(actual_dispute_incidence_sharedness_or_qualified_rosters=True),'Model cannot populateactualjudicialreadiness'),(lambda v:v.update(matched_person_identity_count=79999),'Unmatchedpersonscope cannot get sharedsourcecredit'),(lambda v:v['old_component_ids'].pop(),'Changingreplacement scope needs review'),(lambda v:v['information'].update(rows_per_choice_page=0),'Invalidpagebound rejected'),(lambda v:v['judicial'].update(opt_in_common_fraction='1.1'),'Invalidconsentfraction rejected'),(lambda v:v['local_bodies'][0].update(E_ref=True),'Boolcharter cannot become integerreference'),(lambda v:v.update(actual_country_democratic_adoption_or_readiness=True),'No actualcountryreadiness classifier')]:
 bad=deepcopy(cfg);mutate(bad);check(rejects(lambda:compute(bad)),why)
reg=read(D/'country-register.json');check(len(reg['functions'])==37 and all(v['original_complete_function_sha256']==hashlib.sha256(json.dumps(next(f for f in old['functions'] if f['id']==v['id']),sort_keys=True,separators=(',',':')).encode()).hexdigest() for v in reg['functions']),'All37sidecaridentities trace completeoriginalfunction objects')
check(all(v['actual_full_current_cost'] is None and v['actual_owned_source'] is None for v in reg['functions']),'Everyfunctionactualcost/source remainsnull')
src=read(D/'sources.json');check(len(src['external_sources'])==3 and all(sha(R/a['path'])==a['sha256'] for a in src['local_scoped_sources']),'Scopedprimarysourcefamilies/localdependencies exact, notempiricalorindependentreview')
chain=read(D/'control-chain.json');check(len(chain['links'])==6 and all(v['actual_independence_or_received_execution'] is None for v in chain['links']),'Completecandidatecontrol/failurechain distinguishedfromactualindependence')
scope=read(D/'scope-record.json');ref=inv['democratic_operation_and_public_understanding_reference'];check(all(a is None for o in [scope,ref,x] for k,a in o.items() if k.startswith('actual_')),'Selection, actualauthority/affectedreview/source/readiness/outcomes distinct')
check('Integrated design 128' in (R/'COUNTRY-DESIGN.md').read_text() and 'integrated design 128' in (R/'DESIGN-STATUS.md').read_text(),'Countryoverview/status/C03/C06 alignon128')
check(all(not re.search('[\u4e00-\u9fff]',(R/n).read_text()) for n in scope['changed_current_markdown']),'New/edited publiccurrentMarkdown English; historicalsources preserved')
check(sha(R/'history/03/11-design-116-onward.md')==b['sha256']['history/03/11-design-116-onward.md'],'Preceding142linehistory unchanged; newdecision extends separatecurrenthistory')
pins=read(D/'source-manifest.json')['sha256'];check(all((R/n).is_file() and sha(R/n)==h for n,h in pins.items()),'Every declaredlocal current/inherited pin matches')
run=subprocess.run([sys.executable,str(R.parent/'scripts/check-research-structure.py')],capture_output=True,text=True);check(run.returncode==0,'Structure/150linebound/14entrances/37singleauditowners/locallinks: '+run.stdout.strip()+run.stderr.strip())
report={'edition':128,'status':'pass','bounded_check_count':len(checks),'checks':checks,'source_pin_count':len(pins),'structure':run.stdout.strip(),'scope':'Exactpreservation and authoredfield/task/paidquote/source-scope/conditionalworld/rivalcounterexamples only. Not actualelectorate/meaning/consent/independentcapacity/comprehension/source/authority/safeoperation/receivedremedy/betterlives.'}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:a for k,a in report.items() if k!='checks'},indent=2))
