"""Bounded planned enabling envelope; no national feasibility certificate."""
from fractions import Fraction as F
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def clean(x):
    if isinstance(x,F): return float(x)
    if isinstance(x,dict): return {k:clean(v) for k,v in x.items()}
    if isinstance(x,list): return [clean(v) for v in x]
    return x

def calculate():
    d=json.loads((HERE/'inputs.json').read_text()); results=[]
    for case in d['cases']:
        cash=F(str(case['opening_programme_cash'])); fx=F(d['opening_fx'])
        unpaid=F(0); unpaid_fx=F(0); rows=[]
        end=case['project_years']; total_cap=F(d['capital_total'])*F(str(case['capital_multiplier']))
        for y in range(1,d['years']+1):
            capital=total_cap/end if y<=end else F(0)
            training=F(d['annual_training']) if y<=end else F(0)
            salary=F(str(d['annual_staff_pay']))
            maintenance=F(d['annual_maintenance']) if y>end else F(0)
            due=capital+training+salary+maintenance
            paid=min(due,max(F(0),cash-F(d['cash_buffer'])))
            cash-=paid; unpaid+=due-paid
            imports=F(d['annual_project_imports']) if y<=end else F(d['annual_operating_imports'])
            exports=F(case['export_receipts'])
            forex_due=imports+F(str(d['annual_existing_foreign_service']))
            forex_short=max(F(0),forex_due-exports)
            draw=min(forex_short,max(F(0),fx-F(d['fx_floor'])))
            fx+=max(F(0),exports-forex_due)-draw
            unpaid_fx+=forex_short-draw
            qualified={k:(n if y>d['qualification_years'][k] else 0) for k,n in d['staff_moves'].items()}
            # Opening reserves cannot pay the same liability twice. Arrears persist.
            accepted=(y>=end and unpaid==0 and unpaid_fx==0)
            in_service=(y>end and accepted)
            rows.append({'year':y,'planned_capital':capital,'planned_training':training,
                'planned_salary':salary,'planned_maintenance':maintenance,'planned_due':due,
                'cash_paid_unallocated':paid,'cash_close':cash,'cumulative_cash_unpaid':unpaid,
                'imports_component_not_second_cash_bill':imports,'conditional_export_receipts':exports,
                'foreign_service':F(str(d['annual_existing_foreign_service'])),
                'fx_draw':draw,'fx_close':fx,'cumulative_fx_unpaid':unpaid_fx,
                'qualified_staff_assumption':qualified,'private_staff_after_move':d['private_staff_opening']-sum(d['staff_moves'].values()),
                'public_staff_after_move':d['public_staff_opening']+sum(d['staff_moves'].values()),
                'conditional_asset_acceptance':accepted,'conditional_asset_in_service':in_service,
                'deadline_capacity_missed':y==d['commission_year'] and not (accepted and end==d['commission_year'])})
        r=d['resources']; in_service=rows[-1]['conditional_asset_in_service']
        physical={'energy_available_at_10_percent_loss':F('0.9')*(r['energy_firm_opening']+(r['energy_addition_target'] if in_service else 0))-r['energy_standby'],
            'future_energy_demand':r['future_energy_demand'],
            'water_available_at_10_percent_raw_loss':F('0.9')*F(r['raw_water'])-F(r['ecological_water'])-F(str(r['water_standby']))+(F(r['independent_safe_water_target']) if in_service else F(0)),
            'future_water_demand':F(r['future_raw_water_demand'])-(F(str(r['verified_efficiency_target'])) if in_service else F(0))}
        staffing={k:F('0.9')*(n+rows[-1]['qualified_staff_assumption'][k]) for k,n in d['opening_staff'].items()}
        results.append({'case':case['name'],'annual':rows,'total_planned_due':sum(x['planned_due'] for x in rows),
            'total_capital':total_cap,'ending_cash':cash,'cumulative_cash_unpaid':unpaid,
            'ending_fx':fx,'cumulative_fx_unpaid':unpaid_fx,
            'first_cash_shortfall_year':next((x['year'] for x in rows if x['cumulative_cash_unpaid']>0),None),
            'first_fx_shortfall_year':next((x['year'] for x in rows if x['cumulative_fx_unpaid']>0),None),
            'planned_commission_year':end,'matched_cost_through_two_operating_years':total_cap+F(d['annual_training'])*end+F(str(d['annual_staff_pay']))*(end+2)+F(d['annual_maintenance'])*2,
            'unfunded_matched_completion':max(F(0),total_cap+F(d['annual_training'])*end+F(str(d['annual_staff_pay']))*(end+2)+F(d['annual_maintenance'])*2+F(d['cash_buffer'])-F(str(case['opening_programme_cash']))),
            'annual_postconstruction_salary_and_maintenance':F(str(d['annual_staff_pay']))+F(d['annual_maintenance']),'deadline_met_in_reference':end==d['commission_year'] and rows[end-1]['conditional_asset_acceptance'],
            'physical_if_targets_verified':physical,'staff_after_10_percent_loss_if_qualified':staffing,
            'actual_funding_source':None,'actual_qualified_staff':None,'national_budget_feasibility':None,
            'delivered_remedy':None,'observed_life_outcomes':None,'actual_operating_readiness':False})
    return clean({'qualification':d['scope'],'cases':results})

if __name__=='__main__': print(json.dumps(calculate(),indent=2))
