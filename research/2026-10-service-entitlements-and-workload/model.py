"""Illustrative service workload, joint activity and due-period capacity.
Not clinical staffing guidance, a whole-service census, or a national budget.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,math
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def q(x):return F(str(x))
def clean(x):
 if isinstance(x,F):return float(x)
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,list):return [clean(v) for v in x]
 return x

def validate_inputs(d):
 known={'edition','date','scope','pinned_sources','population','service','capacity','primary','shared_admin','illustrative_pay_million','limits'}
 if set(d)-known:raise ValueError('Unsupported workload input semantics')
 p=d['population'];s=d['service'];a=d['capacity']
 assert p['age_0_2']+p['age_3_5']+p['age_6_17']+p['adults']==p['total']
 assert 0<=p['adult_care_users']<=p['adults'] and 0<=p['school_support_users']<=p['age_6_17']
 assert all(0<=q(s[k])<=1 for k in ['early_takeup','under3_care_takeup','preschool_care_takeup'])
 assert all(type(s[k]) is int and s[k]>0 for k in ['early_group','school_group','under3_group'])
 assert all(q(s[k])>=0 for k in ['early_hours','school_hours','care_hours','adult_assessed_mean_weekly_hours','teacher_preparation_fraction'])
 assert a['usable_annual_hours_per_FTE']>0 and 0<=q(a['additional_absence_fraction'])<1
 assert a['education_teachers']+a['education_support']+a['education_other']==a['education_total']
 assert a['primary_general_FTE']+a['primary_mental_FTE']+a['primary_reproductive_FTE']<=a['national_clinical_reference']
 assert a['shared_admin_FTE']<=a['national_admin_reference']
 months=d['shared_admin']['election_months'];assert months and len(months)==len(set(months)) and all(1<=m<=12 for m in months)

def calculate(d=None):
 if d is None:d=json.loads((HERE/'inputs.json').read_text())
 validate_inputs(d)
 for path,h in d['pinned_sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
 p=d['population'];s=d['service'];a=d['capacity'];hours=q(a['usable_annual_hours_per_FTE']);factor=1-q(a['additional_absence_fraction'])
 early_users=F(p['age_3_5'])*q(s['early_takeup']);infant_users=F(p['age_0_2'])*q(s['under3_care_takeup'])
 assert early_users.denominator==1 and infant_users.denominator==1
 care_users=F(p['age_3_5'])*q(s['preschool_care_takeup']);joint_users=F(s['joint_early_care_users'])
 assert 0<=joint_users<=min(early_users,care_users) and early_users+care_users-joint_users<=p['age_3_5'] and care_users.denominator==1
 joint_groups=math.ceil(joint_users/s['early_group']);early_only_groups=math.ceil((early_users-joint_users)/s['early_group']);care_only_groups=math.ceil((care_users-joint_users)/s['early_group'])
 early_groups=joint_groups+early_only_groups;care_groups=joint_groups+care_only_groups;school_groups=math.ceil(F(p['age_6_17'])/s['school_group']);infant_groups=math.ceil(infant_users/s['under3_group'])
 early_contact=F(early_groups)*s['early_hours']*s['education_weeks']
 school_contact=F(school_groups)*s['school_hours']*s['education_weeks']
 prep=(early_contact+school_contact)*q(s['teacher_preparation_fraction'])
 support=F(p['school_support_users'])*s['school_support_weekly_hours']*s['education_weeks']
 under3_care=F(infant_groups)*s['under3_staff_per_group']*s['care_hours']*s['care_weeks']
 preschool_all_staff=F(care_groups)*s['preschool_adults_per_group']*s['care_hours']*s['care_weeks']
 joint_contact=F(joint_groups)*s['early_hours']*s['education_weeks'];early_only_contact=F(early_only_groups)*s['early_hours']*s['education_weeks']
 # One teacher plus one carer during joint learning; two carers outside it.
 preschool_carer=preschool_all_staff-joint_contact+early_only_contact
 adult_care=F(p['adult_care_users'])*s['adult_assessed_mean_weekly_hours']*52
 care=under3_care+preschool_carer+adult_care
 teacher=early_contact+school_contact+prep
 independent_purchase_staff=preschool_all_staff+early_contact*s['preschool_adults_per_group']
 joint_staff=preschool_all_staff+early_only_contact*s['preschool_adults_per_group']
 education={'early_users':early_users,'early_groups':early_groups,'school_groups':school_groups,'early_contact_teacher_hours':early_contact,'school_contact_teacher_hours':school_contact,'teacher_preparation_hours':prep,'teacher_hours':teacher,'individual_support_hours':support,'combined_known_role_hours':teacher+support,
  'teacher_normal_margin':F(a['education_teachers'])*hours-teacher,'support_normal_margin':F(a['education_support'])*hours-support,'support_additional_absence_gap':max(F(0),support-F(a['education_support'])*hours*factor),'aggregate_absence_margin_before_other_tasks':F(a['education_total'])*hours*factor-teacher-support,'unknown_other_education_work':None}
 care_data={'under3_users':infant_users,'under3_group_carer_hours':under3_care,'preschool_carer_hours':preschool_carer,'adult_care_hours':adult_care,'known_partial_care_hours':care,'normal_available_hours':F(a['care_FTE'])*hours,'normal_gap_hours':max(F(0),care-F(a['care_FTE'])*hours),'additional_absence_available_hours':F(a['care_FTE'])*hours*factor,'additional_absence_gap_hours':max(F(0),care-F(a['care_FTE'])*hours*factor),'missing_school_age_and_other_care':None}
 v=d['primary'];n=F(v['unique_episodes']);mental=F(v['mental_episodes']);repro=F(v['reproductive_episodes']);both=F(v['both_labels']);assert 0<=both<=min(mental,repro) and mental+repro-both<=n
 base_contact=n*v['base_contact_minutes']/60;notes=n*v['base_professional_notes_minutes']/60
 mental_time=mental*v['mental_additional_minutes']/60;repro_time=repro*v['reproductive_additional_minutes']/60
 clerical=n*v['clerical_minutes']/60
 primary={'unique_episodes':n,'tagged_service_count_not_unique_episodes':n+mental+repro,'label_overlap':both,'base_role_hours_including_own_notes':base_contact+notes,'mental_role_hours_including_own_incremental_work':mental_time,'reproductive_role_hours_including_own_incremental_work':repro_time,'clerical_hours':clerical,'double_booked_base_minutes_if_tags_bought_independently':(mental+repro)*v['base_contact_minutes'],
  'normal_base_margin':F(a['primary_general_FTE'])*hours-base_contact-notes,'absence_base_gap':max(F(0),base_contact+notes-F(a['primary_general_FTE'])*hours*factor),'normal_reproductive_margin':F(a['primary_reproductive_FTE'])*hours-repro_time,'absence_reproductive_gap':max(F(0),repro_time-F(a['primary_reproductive_FTE'])*hours*factor),'normal_mental_margin':F(a['primary_mental_FTE'])*hours-mental_time,'absence_mental_gap':max(F(0),mental_time-F(a['primary_mental_FTE'])*hours*factor),'actual_competence_or_receipt':None,'all_other_clinical_workload':None}
 calendar=[];election=q(d['shared_admin']['election_hours'])/len(d['shared_admin']['election_months'])
 for month in range(1,13):
  due=clerical/12+(election if month in d['shared_admin']['election_months'] else 0)
  available=F(a['shared_admin_FTE'])*hours/12
  calendar.append({'month':month,'due_hours':due,'ordinary_gap':max(F(0),due-available),'additional_absence_gap':max(F(0),due-available*factor)})
 annual=clerical+q(d['shared_admin']['election_hours']);monthly_peak=max(x['due_hours'] for x in calendar)
 repairs={'care_FTE':max(0,math.ceil(care/(hours*factor))-a['care_FTE']),
  'education_support_FTE':max(0,math.ceil(support/(hours*factor))-a['education_support']),
  'primary_general_FTE':max(0,math.ceil((base_contact+notes)/(hours*factor))-a['primary_general_FTE']),
  'primary_reproductive_FTE':max(0,math.ceil(repro_time/(hours*factor))-a['primary_reproductive_FTE']),
  'two_month_additional_admin_people':max(0,math.ceil(monthly_peak/(hours*factor/12))-a['shared_admin_FTE'])}
 wages=d['illustrative_pay_million'];bill=F(repairs['care_FTE']+repairs['education_support_FTE'])*q(wages['care_support'])+F(repairs['primary_general_FTE']+repairs['primary_reproductive_FTE'])*q(wages['clinical'])+F(repairs['two_month_additional_admin_people'])*q(wages['admin'])*F(len(d['shared_admin']['election_months']),12)
 return clean({'edition':67,'education':education,'care':care_data,'primary':primary,
  'valid_joint_preschool_delivery':{'joint_actual_staff_hours':joint_staff,'independent_duplicate_staff_hours':independent_purchase_staff,'hours_double_booked_if_both_bought_in_full':independent_purchase_staff-joint_staff,'physical_child_care_hours':care_users*s['care_hours']*s['care_weeks'],'included_child_learning_hours':joint_users*s['early_hours']*s['education_weeks'],'early_learning_users':early_users,'childcare_users_independent_of_learning':care_users,'unique_child_service_hours':care_users*s['care_hours']*s['care_weeks']+(early_users-joint_users)*s['early_hours']*s['education_weeks'],'actual_dual_safety_and_quality_verified':None},
  'shared_admin':{'annual_due_hours':annual,'annual_ordinary_capacity':F(a['shared_admin_FTE'])*hours,'annual_ordinary_margin':F(a['shared_admin_FTE'])*hours-annual,'calendar':calendar,'sum_ordinary_positive_period_gaps':sum(x['ordinary_gap'] for x in calendar),'sum_additional_absence_positive_period_gaps':sum(x['additional_absence_gap'] for x in calendar),'actual_cross_role_permission_and_records_separation':None},
  'illustrative_repair':{**repairs,'gross_annual_and_seasonal_salary_floor_million':bill,'preparation_sites_and_source_cost':None,'actual_available_qualified_people':None,'actual_private_work_displaced':None,'changes_are_not_selected_country_headcounts':True},
  'actual_safe_service_standards':None,'full_current_country_cost':None,'actual_operational_readiness':False,'observed_life_improvement':None,'limits':d['limits']})
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
