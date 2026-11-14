"""A five-table operating book with honest stops before unsupported country totals."""
from pathlib import Path
import json,math
import personal,producers
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent


def calculate(c=None):
    c=c or json.loads((HERE/'inputs.json').read_text());H=json.loads((ROOT/c['sources']['tw_results']).read_text())['cases'][0]['calendar']['deployable_task_hours']
    ps=json.loads((ROOT/c['sources']['ps_results']).read_text());house=json.loads((ROOT/c['sources']['housing_results']).read_text())
    goods=producers.ordinary_goods(c['goods'],H);labor=personal.labor_cases(c['labor'])
    persons=[]
    for p in c['persons']:
        outcomes={k:personal.payment(p,c['tax'],k) for k in ['protected_foundation','extra_personal_allowance','retained_I05','equivalent_taxable_gross']}
        ordered=personal.payment(p,c['tax'],'protected_foundation','work_first')
        # Fixed-fact marginal resource change; not actual work incentive/price response.
        q=dict(p);q['wage']=p.get('wage',0)+1
        following=personal.payment(q,c['tax'],'protected_foundation')
        outcomes['fixed_fact_next_gross_wage_retained_CU']=following['usable_resources_including_actual_asset_draw']-outcomes['protected_foundation']['usable_resources_including_actual_asset_draw']
        outcomes['work_first_attribution_rival']=ordered
        persons.append(dict(id=p['id'],outcomes=outcomes))
    Y=[]
    for full in [False,True]:
        a=personal.pension_new_year(12000,1 if full else 0,12000 if full else 0,c['tax']['annual_independent_W'])
        b=personal.pension_new_year(18000,1 if full else 0,18000 if full else 0,c['tax']['annual_independent_W'])
        Y.append(dict(full_credit_eligibility_assumed=full,before=a,after=b,people=15000,
                      extra_restricted_contribution_CU=(b['contribution']-a['contribution'])*15000,
                      G_credit_transfer_change_CU=(b['G_credit_transfer']-a['G_credit_transfer'])*15000,
                      extra_service_year_candidate_units_CU=(b['new_annual_lifetime_unit']-a['new_annual_lifetime_unit'])*15000,
                      best48_selection_or_lifetime_liability=None,actual_eligibility_or_funding=None))
    cohort_tax=[]
    for l in labor:
        total=tax=contrib=0
        for row in l['rows']:
            z=personal.payment(dict(id=row['id'],wage=row['annual_pay_CU']),c['tax'])
            total+=row['people']*row['annual_pay_CU'];tax+=row['people']*z['personal_tax'];contrib+=row['people']*z['employee_Y_contribution']
        cohort_tax.append(dict(case=l['id'],scenario_wages_CU=total,hypothetical_personal_tax_CU=tax,hypothetical_restricted_contribution_CU=contrib,actual_employer_source_or_collected_tax=None,national_general_balance=None))
    paths=[]
    for path in ['resource_fit_mixed/desal','import_heavy/bulk']:
        s=next(x for x in ps['cases'] if x['id']==path)
        inherited=[]
        for name,roles in [('food',s['food']['roles']),('new_water',s['water']['new_roles']),('housing_repair40',house['programs']['selected32']['repair40']['roles'])]:
            for id,x in roles.items():
                inherited.append(dict(producer=name,id=id,required_annual_posts=x.get('annual_post_bound',x.get('annual_post_lower_bound')),payroll_CU=x.get('ordinary_payroll_CU'),actual_job_or_person_assignment=None,possible_overlap_with_old_service_book=None))
        # Do not sum ambiguous shares into actual national workforce or revenues.
        five=dict(final_goods=[*goods['final_goods'],dict(id='food_received',quantity=s['food']['received_t'],unit='tonne',public_meals_subset=True),dict(id='bus_mobility',quantity=goods['bus_passenger_km'],unit='passenger-km',old_scope_replaced=True)],
                  producers=[*goods['producer_recipes'],dict(id='PS_food_water_power',source_case=path,complete_price=None,required_foreign_minimum_CU=s['named_recurring_FX_quote_CU'])],
                  jobs=[*goods['role_requirements'],*inherited],
                  assets=goods['operator_assets'],
                  cash_claims=[dict(id='annual_final_goods_border',required_CU=goods['annual_final_goods_border_quote_CU'],owner='Private/authorized public importer, actual owner unknown',settled_source=None),dict(id='retail_working_stock',required_CU=goods['inventory_working_asset_CU'],type='Initial working inventory, not recurring consumption',settled_source=None),dict(id='operator_assets',quote_if_all_absent_CU=goods['operator_gross_asset_quote_CU'],actual_required_CU=None,type='Replacement quote; identify included asset OR paid transaction before commitment',settled_source=None),dict(id='consumer_durables_if_absent',quote_if_all_absent_CU=goods['household_device_appliance_stock_quote_CU'],actual_required_CU=None,type='Household stock quote, not automatic new purchase/operator capital',settled_source=None),dict(id='old_due_claims',required_CU=None,continuing_obligations=True,source_law=None)])
        paths.append(dict(path=path,five_tables=five,new_private_service_electricity_GWh=goods['electricity_GWh'],
                          provisional_PS10_reallocation_not_complete_source_match=True,public_building60_overlap_resolved=False,
                          water_annual_source_volume_bound_pass=s['water']['normal_source_volume_bound_pass'],
                          new_good_quantities_have_complete_supplier_or_price=False,all_person_job_contracts_matched=False,
                          full_physical_or_price_or_income_tax_closure=None,full_initial_or_recurring_or_foreign_finance=None,
                          national_GDP=None,national_launch_qualified=False))
    return dict(edition=93,status='Five-table partial operating book and explicit tax/pay choices, not a nationally closed budget/price/source account',
                ordinary_goods=goods,labor_cases=labor,personal_incidence=persons,low_wage_pension_changes=Y,
                hypothetical_cohort_wage_tax=cohort_tax,paths=paths,
                simple_high_band_fixed_cost_retention=(1-.1)*(1-.55)*(1-.5),
                unresolved=['Complete supplier/plant/land/finance prices and actual household basket choices','Accepted employer/person/qualification/time matches for all wages','Matched old/new37function purchases, assets, participant time and bus scopes','Private discretionary demand/saving/production and additional needs','Y cohorts/oldindex/netsource obligations, due-day liquidity and full sources','Actual funded foreign orders/energy routes and independent safe operation'],
                actual=c['actual'])


if __name__=='__main__':(HERE/'results.json').write_text(json.dumps(calculate(),indent=2)+'\n')
