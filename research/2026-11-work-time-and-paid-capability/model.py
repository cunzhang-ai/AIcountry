"""Paid calendars and unchanged-care comparisons, not an economic forecast."""
from pathlib import Path
import copy
import hashlib
import json
import math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def calendar(c,p):
    h=p['weekly_hours'];days=p['days_per_week'];daily=h/days
    scheduled=h*(c['weeks']-c['annual_leave_weeks']-c['public_flexible_holiday_weeks'])
    if daily<=6:raise ValueError('This fixture assumes a paid break on every workday; shorter-day patterns need their own ledger')
    breaks=scheduled/daily*c['paid_break_hours_per_day']
    before_loss=scheduled-breaks-c['protected_learning_hours']
    if before_loss<=0:raise ValueError('No positive task time; do not force closure')
    return dict(id=p['id'],weekly_hours=h,days_per_week=days,daily_paid_hours=daily,
                annual_normal_paid_hours=h*c['weeks'],scheduled_after_leave_and_holidays=scheduled,
                paid_breaks=breaks,protected_learning=c['protected_learning_hours'],
                task_before_loss=before_loss,unexpected_absence=before_loss*c['unexpected_absence_fraction'],
                deployable_task_hours=before_loss*(1-c['unexpected_absence_fraction']),
                actual_individual_roster=None)


def care_case(cfg,hours,pay,pro_pay):
    d=cfg['days'];notes=cfg['notes_fraction']
    contact=cfg['people']*d*cfg['daily_contact_hours_per_person']
    reference=d*cfg['central_routes_day']*(cfg['central_contact_hours_route']*(1+notes)+cfg['central_travel_hours_route'])
    local=d*cfg['local_routes_day']*(cfg['local_contact_hours_route']*(1+notes)+cfg['local_travel_hours_route']+cfg['extra_worker_commute_hours_route'])
    refposts=math.ceil(reference/hours);taskposts=math.ceil(local/hours)
    paid_local=taskposts+cfg['local_reserve_posts']
    fitout=cfg['microbases']*cfg['fitout_per_base_CU'];renewal=fitout/cfg['fitout_life_years']
    newop=cfg['microbases']*(cfg['lease_per_base_year_CU']+cfg['maintenance_per_base_year_CU'])
    support=cfg['dispatch_stock_posts']*pay+cfg['independent_review_paid_fraction']*pro_pay
    refpay=refposts*pay
    localpay=paid_local*pay
    full=localpay+support+newop+renewal
    return dict(people=cfg['people'],contact_hours=contact,notes_hours=contact*notes,
                central_task_hours=reference,local_task_hours=local,
                central_posts=refposts,local_task_posts=taskposts,
                local_paid_reserve_posts=cfg['local_reserve_posts'],local_frontline_posts=paid_local,
                new_support_pay_CU=support,new_operating_premises_CU=newop,
                fitout_initial_CU=fitout,fitout_CFC_and_renewal_reserve_CU=renewal,
                central_named_recurring_cost_CU=refpay,local_named_full_recurring_cost_CU=full,
                avoided_vacancies_named_saving_CU=refpay-full,
                local_actual_first_year_outflow_CU=full-renewal+fitout,
                local_first_year_funding_including_held_renewal_CU=full+fitout,
                retained_staff_named_recurring_cost_CU=max(refposts,paid_local)*pay+support+newop+renewal,
                review_required=cfg['independent_review_task_hours'],
                review_capacity=cfg['independent_review_paid_fraction']*hours,
                releaseable_task_hours_if_staff_retained=max(0,refposts-paid_local)*hours,
                unpriced=['fuel/vehicles and actual route access','common retained depot/other unchanged inputs','qualification/learning/overlap/lease exit','tax/benefit/producer effects','additional clinical or weekend care','actual source'],
                actual_offer_or_saving=None)


def rest_gaps(events):
    """Hours in an authored bounded scenario; actual sector/rolling-week review separate."""
    rows=sorted(events,key=lambda x:x[0]);gaps=[]
    for a,b in zip(rows,rows[1:]):
        if b[0]<a[1]:raise ValueError('Overlapping attributed human work')
        gaps.append(b[0]-a[1])
    return gaps


def minimum_rate(previous,median_hour,cpi,ratio=.6):
    if not all(math.isfinite(x) and x>0 for x in [previous,median_hour,cpi,ratio]):
        raise ValueError('Missing/unsupported wage-index evidence; do not invent a rate')
    return max(previous,previous*cpi,ratio*median_hour)


def calculate():
    c=json.loads((HERE/'inputs.json').read_text())
    for n,h in c['pinned_support'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    w=json.loads((ROOT/'2026-10-full-offer-resource-estimate/workloads.json').read_text())
    under=next(x for x in w['rows'] if x['id']=='under3');demand=math.prod(under['factors'])
    calendars=[calendar(c['calendar'],p) for p in c['calendar']['cases']]
    rows=[]
    for p in calendars:
        H=p['deployable_task_hours'];posts=math.ceil(demand/H)
        care=care_case(c['local_care'],H,c['frontline_annual_pay_CU'],c['professional_annual_pay_CU'])
        daily_tasks=p['daily_paid_hours']-c['calendar']['paid_break_hours_per_day']
        central_route=c['local_care']['central_contact_hours_route']*(1+c['local_care']['notes_fraction'])+c['local_care']['central_travel_hours_route']
        local_route=c['local_care']['local_contact_hours_route']*(1+c['local_care']['notes_fraction'])+c['local_care']['local_travel_hours_route']+c['local_care']['extra_worker_commute_hours_route']
        care['intact_central_route_fits_normal_day']=central_route<=daily_tasks
        care['intact_local_route_fits_normal_day']=local_route<=daily_tasks
        care['central_route_task_hours']=central_route;care['local_route_task_hours']=local_route
        care['normal_day_task_ceiling']=daily_tasks
        care['qualified_executable_saving']=False
        care['whole_route_day_post_bounds']=dict(central=math.ceil(c['local_care']['days']*c['local_care']['central_routes_day']/(H/daily_tasks)),local=math.ceil(c['local_care']['days']*c['local_care']['local_routes_day']/(H/daily_tasks)),qualification='One intact route/person/day; annual-day bound only, not a qualified local roster') if central_route<=daily_tasks and local_route<=daily_tasks else None
        rows.append(dict(calendar=p,under3=dict(task_hours=demand,posts=posts,
                     annual_frontline_pay_CU=posts*c['frontline_annual_pay_CU'],
                     offered_hours_week=40,offered_weeks=48,actual_safe_local_roster=None),
                     continuous_post_annual_bound=math.ceil(8760/H),
                     care=care))
    p=c['minimum_pay'];median_hour=p['median_full_time_annual_example_CU']/(p['normal_weekly_hours']*52)
    floor=median_hour*p['ratio_of_independent_median_hourly']
    payrows=[]
    for weekly in [32,16]:
        contracted=c['minimum_pay']['low_paid_example_annual_CU']
        required=floor*weekly*52
        payrows.append(dict(normal_weekly_hours=weekly,current_annual_pay_CU=contracted,
                            required_annual_cash_minimum_CU=required,
                            needed_uplift_CU=max(0,required-contracted)))
    med=c['medical_example'];weeklypay=med['usual_annual_pay_CU']/52
    # Five-day authored work pattern only. Existing salary/insurance is matched
    # once; incidence/frequency and prior source-law conditions are not inferred.
    employer_weeks=med['employer_full_pay_first_normal_weeks']
    public_weekly_basis=min(med['usual_annual_pay_CU'],p['median_full_time_annual_example_CU'])/52
    return dict(edition=90,status=c['status'],cases=rows,
                minimum_pay=dict(independent_median_hour_example_CU=median_hour,
                                 minimum_hour_example_CU=floor,person_examples=payrows,
                                 national_uplift_or_tax_gain=None,
                                 annual_index_examples=[dict(previous=a,median_hour=b,cpi=v,new_rate=minimum_rate(a,b,v)) for a,b,v in [(10,18,1.03),(11,17,.98),(11,17,1.10)]]),
                learning=dict(protected_hours=64,clinical_participant_hours=8000,
                              distinct_independent_review_hours=1000,
                              removable_same_employee_matched_hours_only=8000,
                              unknown_teacher_preparation_training_split=None,
                              actual_participant_membership_and_places=None),
                medical_example=dict(employer_first_period_CU=weeklypay*employer_weeks,
                                     public_remaining_episode_CU=public_weekly_basis*med['public_replacement_fraction_after_employer_period']*(med['maximum_episode_weeks']-employer_weeks),
                                     usual_pay_for_episode_CU=weeklypay*med['maximum_episode_weeks'],
                                     public_basis_cap_per_person_CU=p['median_full_time_annual_example_CU'],
                                     initial_period_normal_weeks=employer_weeks,
                                     no_double_salary_or_public_receipt=True,
                                     actual_claims_or_source=None),
                rest_counterexample=dict(day_shift=[9,17],night_requested_human_review=[23,23.5],next_shift=[33,41],
                                         actual_gap_after_review=33-23.5,
                                         insufficient_daily_rest=(33-23.5)<11,
                                         asynchronous_AI_runtime_alone_is_not_human_work=True,
                                         actual_roster_or_authorized_exception=None),
                actual=c['actual'])


if __name__=='__main__':
    (HERE/'results.json').write_text(json.dumps(calculate(),indent=2)+'\n')
    print('Wrote paid-time, unchanged-care, minimum-pay, learning and sickness comparisons.')
