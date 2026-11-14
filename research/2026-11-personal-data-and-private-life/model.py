"""Authored work/scope/deadline bounds, not a legal/data-processing decision system."""
from pathlib import Path
from datetime import datetime,timedelta
import copy,json,math
HERE=Path(__file__).resolve().parent
FIELDS={
'intake':{'online_h','assisted_h','interpretation_h','available_assisted_h','actual_clinical_receipt'},
'correction':{'tasks','available_by_task','completed_nodes','actual_corrected_model_or_decision'},
'proof':{'issuer_pilot_CU','verifier_pilot_CU','first_year_audit_training_CU','assisted_fallback_CU','claim','actual_earned_units_or_payee_or_receipt','actual_anonymity_or_safe_proof'},
'vendor':{'shared_forensic_core_h','health_response_h','benefit_response_h','coordination_h','actual_qualified_shifts_or_receivers'},
'agent':{'scope_version','allowed_purpose','allowed_recipient','allowed_actions','requested_actions','direct_assisted_alternative_h','fixture_prior_valid_booking','actual_data_basis_or_current_mandate','actual_unlearning_or_received_care'},
'request_clock':{'first_usable_received','later_referral_received','answer_given','ordinary_days','extension_days','extension_given','extension_genuine_complexity','extension_previously_used','urgent_protection_due','protection_given','actual_legal_or_service_finding'},
'breach_clock':{'reasonable_awareness','regulator_notice','affected_notice','outer_hours','useful_protection_due','protection_given','actual_secure_recovery_or_notice_receipt'},
'actual':{'jurisdiction_law_and_treaties','appropriation_and_owned_sources','qualified_controller_supervisor_or_court_staff','lawful_bases_consent_and_mandates','safe_custody_anonymity_or_unlearning','affected_participation','qualified_independent_review','received_remedies','better_lives'}}
TASKS={'source','feature_model','housing_redecision','independent_challenge'}
ACTIONS={'book_visit','send_listed_symptoms','train_on_full_archive','send_to_insurer'}
def number(v):
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<0:raise ValueError('Uninterpreted negative/nonfinite/non-numeric quantity')
    return v
def instant(s):
    if not isinstance(s,str):raise ValueError('Explicit aware timestamp required')
    try:t=datetime.fromisoformat(s)
    except ValueError:raise ValueError('Unsupported date semantics')
    if t.tzinfo is None or t.utcoffset()!=timedelta(0):raise ValueError('This UTC fixture needs an explicit UTC offset; other calendars require interpretation')
    return t

def calculate(c=None):
    if c is None:c=json.loads((HERE/'inputs.json').read_text())
    if not isinstance(c,dict) or set(c)!=set(FIELDS)|{'edition','status','unit'}:raise ValueError('Explicit missing/new case semantics require fresh interpretation')
    for k,keys in FIELDS.items():
        if not isinstance(c[k],dict) or set(c[k])!=keys:raise ValueError('Changed schema in '+k+' cannot approve itself')
    if type(c['edition']) is not int or c['edition']!=96:raise ValueError('No review transfer to a new edition')
    a=c['intake'];demand=number(a['assisted_h'])+number(a['interpretation_h']);available=number(a['available_assisted_h'])
    intake=dict(assisted_intake_required_h=demand,online_intake_reference_h=number(a['online_h']),
        assisted_gap_h=max(0,demand-available),actual_clinical_receipt=a['actual_clinical_receipt'])
    b=c['correction']
    if set(b['tasks'])!=TASKS or set(b['available_by_task'])!=TASKS or not isinstance(b['completed_nodes'],list) or len(set(b['completed_nodes']))!=len(b['completed_nodes']) or not set(b['completed_nodes'])<=TASKS:raise ValueError('Unknown or duplicated correction-stage meaning')
    required={k:number(v) for k,v in b['tasks'].items()};avail={k:number(v) for k,v in b['available_by_task'].items()}
    if any(avail[k]<required[k] for k in b['completed_nodes']):raise ValueError('Declared completion contradicts this same-window per-task capacity; reinterpreted evidence is required')
    correction=dict(required_distinct_h=sum(required.values()),available_aggregate_h=sum(avail.values()),
        shortage_by_task_h={k:max(0,required[k]-avail[k]) for k in sorted(TASKS)},
        uncompleted_nodes=sorted(TASKS-set(b['completed_nodes'])),all_stages_completed=set(b['completed_nodes'])==TASKS,
        actual_corrected_model_or_decision=b['actual_corrected_model_or_decision'])
    p=c['proof']
    if p['claim']!='over65_hypothetical_threshold':raise ValueError('New claim meaning cannot inherit threshold-only pilot cost or authority')
    named=sum(number(p[k]) for k in ['issuer_pilot_CU','verifier_pilot_CU','first_year_audit_training_CU']);fallback=p['assisted_fallback_CU']
    proof=dict(named_first_year_subset_CU=named,assisted_fallback_CU=fallback,
        full_example_cost_CU=None if fallback is None else named+number(fallback),claim=p['claim'],
        actual_earned_units_or_payee_or_receipt=p['actual_earned_units_or_payee_or_receipt'],actual_anonymity_or_safe_proof=p['actual_anonymity_or_safe_proof'])
    v=c['vendor'];core=number(v['shared_forensic_core_h']);total=core+sum(number(v[k]) for k in ['health_response_h','benefit_response_h','coordination_h'])
    vendor=dict(distinct_task_h=total,incorrect_duplicate_core_total_h=total+core,shared_core_count=1,
        actual_qualified_shifts_or_receivers=v['actual_qualified_shifts_or_receivers'])
    g=c['agent']
    if g['scope_version']!='booking_example_v1' or g['allowed_purpose']!='book_clinical_visit' or g['allowed_recipient']!='chosen_clinician':raise ValueError('New mandate purpose/recipient/version needs interpreted case')
    for k in ['allowed_actions','requested_actions']:
        if not isinstance(g[k],list) or len(g[k])!=len(set(g[k])) or not set(g[k])<=ACTIONS:raise ValueError('Unsupported or duplicated future action')
    if not set(g['allowed_actions'])<={'book_visit','send_listed_symptoms'}:raise ValueError('Booking-case version cannot authorize a new training or insurer purpose')
    if type(g['fixture_prior_valid_booking']) is not bool:raise ValueError('Numeric flag is not proof of prior validity')
    agent=dict(scope_only_classification={k:k in g['allowed_actions'] for k in g['requested_actions']},
        direct_assisted_alternative_h=number(g['direct_assisted_alternative_h']),
        fixture_prior_booking_not_erased_by_chat_deletion=g['fixture_prior_valid_booking'],
        actual_data_basis_or_current_mandate=g['actual_data_basis_or_current_mandate'],actual_unlearning_or_received_care=g['actual_unlearning_or_received_care'])
    t=c['request_clock']
    if t['ordinary_days']!=30 or t['extension_days']!=30:raise ValueError('A new legal clock requires a new interpreted case, not self-authorizing input')
    first=instant(t['first_usable_received']);deadline=first+timedelta(days=number(t['ordinary_days']))
    if type(t['extension_genuine_complexity']) is not bool or type(t['extension_previously_used']) is not bool:raise ValueError('Unsupported extension meaning')
    if t['extension_previously_used']:raise ValueError('An existing-extension history requires a separate interpreted timeline; do not erase its valid deadline or grant a second extension')
    extension=t['extension_given'];extended=extension is not None and first<=instant(extension)<deadline and t['extension_genuine_complexity'] and not t['extension_previously_used']
    if extended:deadline+=timedelta(days=number(t['extension_days']))
    later=instant(t['later_referral_received'])
    if later<first:raise ValueError('Earlier claimed first receipt requires reinterpreted baseline')
    request=dict(first_usable_received=first.isoformat(),fixture_controller_outer_due_assuming_valid_extension=deadline.isoformat(),
        fixture_extension_time_and_flags_pass=extended,answer_within_trigger_and_outer_bound=first<=instant(t['answer_given'])<=deadline,
        ignored_reset_if_using_referral=(later+timedelta(days=t['ordinary_days'])).isoformat(),
        urgent_protection_within_useful_time=instant(t['protection_given'])<=instant(t['urgent_protection_due']),
        working_day_or_holiday_deadlines_computed=False,actual_legal_or_service_finding=t['actual_legal_or_service_finding'])
    z=c['breach_clock']
    if z['outer_hours']!=72:raise ValueError('Changed notice rule requires fresh scoped interpretation')
    aware=instant(z['reasonable_awareness']);outer=aware+timedelta(hours=number(z['outer_hours']))
    breach=dict(outer_due=outer.isoformat(),regulator_trigger_and_outer_notice_bound=aware<=instant(z['regulator_notice'])<=outer,
        affected_trigger_and_outer_notice_bound=aware<=instant(z['affected_notice'])<=outer,
        useful_protection_within_time=instant(z['protection_given'])<=instant(z['useful_protection_due']),
        without_undue_delay_or_full_notice_receipt_qualified=False,actual_secure_recovery_or_notice_receipt=z['actual_secure_recovery_or_notice_receipt'])
    return dict(edition=96,status=c['status'],intake=intake,correction=correction,proof=proof,vendor=vendor,agent=agent,request_clock=request,breach_clock=breach,actual=copy.deepcopy(c['actual']))

if __name__=='__main__':(HERE/'results.json').write_text(json.dumps(calculate(),indent=2)+'\n')
