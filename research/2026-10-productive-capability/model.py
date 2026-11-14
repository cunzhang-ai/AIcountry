"""A paid capability pipeline, not a GDP/whole-country feasibility forecast."""
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

def budget(d,delay=0):
 years=8+delay;tracks=d['tracks'];rows=[];new=d['new_facilities'];upfront=q(new['capital'])
 core=sum(d['opening_roles'].values());base_people=sum(t['people'] for t in d['old_role_training'].values())
 for year in range(1,years+1):
  trainee=F(0);instructors=F(0);graduate=F(0);bridges=F(0);head=F(0);graduates={};active_training=False
  for t in tracks:
   duration=t['years']+(delay if t['role']=='clinical' else 0)
   n=t['intake'];g=math.floor(F(n)*q(d['pass_fraction']));mentors=math.ceil(F(n)/d['students_per_instructor'])
   pay=q(t['prior_annual_pay_million']);mpay=q(t['instructor_annual_pay_million'])
   if year<=duration:
    trainee+=n*pay;instructors+=mentors*mpay;head+=n+mentors;active_training=True
   else:
    graduate+=g*pay;head+=g
    if year==duration+1:
     bridges+=(n-g)*pay*q(d['bridge_year_fraction'])+mentors*mpay*q(d['bridge_year_fraction'])
     head+=(n-g+mentors)*q(d['bridge_year_fraction'])
   graduates[t['name']]=g if year>duration else 0
  old=d['old_transition'];old_bill=q(old['annual_staff_pay'])+ (q(old['annual_training'])+q(old['capital_total'])/old['commission_year'] if year<=old['commission_year'] else q(old['annual_maintenance']))
  maintenance=q(new['annual_maintenance']);replacement=q(new['capital'])*q(new['depreciation_rate'])
  other_training=q(d['annual_new_nonwage_training']) if active_training else F(0)
  old_replacement=q(old['capital_total'])*q(old['operating_capital_replacement_rate']) if year>old['commission_year'] else F(0)
  old_bill+=old_replacement
  new_bill=trainee+instructors+graduate+bridges+maintenance+replacement+other_training
  rows.append({'year':year,'trainee_income':trainee,'dedicated_instructor_pay':instructors,'qualified_pay':graduate,'minimum_return_bridges':bridges,'facility_maintenance':maintenance,'facility_gross_replacement':replacement,'other_training_inputs':other_training,'new_pipeline_total':new_bill,'old_enabling_total':old_bill,'old_project_gross_replacement':old_replacement,'combined_due':new_bill+old_bill,'new_paid_person_years':head,'base_paid_programme_people':base_people,'public_paid_person_years_including_core':core+base_people+head,'people_not_assigned_to_public_paid_work':d['total_reference_workforce']-(core+base_people+head),'new_graduates_available_at_start':graduates})
 total=upfront+sum((r['combined_due'] for r in rows),F(0))
 return {'horizon':years,'upfront_training_facilities':upfront,'annual':rows,'known_combined_bills':total,'conditional_prior_source_to_keep_buffer':total+q(d['cash_buffer']),'known_new_pipeline_bills':upfront+sum((r['new_pipeline_total'] for r in rows),F(0)),'qualified_target_annual_pay_after_training':sum((math.floor(F(t['intake'])*q(d['pass_fraction']))*q(t['prior_annual_pay_million']) for t in tracks),F(0)),'actual_whole_country_cost':None,'actual_renewal_pipeline_after_horizon':None,'actual_readiness':False}

def capacity(d,teacher_fraction=F(1),facility=True,delay=0):
 years=8+delay;tracks=[]
 for t in d['tracks']:
  mentors=math.ceil(F(t['intake'])/d['students_per_instructor'])
  slots=math.floor(F(mentors)*teacher_fraction*d['students_per_instructor']) if facility else 0
  admitted=min(t['intake'],slots);grads=math.floor(F(admitted)*q(d['pass_fraction']))
  tracks.append({'name':t['name'],'role':t['role'],'intake':t['intake'],'instructors_if_qualified':mentors,'admitted_by_declared_capacity':admitted,'unplaced_at_start':t['intake']-admitted,'graduates_if_qualified':grads,'duration':t['years']+(delay if t['role']=='clinical' else 0)})
 rows=[]
 for year in range(1,years+1):
  staff={k:F(v) for k,v in d['opening_roles'].items()}
  for role,entry in d['old_role_training'].items():
   if year>entry['years']:staff[role]+=entry['people']
  for t in tracks:
   if year>t['duration']:staff[t['role']]+=t['graduates_if_qualified']
  losses={k:max(F(0),F(v)-staff[k]*F('0.9')) for k,v in d['postcommission_role_requirements'].items()}
  rows.append({'year':year,'qualified_roles_if_all_sources_valid':staff,'gaps_against_postproject_10_percent_loss_target':losses})
 return {'tracks':tracks,'years':rows,'first_year_stated_loss_target_fits':next((r['year'] for r in rows if all(v==0 for v in r['gaps_against_postproject_10_percent_loss_target'].values())),None),'additional_finance_for_unplaced_or_revised_completion':None,'actual_qualification_or_delivery':None}

def sources(b,opening,buffer):
 cumulative=b['upfront_training_facilities'];rows=[]
 for r in b['annual']:
  cumulative+=r['combined_due']
  rows.append({'year':r['year'],'cumulative_bills':cumulative,'unallocated_bill_finance_gap':max(F(0),cumulative-opening),'additional_source_needed_to_preserve_buffer':max(F(0),cumulative+buffer-opening)})
 return {'conditional_opening_source':opening,'schedule':rows,'last_bill_finance_gap':rows[-1]['unallocated_bill_finance_gap'],'last_gap_including_buffer':rows[-1]['additional_source_needed_to_preserve_buffer'],'actual_source_or_appropriation':None,'payment_priority_or_actual_receipt':'Not assigned by this arithmetic; prior E/T and elected-law duties continue'}

def validate_inputs(d):
 allowed={'edition','date','scope','pinned_sources','cash_buffer','old_prior_source','old_transition','pass_fraction','students_per_instructor','bridge_year_fraction','annual_new_nonwage_training','new_facilities','tracks','opening_roles','old_role_training','postcommission_role_requirements','limits','total_reference_workforce'}
 unknown=set(d)-allowed
 if unknown:raise ValueError('Unsupported input semantics: '+', '.join(sorted(unknown)))
 assert 0<=q(d['pass_fraction'])<=1 and d['students_per_instructor']>0
 assert 0<=q(d['bridge_year_fraction'])<=1
 assert len({t['name'] for t in d['tracks']})==len(d['tracks'])
 fields={'name','role','intake','years','prior_annual_pay_million','instructor_annual_pay_million'}
 for t in d['tracks']:
  if set(t)-fields:raise ValueError('Unsupported track semantics')
  assert type(t['intake']) is int and t['intake']>=0
  assert type(t['years']) is int and t['years']>0
  assert q(t['prior_annual_pay_million'])>=0 and q(t['instructor_annual_pay_million'])>=0
  assert t['role'] in d['opening_roles']

def calculate():
 d=json.loads((HERE/'inputs.json').read_text());validate_inputs(d)
 for p,h in d['pinned_sources'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 base=budget(d);delayed=budget(d,2)
 full=base['conditional_prior_source_to_keep_buffer'];wages_only=q(d['old_prior_source'])+base['qualified_target_annual_pay_after_training']*8
 o=d['old_transition'];known_continuing=q(o['annual_staff_pay'])+q(o['annual_maintenance'])+q(o['capital_total'])*q(o['operating_capital_replacement_rate'])+base['qualified_target_annual_pay_after_training']+q(d['new_facilities']['annual_maintenance'])+q(d['new_facilities']['capital'])*q(d['new_facilities']['depreciation_rate'])
 return clean({'edition':66,'normal_paid_pipeline':base,'two_year_clinical_delay':delayed,'normal_source_schedule':sources(base,full,q(d['cash_buffer'])),'posthire_wages_only_source_schedule':sources(base,wages_only,q(d['cash_buffer'])),'delayed_with_only_normal_source':sources(delayed,full,q(d['cash_buffer'])),'capacity_normal':capacity(d),'capacity_10_percent_instructor_loss':capacity(d,F('.9')),'capacity_unreceived_facility':capacity(d,facility=False),'capacity_two_year_clinical_delay':capacity(d,delay=2),'known_annual_continuing_bill_excluding_renewal_and_baseline':known_continuing,'full_current_function_costs':None,'new_training_physical_inputs':None,'actual_AI_net_capacity':None,'actual_productivity_gain':None,'actual_private_job_or_output_replacement':None,'actual_readiness':False,'limits':d['limits']})
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
