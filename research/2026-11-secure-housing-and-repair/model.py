"""Authored housing work/material/cash comparisons, never an acquisition or roster."""
from pathlib import Path
import json, math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def annual_program(c, calendar, repair_life=None):
    # Stable-stock equivalent flows, not proof of this year's vintage calendar.
    n=c['retained_reference_structures']; life=c['rebuild']['accepted_service_years']
    repair_life=c['repair']['hypothetical_accepted_service_years'] if repair_life is None else repair_life
    if not calendar>0 or not life>0 or not repair_life>0 or not 0<=c['repair_share_of_stock']<=1:
        raise ValueError('Positive time/service and bounded stock share required')
    if any(sum(c[k]['task_hours_by_role'].values())!=c[k]['task_hours'] for k in ['rebuild','repair']):
        raise ValueError('Role tasks must exhaust event work exactly once')
    frac=c['repair_share_of_stock']; rebuild=n*(1-frac)/life; repair=n*frac/repair_life
    tonnes=rebuild*c['rebuild']['new_input_tonnes']+repair*c['repair']['new_input_tonnes']
    task=rebuild*c['rebuild']['task_hours']+repair*c['repair']['task_hours']
    roles={}
    for role,pay in c['role_annual_pay_CU'].items():
        h=rebuild*c['rebuild']['task_hours_by_role'][role]+repair*c['repair']['task_hours_by_role'][role]
        posts=math.ceil(h/calendar)
        roles[role]=dict(task_hours=h,annual_post_lower_bound=posts,ordinary_payroll_CU=posts*pay)
    posts=sum(x['annual_post_lower_bound'] for x in roles.values())
    # Little's-law average, rounded only as a lower bound; no actual dated starts.
    avg_temp=rebuild*c['rebuild']['temporary_years']+repair*c['repair']['temporary_fraction']*c['repair']['temporary_years']
    bound=math.ceil(avg_temp)
    payroll=sum(x['ordinary_payroll_CU'] for x in roles.values())
    materials=tonnes*c['new_material_quote_CU_per_tonne']
    distinct=rebuild*c['rebuild']['distinct_other_CU']+repair*c['repair']['distinct_other_CU']
    temp=bound*c['temporary_unit_year_quote_CU']
    # None of these assumed quotes identifies a supplier or real funding.
    return dict(rebuild_events_average=rebuild,repair_events_average=repair,
                new_input_tonnes=tonnes,task_hours=task,annual_task_hours_per_post=calendar,
                annual_post_lower_bound=posts,roles=roles,ordinary_payroll_CU=payroll,
                average_temporary_dwelling_demand=avg_temp,temporary_dwelling_lower_bound=bound,
                new_material_quote_CU=materials,distinct_other_quote_CU=distinct,
                temporary_stock_lease_quote_CU=temp,named_total_quote_CU=payroll+materials+distinct+temp,
                actual_safe_repair_acceptance=None,actual_roster=None,actual_temporary_stock=None,
                qualified_national_saving=False)


def rent_case(c, debt_fraction, remaining_years=None):
    years=c['authored_remaining_service_years'] if remaining_years is None else remaining_years
    if years<=0 or not 0<=c['vacancy_fraction']<1 or not 0<=debt_fraction<=1:raise ValueError('Invalid service or collected-rent basis')
    N=c['homes']; price=c['structure_acquisition_allocation_CU']+c['land_acquisition_allocation_CU']
    acquisition=N*price; debt=debt_fraction*acquisition; grant=acquisition-debt
    r=c['loan_rate']; T=c['loan_years']
    payment=debt/T if r==0 else debt*r/(1-(1+r)**(-T))
    interest=debt*r; principal=payment-interest
    upkeep=N*c['routine_upkeep_CU']; management=N*c['management_CU']
    levy=N*c['site_levy_CU']; renewal=N*c['structure_acquisition_allocation_CU']/years
    opex=upkeep+management+levy
    full_cost=opex+renewal+interest
    cash_need=opex+renewal+payment
    occupied=N*(1-c['vacancy_fraction'])
    return dict(homes=N,expected_occupied_homes=occupied,total_structures_added=0,
                acquisition_payment_CU=acquisition,appropriated_capital_grant_required_CU=grant,
                new_debt_required_CU=debt,loan_annual_payment_CU=payment,
                year1_interest_CU=interest,year1_principal_CU=principal,
                upkeep_CU=upkeep,management_CU=management,site_levy_CU=levy,
                annual_capital_consumption_reference_CU=renewal,annual_cash_renewal_deposit_CU=renewal,
                year1_economic_cost_CU=full_cost,year1_cash_requirement_including_held_reserve_CU=cash_need,
                year1_actual_outflow_excluding_held_reserve_CU=opex+payment,
                monthly_cash_cover_rent_per_occupied_home_CU=cash_need/occupied/12,
                monthly_economic_cost_per_occupied_home_CU=full_cost/occupied/12,
                remaining_service_years_hypothesis=years,
                loan_matures_within_current_service_hypothesis=(debt==0 or T<=years),
                full_lifetime_finance_qualified=False,actual_land_or_equity_quote=None,
                actual_grant_or_debt_receipt=None,individual_affordability=None)


def quarterly_peak(starts,duration_months):
    if len(starts)!=4 or not 0<duration_months<=12:raise ValueError('Unsupported quarterly pattern')
    # Repeated completed example year, with prior-year carryover at month0.
    occupied=[]
    for month in range(12):
        occupied.append(sum(n for year in [-1,0] for q,n in enumerate(starts)
                            if year*12+q*3<=month<year*12+q*3+duration_months))
    return occupied


def calculate(c=None):
    c=c or json.loads((HERE/'inputs.json').read_text())
    tw=json.loads((ROOT/c['frozen_tw_results']).read_text())
    times={x['calendar']['id']:x['calendar']['deployable_task_hours'] for x in tw['cases']}
    cases={}
    for label, hours in [('selected32',times['selected32_five_days']),('rival40',times['rival40_five_days'])]:
        repair=annual_program(c['program'],hours)
        old=json.loads(json.dumps(c['program']));old['repair_share_of_stock']=0
        cases[label]=dict(all_rebuild=annual_program(old,hours),repair40=repair,
                          repair20=annual_program(c['program'],hours,20))
    a=cases['selected32']['all_rebuild']['roles'];b=cases['selected32']['repair40']['roles']
    retained_extra=(a['craft']['annual_post_lower_bound']-b['craft']['annual_post_lower_bound'])*c['program']['role_annual_pay_CU']['craft']
    continuity=dict(hypothetical_retained_craft_posts=a['craft']['annual_post_lower_bound'],
                    additional_current_payroll_if_all_retained_CU=retained_extra,
                    extra_design_posts_needed=b['design']['annual_post_lower_bound']-a['design']['annual_post_lower_bound'],
                    extra_independent_posts_needed=b['independent_technical']['annual_post_lower_bound']-a['independent_technical']['annual_post_lower_bound'],
                    actual_retained_or_reassigned_workers=None,capitalized_idle_work_CU=0)
    finance={
      'grant_paid20_remaining':rent_case(c['conversion'],0),
      'debt_paid20_remaining':rent_case(c['conversion'],1),
      'grant_paid40_remaining_sensitivity':rent_case(c['conversion'],0,40),
      'debt_paid40_remaining_sensitivity':rent_case(c['conversion'],1,40)}
    q=c['quarterly_counterexample']
    alltemp=quarterly_peak(q['all_rebuild_starts'],6)
    rebuildtemp=quarterly_peak(q['repair_path_rebuild_starts'],6)
    repairtemp=quarterly_peak(q['moving_repair_starts'],2)
    temp=dict(all_monthly_dwellings=alltemp,repair_monthly_dwellings=[a+b for a,b in zip(rebuildtemp,repairtemp)],
              all_peak=max(alltemp),repair_peak=max(a+b for a,b in zip(rebuildtemp,repairtemp)),
              repair_moves=sum(q['moving_repair_starts']),
              additional_named_lease_CU_above_average_bound=(max(a+b for a,b in zip(rebuildtemp,repairtemp))-cases['selected32']['repair40']['temporary_dwelling_lower_bound'])*c['program']['temporary_unit_year_quote_CU'],
              actual_dated_local_plan=None,actual_outage_or_accessible_capacity=None)
    p=c['frozen_housing']; s=p['private_units']+p['public_units']
    oldrent=(s*(p['structure_CU']/p['life_years']+p['upkeep_CU'])+
             p['private_units']*p['land_CU']*p['levy_rate'])
    return dict(edition=91,status='Authored conditional housing subset, not current national closure',
                retained_reference_structures=s,reference_persons=100000,
                actual_occupied_structures_or_household_choices=None,
                old_private_rent_CU=p['private_units']*(p['structure_CU']/p['life_years']+p['upkeep_CU']+p['land_CU']*p['levy_rate']),
                old_public_rent_CU=p['public_units']*(p['structure_CU']/p['life_years']+p['upkeep_CU']),
                old_total_rent_CU=oldrent,old_explicit_profit_or_finance_margin_CU=0,
                old_margin_zero_is_observed_landlord_profit=False,
                programs=cases,quarterly_counterexample=temp,workforce_continuity=continuity,conversion=finance,
                four_year_equivalent_schedule=[dict(rebuild=n,repair=1875-n) for n in [469,469,469,468]],
                actual={k:None for k in ['occupancy','private_space','title_priority','acquisition_price','qualified_trade_crews','safe_repair_life','material_supply','temporary_dwellings','sources','independent_review','participation','enactment','delivered_remedy','better_lives']})


if __name__=='__main__':
    (HERE/'results.json').write_text(json.dumps(calculate(),indent=2)+'\n')
