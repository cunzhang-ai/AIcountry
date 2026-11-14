"""Authored bounds and illustrative thresholds, never a live governing system."""
from pathlib import Path
import json,math
import context
HERE=Path(__file__).resolve().parent

def mobility(c):
    for k in ['residents','returns_per_week','weeks','return_km','speed_kmh','annual_task_hours']:
        if c[k]<=0:raise ValueError('Positive defined quantity required: '+k)
    out=[];person_returns=c['residents']*c['returns_per_week'];ppkm=person_returns*c['return_km']
    for p in c['cases']:
        if p['passengers']<=0 or p['empty_fraction']<0:raise ValueError('Unsupported packing/deadhead')
        runs=person_returns/p['passengers'];km=runs*c['return_km']*(1+p['empty_fraction'])
        h=km/c['speed_kmh']+runs*c['handling_hours_per_return'];annual=h*c['weeks']
        posts=math.ceil(annual/c['annual_task_hours']);paid=posts+p['reserve_posts']+p['dispatch_posts']
        fuel=km*c['weeks']*p['fuel_litre_km']*c['fuel_quote_CU_litre']
        maintenance=p['fleet']*p['maintenance_CU_vehicle'];renewal=p['fleet']*p['vehicle_quote_CU']/p['life_years']
        out.append(dict(id=p['id'],person_returns_week=person_returns,passenger_km_year=ppkm*c['weeks'],
            vehicle_returns_week=runs,vehicle_km_week=km,task_hours_week=h,task_hours_year=annual,
            task_driver_post_bound=posts,reserve_posts=p['reserve_posts'],dispatch_posts=p['dispatch_posts'],
            fleet_hypothesis=p['fleet'],initial_fleet_quote_CU=p['fleet']*p['vehicle_quote_CU'],
            fuel_quote_CU_year=fuel,maintenance_quote_CU_year=maintenance,renewal_cash_quote_CU_year=renewal,
            named_recurring_subtotal_CU=paid*c['wage_quote_CU']+fuel+maintenance+renewal+p['premises_CU'],
            omitted_costs=['finance','insurance','qualification','inspection','access construction','tax','other suppliers','constrained waiting beyond named handling'],
            qualified_roster_or_fleet=False,actual_offer_or_source=None))
    country=[]
    for distance in c['distances_return_km']:
        for uptake in c['usage_cases']:
            returns=c['country_people']*c['returns_per_week']*c['weeks']*uptake
            demand=returns*distance
            country.append(dict(return_km=distance,usage_fraction=uptake,ordinary_person_returns_year=returns,
                ordinary_passenger_km=demand,old_PA_after_ordinary_passenger_km=c['old_PA_passenger_km']-demand,
                necessary_other_trips_included=False,accepted_capacity=False))
    x=c['wheelchair_peak'];first=x['ready_minute']+x['boarding_minutes']+x['oneway_minutes']
    next_arrival=first+x['oneway_minutes']+x['boarding_minutes']+x['oneway_minutes']
    # Specific single-space, common-ready-time test; not a general routing algorithm.
    first_wave_capacity=x['vehicles']*x['spaces_per_vehicle']
    peak=dict(first_arrival_minute=first,next_arrival_minute=next_arrival,deadline_minute=x['deadline_minute'],
        first_wave_capacity=first_wave_capacity,people=x['people'],
        all_arrive_in_time=(x['people']<=first_wave_capacity and first<=x['deadline_minute']) or (x['people']<=2*first_wave_capacity and next_arrival<=x['deadline_minute']),
        actual_safe_engineering=None)
    return dict(local_cases=out,country_cases=country,wheelchair_peak=peak,actual_national_cost_or_source=None)

def evidence(c):
    if c['seats']<=0 or not 0<c['vote_numerator']<=c['vote_denominator']:raise ValueError('Unsupported full Assembly size/threshold')
    threshold=math.ceil(c['seats']*c['vote_numerator']/c['vote_denominator'])
    return dict(full_seats=c['seats'],votes_required=threshold,
        illustrative_votes=[dict(yes=n,threshold_met=n>=threshold,actual_appointment=False) for n in [threshold-1,threshold]],
        vacancy_cases=[dict(elapsed_days=d,limited_deputy_continuity=d<c['continuity_limit_days'],
            routine_source_preservation_existing_series_and_in_method_correction_continue=True,
            new_policy_or_senior_discretion_from_vacancy=False,appointment_from_elapsed_time=False) for d in c['vacancy_days']],
        legal_series_definition_changed_by_method=False,statistical_revision_automatically_reprices_claim=False,
        actual_authority_publication_or_funding=None)

def calculate(c=None):
    c=c or json.loads((HERE/'inputs.json').read_text())
    return dict(edition=94,scope='Conditional arithmetic and illustrative institution thresholds only; no complete country operating account',
        context=context.calculate(c['context']),mobility=mobility(c['mobility']),evidence=evidence(c['evidence']),actual=c['actual'])

if __name__=='__main__':(HERE/'results.json').write_text(json.dumps(calculate(),indent=2)+'\n')
