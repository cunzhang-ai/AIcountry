"""Declared amount, upper-workload and Gregorian-date probes; no legal inference."""
from pathlib import Path
from decimal import Decimal,ROUND_FLOOR,ROUND_CEILING
from datetime import date,timedelta
import json,math
HERE=Path(__file__).resolve().parent
PARTITION='distinct eligible natural people; one actual territorial track each where assigned; no account or AI copies'
SCOPE='independent invented CU/person/date fixtures; not one real election or source budget'
def keys(x,n):
 if not isinstance(x,dict) or set(x)!=set(n.split()):raise ValueError('Unknown/missing semantics')
def num(x,positive=False):
 if type(x) not in (int,float) or not math.isfinite(x) or x<0 or (positive and x<=0):raise ValueError('Unknown/invalid number is not zero')
 return Decimal(str(x))
def count(x,positive=False):
 num(x,positive)
 if type(x) is not int:raise ValueError('Person count not integer')
 return x
def counts(x,positive=False):
 if not isinstance(x,list) or not x:raise ValueError('Missing actual track partition')
 return [count(v,positive) for v in x]
def day(x):
 if not isinstance(x,str):raise ValueError('Missing date')
 try:d=date.fromisoformat(x)
 except (ValueError,TypeError):raise ValueError('Invalid Gregorian date')
 if d.isoformat()!=x:raise ValueError('Noncanonical date')
 return d
def floor(x):return int(x.to_integral_value(rounding=ROUND_FLOOR))
def ceil(x):return int(x.to_integral_value(rounding=ROUND_CEILING))
def cash(x):return float(x)
def calculate(c=None):
 if c is None:c=json.loads((HERE/'inputs.json').read_text())
 keys(c,'edition declared_scope B_CU minor_unit_CU N_fixture call_national call_territories cutoff_people_national cutoff_people_territories eligible_credit_national eligible_credit_territories requested_one_principal_national requested_one_principal_first_territory declared_person_partition printing_staff_fixture growth_fixture fine_quantity calendar')
 if c['edition']!=101 or type(c['edition']) is not int or c['declared_scope']!=SCOPE or c['declared_person_partition']!=PARTITION:raise ValueError('Different fixture meaning')
 B=num(c['B_CU'],True);q=num(c['minor_unit_CU'],True);v=q*floor(B/(200*q))
 if v<=0:raise ValueError('Credit rounds to zero: revise scheme, not a funded cash route')
 N=count(c['N_fixture'],True);E0=count(c['call_national'],True);ds=counts(c['call_territories'],True)
 R=count(c['cutoff_people_national'],True);rs=counts(c['cutoff_people_territories'],True)
 E=count(c['eligible_credit_national']);es=counts(c['eligible_credit_territories'])
 if len(ds)!=len(rs) or len(ds)!=len(es) or len(ds)>N//3 or sum(ds)>E0 or sum(rs)>R or sum(es)>E:raise ValueError('Different legal-person/territory partition')
 wanted=count(c['requested_one_principal_national']);wanted_d=count(c['requested_one_principal_first_territory'])
 if wanted>E or wanted_d>es[0]:raise ValueError('Requested assignments exceed distinct eligible fixture people')
 s=(E0+99)//100;sd=[(d+99)//100 for d in ds];U=2*R//s;ud=[2*r//t for r,t in zip(rs,sd)]
 K=2*E0//5;kd=[2*d//5 for d in ds];paid=min(wanted,K);paid_d=min(wanted_d,kd[0])
 base=v*(E0+sum(ds));reserve=q*ceil(base*Decimal('.1')/q);maximum=v*(E+sum(es))
 out={'credits':{'nominal_each_CU':cash(B/200),'actual_each_CU':cash(v),'call_source_base_CU':cash(base),'planning_growth_reserve_CU':cash(reserve),'maximum_cash_by_actual_fixture_entitlements_CU':cash(maximum),'source_gap_CU':cash(max(Decimal(0),maximum-base-reserve)),'principal_national_whole_credit_cap':K,'principal_national_paid_cap_CU':cash(v*K),'principal_first_territory_paid_cap_CU':cash(v*kd[0]),'requested_one_principal_national_CU':cash(v*wanted),'allowed_one_principal_national_CU':cash(v*paid),'unpaid_cap_residue_national_CU':cash(v*(wanted-paid)),'allowed_first_territory_CU':cash(v*paid_d),'no_whole_credit_track':K==0 or any(k==0 for k in kd)},'field':{'national_threshold':s,'territorial_thresholds':sd,'national_endorsement_supply_upper':U,'territorial_endorsement_supply_uppers':ud,'actual_qualified_field_or_source_independence':None}}
 f=c['printing_staff_fixture'];keys(f,'platform_words words_per_page assumed_words_per_pool_name hours_per_nomination_including_source_check paid_hours_per_worker_in_decision_peak decision_calendar_days availability_fraction')
 for k in ['platform_words','words_per_page','assumed_words_per_pool_name','decision_calendar_days']:count(f[k],True)
 for k in ['hours_per_nomination_including_source_check','paid_hours_per_worker_in_decision_peak','availability_fraction']:num(f[k],True)
 if f['availability_fraction']>1:raise ValueError('Invalid paid availability')
 # Weighted by actual hypothetical territory people; full printed directory is a separate worst-case request.
 platform_pages=sum(e*(((U+u)*f['platform_words']+f['words_per_page']-1)//f['words_per_page']) for e,u in zip(es,ud))
 platform_pages+=(E-sum(es))*math.ceil(U*f['platform_words']/f['words_per_page'])
 directory_pages=sum(e*math.ceil(((U+u)*f['platform_words']+(U*2*N+u)*f['assumed_words_per_pool_name'])/f['words_per_page']) for e,u in zip(es,ud))
 directory_pages+=(E-sum(es))*math.ceil((U*f['platform_words']+U*2*N*f['assumed_words_per_pool_name'])/f['words_per_page'])
 cases=U+sum(ud);hours=cases*f['hours_per_nomination_including_source_check'];workerhours=f['paid_hours_per_worker_in_decision_peak']*f['availability_fraction']
 out['workload']={'platform_text_pages_if_each_territorial_elector_requests_all':platform_pages,'platform_and_max2N_names_pages_same_request_fixture':directory_pages,'max_list_pool_names_from2N_bound':U*2*N,'presentation_minutes_all_tracks':cases*5,'minimum_QA_minutes_all_tracks':cases*2,'single_joined_forum_minutes_all_tracks':cases*7,'case_count_endorsement_bound':cases,'assumed_case_hours':hours,'assumed_minimum_available_workers_for5day_peak':math.ceil(hours/workerhours),'actual_names_prices_print_demand_qualified_roster_or_audience':None}
 g=c['growth_fixture'];keys(g,'cutoff_and_credit_people_national cutoff_and_credit_people_territories');ge=count(g['cutoff_and_credit_people_national'],True);gd=counts(g['cutoff_and_credit_people_territories'],True)
 if len(gd)!=len(ds) or sum(gd)>ge:raise ValueError('Different growth people/track partition')
 gm=v*(ge+sum(gd))
 out['growth']={'national_field_upper':2*ge//s,'territorial_field_uppers':[2*x//t for x,t in zip(gd,sd)],'maximum_credit_cash_CU':cash(gm),'call_plan_and_reserve_CU':cash(base+reserve),'source_gap_CU':cash(max(Decimal(0),gm-base-reserve)),'unchanged_principal_national_cap_CU':cash(v*K),'actual_roll_growth_or_appropriation':None}
 out['private_quantity']={'one_donor_one_principal_nominal_CU':cash(B/2),'one_donor_all_principals_nominal_CU':cash(B),'national_spend_cap_CU':cash(B*(6+Decimal(E0)/200)),'first_district_spend_cap_CU':cash(B*(1+Decimal(ds[0])/200)),'independent_national_spend_cap_CU':cash(B*E0/1000),'independent_first_district_spend_cap_CU':cash(B*ds[0]/1000),'actual_source_or_controller_or_violation':None}
 a=c['fine_quantity'];keys(a,'defendant_verified_revenue proved_net_illicit_gain proved_one_flow_unlawful_campaign_value')
 for x in a.values():num(x)
 old=max(num(a['defendant_verified_revenue'])*Decimal('.05'),num(a['proved_net_illicit_gain'])*2);new=max(old,num(a['proved_one_flow_unlawful_campaign_value'])*2)
 out['fine_quantity']={'old_middle_body_upper_CU':cash(old),'explicit_VD12_upper_CU':cash(new),'wrong_same_flow_receipt_plus_spend_upper_CU':cash(num(a['proved_one_flow_unlawful_campaign_value'])*4),'actual_fault_or_court_or_punishment':None}
 a=c['calendar'];keys(a,'final_P annulment_J late_cap_notice_days_before_V');P=day(a['final_P']);J=day(a['annulment_J']);V=P-timedelta(days=14);before=lambda n:(V-timedelta(days=n)).isoformat();n=count(a['late_cap_notice_days_before_V'])
 notice=V-timedelta(days=n);redirect=min(V-timedelta(days=3),max(V-timedelta(days=10),notice+timedelta(days=1)))
 out['calendar']={'P':P.isoformat(),'V':V.isoformat(),'ordinary_call_latest':before(90),'early_call_latest':before(60),'nomination_freeze':before(40),'final_decision_outer':before(35),'guide_48h_midnight_date_fixture':before(33),'historical_proof_close':before(30),'production_and_actual_forum_due':before(21),'ordinary_credit_close':before(14),'ordinary_last_credit_48h_date_fixture':before(12),'correction_outer':before(3),'late_cap_notice':notice.isoformat(),'latest_correction_if_notice_allows':redirect.isoformat(),'notice_has_remaining_correction_time':notice<redirect,'if_timely_corrected_48h_pay_date':(redirect+timedelta(days=2)).isoformat() if notice<redirect else None,'repeat_final_P':(J+timedelta(days=90)).isoformat(),'repeat_V':(J+timedelta(days=76)).isoformat(),'repeat_prepare_days':76,'repeat_freeze':(J+timedelta(days=36)).isoformat(),'repeat_guide_midnight_date_fixture':(J+timedelta(days=43)).isoformat(),'actual_usable_notice_UTC48h_or_court_or_poll':None}
 out['actual']={k:None for k in ['public_mandate','legal_adoption','original_electorate_and_map','qualified_independent_review','affected_participation','staffed_payment_custody_courts','source_cash_and_FX','received_opportunity_and_outcomes']}
 return out
if __name__=='__main__':(HERE/'results.json').write_text(json.dumps(calculate(),indent=2,allow_nan=False)+'\n')
