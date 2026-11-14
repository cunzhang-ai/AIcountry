#!/usr/bin/env python3
"""Bounded preservation/current-consumer alignment and time compatibility, never country certification."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,re,subprocess,sys
D=Path(__file__).resolve().parent;R=D.parent;sys.path.insert(0,str(D));from model import compute
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(ok,why):
 if not ok:raise AssertionError(why)
 checks.append(why)
def rejects(fn):
 try:fn()
 except (TypeError,ValueError):return True
 return False
compact=lambda s:re.sub(r'\s+','',s)
(D/'validation.json').write_text(json.dumps({'edition':129,'status':'incomplete'})+'\n')
b=read(D/'baseline.json');P=D/'predecessor-design-128';old=read(P/'settlement/commitments/inventory.json');inv=read(R/'settlement/commitments/inventory.json')
check(len(b['sha256'])==988,'988exact128artifacts:987currentMarkdown and completeinventory')
check(all(sha(P/n)==h for n,h in b['sha256'].items()),'Everypreserved128artifact exact')
check(inv['functions']==old['functions'] and len(inv['functions'])==37,'All37completeoriginalfunction/bid/actualnullobjects exact')
check(inv['selections']==old['selections'] and len(inv['selections'])==61,'All61originalselections exact')
refs={k:v for k,v in old.items() if k.endswith('_reference') and isinstance(v,dict)}
check(len(refs)==68 and all(inv[k]==v for k,v in refs.items()),'All68inheritedreferenceobjects exact; no transferredfinalapproval')
check(all(sha(R/n)==h for n,h in old['source_hashes'].items() if n.startswith('2026-')),'Everyinheriteddatedsource/model/manifest/report exact')
check(all(sha(R/n)==b['sha256'][n] for n in ['FRAMEWORK.md','DECISION-TEMPLATE.md']),'Commonproposedmethod/template unchanged, no newprocedure approves itself')
check(all(sha(R/n)==h for n,h in b['sha256'].items() if n.startswith(('country/C01/','country/C02/','country/C04/','country/C05/','country/C06/','country/C07/','country/C08/','country/C09/','country/C10/','country/C11/','country/C12/'))),'Existingfoundations/rights/economy/budget/services/justice/physical/defense/AI/collaborationcanonicalclauses exact')
check(all(sha(R/n)==h for n,h in b['sha256'].items() if n.startswith('country/C03/13')),'ELselectedfranchise/count/meaning/local rules unchanged; consumerrepair not newelectoralpolicy')
a10=(R/'authority/05-candidate-provisions-A10-A15.md').read_text();oa10=(P/'authority/05-candidate-provisions-A10-A15.md').read_text();a9=(R/'authority/provisions/03-review-emergency-and-change-A07-A09.md').read_text();oa9=(P/'authority/provisions/03-review-emergency-and-change-A07-A09.md').read_text()
check(compact(a10[a10.index('**A11'):])==compact(oa10[oa10.index('**A11'):]),'A11-A15essential/local/continuity/evidence/culture text retained, not reselected')
check(compact(a9[a9.index('**A7'):a9.index('**A9')])==compact(oa9[oa9.index('**A7'):oa9.index('**A9')]),'A7-A8review/emergency/externalscope retained')
check('one fixed-size national proportional-list track' in a10 and 'There is no additional' in a10 and 'territorial-person track' in a10,'A10activepositivechoice and exclusion of oldextra territorial seats explicit')
check('N minus independent personal seats' not in a10 and 'two-vote, fixed-size compensatory model' not in a10,'Retired count no longer prescribed by activeA10consumer')
check('ordinary election-statute reference' in a10 and 'retroactively authorize its own ballot' in a10 and 'Existing-called polls' in a10,'Constitutionalrights/statutoryform/priorcontestauthority separated')
check('All RR02–RR07 safeguards apply' in a9 and 'predecessor-law' in a9 and 'protected immediate succession' in a9,'A9points to fullclosedRRscope and existingreviewingauthority')
check(all(v in a9 for v in ['lawful rerun','formation-failure repeats','alter seat conversion or boundaries','absent forum','approve itself']),'Reruns/complete protectedsuccession and prohibitedrestoration shortcuts retained')
for path,dup in [('country/C14/08/01-delay-and-restoration.md','- Earlier effect is necessary to prevent identifiable exclusion or irreparable\n  loss of that function before ordinary delayed effect; an adequate narrower\n  existing-law remedy is unavailable.\n'),('country/C14/08/02-review-electorate-and-time.md','Publish the early-effect determination before the final90-day consideration\nperiod. The supported text must state the requested date and any expressly\napproved delayed fallback; a court cannot invent a fallback or severability.\n')]:
 before=(P/path).read_text();after=(R/path).read_text();check(before.count(dup)==2 and compact(before.replace(dup+dup,dup))==compact(after),'Only exact duplicate and whitespace removed, distinctRRpredicates unchanged: '+path)
path='country/C14/01/02-public-constitutional-change.md';before=(P/path).read_text();after=(R/path).read_text();check(compact(before.replace('These\nNo approval follows from zero valid yes/no votes. These','No approval follows from zero valid yes/no votes. These'))==compact(after),'Broken sentence repaired without amendmentthreshold/date/zero-vote change')
form=(R/'country/C14/05-scale-and-national-form.md').read_text();found=(R/'country/C14/01/01-lawful-founding-and-rank.md').read_text();ea=(R/'country/C03/09/05-migration-rivals-and-cases.md').read_text()
check('replaces the older two-vote/D-ceiling candidate' in form and 'must enact N, D' not in form,'Nationalform consumer treats oldDceiling as historicalrival, not unfilledcurrentparameter')
check('no territorial-person plurality track' in found and 'For the C03 reference this includes N, D' not in found,'Foundingconsumer aligns actualN/localcharters/source/count with EL')
check('root\'s' not in ea and 'current whole-country priorities' in ea,'EAactivefollowthrough no internalagent reference or obsoleteautomaticnextboard')
stress=(R/'country/C13/14-incumbent-campaign-capture.md').read_text();check('Cabinet appointment of the election' in stress and 'not the current lawful candidate arrangement' in stress and 'separate from ballot decisions' in stress,'Campaignstress distinguishes adversarialpressure from currentEAmixed/careerpowers')
cfg=read(D/'inputs.json');x=compute(cfg);check(x==read(D/'results.json'),'Authored finiteinterval results reproduce exactly')
check(x['requested_paid_work_minutes_week']==1920 and x['nominal_current_care_offer_minutes_week']==2400,'32paidwork/40nominalcare offer scope explicit')
check(x['current']['earliest_work_arrival_minute']==525 and x['current']['latest_work_departure_minute']==915,'45minute journeys constrain actualfeasiblearrival/departure to08:45-15:15')
check(x['current']['feasible_requested_work_minutes_week']==1560 and x['missing_current_work_minutes_week']==360,'Nominalsufficientweeklyoffers permit26workhours, sixshort')
check(not x['current']['time_compatibility_only'] and x['current']['chosen_minutes_within_S10_reference'],'Withinweeklyreference alone cannot imply usablework/care combination')
check(x['alternative']['feasible_requested_work_minutes_week']==1920 and x['alternative']['chosen_care_minutes_week']==2280 and x['alternative']['time_compatibility_only'],'07:15-16:45alternate fits time with38chosencarehours')
check(x['alternative']['chosen_minutes_within_S10_reference'] and x['alternative']['actual_safe_received_service_or_free_choice'] is None,'Timefit/withinreference do not certify childchoice/safety/receivedcare')
check(x['additional_chosen_edge_child_minutes_week']==360 and x['hypothetical_all_family_edge_child_hours_week']==6000 and x['hypothetical_all_family_edge_child_hours_year']==288000,'1000family/48weekchild-hour exposure explicit')
check(x['additional_staff_hours_or_budget'] is None and x['actual_staff_ratio_group_schedule_release_child_preference_or_quality'] is None,'Childhours cannot become workerhours/freeunuseddaystaff/budget without matchedgroups/source')
bad=deepcopy(cfg);bad['journey_minutes_each_way']=0;y=compute(bad);check(y['current']['time_compatibility_only'] and y['current']['feasible_requested_work_minutes_week']==1920,'Zerojourney counterfactual discriminates cause, not unexplainednewentitlement')
bad=deepcopy(cfg);bad['journey_minutes_each_way']=30;y=compute(bad);check(y['current']['feasible_requested_work_minutes_week']==1680,'Shorter30minutejourney still leaves28/32hours under identicalofferwindows')
bad=deepcopy(cfg);bad['alternative_care_end_minute']=960;y=compute(bad);check(not y['alternative']['time_compatibility_only'],'Only earlieropening does not supply laterreceiving; incompletealternate fails')
for mutate,why in [(lambda c:c.update(future_medium={'uninterpreted':'situated'}),'Unknownfuturemeaning cannot silently enter a fixture'),(lambda c:c.update(scope=['uninterpreted']),'Changedscope type needs interpretation'),(lambda c:c.update(work_start_minute=True),'Boolcannotbe a lawful time integer'),(lambda c:c.update(alternative_care_end_minute=100),'Overnightsemantics not silently forcedinto daytime'),(lambda c:c.update(chosen_work_days=6),'Work beyond offereddayfixture requires new receiving'),(lambda c:c.update(S10_weekly_reference_minutes=2500),'Fixture cannot silently redefine currentS10reference'),(lambda c:c.update(actual_child_choice_safe_capacity_received_service_or_authority=True),'No actualchild/safeoperation/authorityclassifier supplied')]:
 bad=deepcopy(cfg);mutate(bad);check(rejects(lambda:compute(bad)),why)
findings=read(D/'findings.json');check([c['id'] for c in findings['chapters']]==[f'C{i:02}' for i in range(1,15)] and all((R/c['entrance']).is_file() and all((R/n).is_file() for n in c['material_inspected_dependencies']) for c in findings['chapters']),'14entrance/selecteddependency dispositions trace real currentpaths, not everyclauseproof')
check(all(c['actual_full_chapter_review'] is None and c['actual_affected_choice_authority_or_outcome'] is None for c in findings['chapters']),'Chapter inspection explicitlylimited, no inventedaffected/fulllegalreview')
req=read(D/'requirements.json');check(len(req['requirements'])==12 and [a['id'] for a in req['requirements']]==[f'R{i:02}' for i in range(1,13)] and all((R/a['principal_evidence_path']).is_file() for a in req['requirements']),'All12wholegoal/instruction requirements have named evidence and disposition')
check(req['full_goal_achieved'] is False and all(not c['design_complete_proved'] and c['actual_authority_readiness_or_better_lives'] is None for c in req['requirements']),'No shrunkenobjective or artifactchecks substitutedfor fullgoalproof')
reg=read(D/'country-register.json');check(len(reg['functions'])==37 and all(v['original_complete_function_sha256']==hashlib.sha256(json.dumps(next(f for f in old['functions'] if f['id']==v['id']),sort_keys=True,separators=(',',':')).encode()).hexdigest() for v in reg['functions']),'Every37sidecar traces original completefunction object')
check(all(v['original_function_name']==next(f.get('name',f.get('function')) for f in old['functions'] if f['id']==v['id']) for v in reg['functions']),'Functionnames preserve originalsemantics, not inferredrelabelled K03orotherduties')
check(all(v['actual_full_current_cost'] is None and v['actual_owned_source'] is None for v in reg['functions']),'Allactualfullfunctioncost/source fields remain null')
src=read(D/'sources.json');check(all(sha(R/a['path'])==a['sha256'] for a in src['local_scoped_sources']),'Listed selectedcurrent/source identities exact, not fullsemantic/empiricalreview')
scope=read(D/'scope-record.json');ref=inv['country_closure_and_lived_operation_reference'];check(all(v is None for o in [scope,ref,x] for k,v in o.items() if k.startswith('actual_')),'Evidence/selection/legaladoption/source/readiness/receivedlives separate')
check('Integrated design 129' in (R/'COUNTRY-DESIGN.md').read_text() and 'integrated design 129' in (R/'DESIGN-STATUS.md').read_text(),'Canonicaloverview/status/C13/C14 alignon129scope andonecurrentnext')
check(all(not re.search('[\u4e00-\u9fff]',(R/n).read_text()) for n in scope['changed_current_markdown']),'Allnew/editedcurrentpublicMarkdown English; historicalsources unchanged')
check(sha(R/'history/03/11-design-116-onward.md')==b['sha256']['history/03/11-design-116-onward.md'],'Earlierhistory unchanged; newdecision extends boundedseparatehistory')
pins=read(D/'source-manifest.json')['sha256'];check(all((R/n).is_file() and sha(R/n)==h for n,h in pins.items()),'Every declared current/inheritedlocal pin matches')
run=subprocess.run([sys.executable,str(R.parent/'scripts/check-research-structure.py')],capture_output=True,text=True);check(run.returncode==0,'Currentstructure/150linebound/14chapters/37singleauditowners/locallinks: '+run.stdout.strip()+run.stderr.strip())
report={'edition':129,'status':'pass','bounded_check_count':len(checks),'checks':checks,'source_pin_count':len(pins),'structure':run.stdout.strip(),'scope':'Exactpreservation, selectedactiveconsumer alignment, scoped14chapter/12requirement map and finiteinterval counterexamples only. Not exhaustivelaw/actualchildorpublicchoice/safequalifiedcapacity/currentcountrycost/source/independentauthority/readiness/receivedremedy/betterlives.'};(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
