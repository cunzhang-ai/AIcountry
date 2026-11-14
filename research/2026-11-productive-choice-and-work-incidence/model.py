"""Authored incidence and matched garment offers; no orders, jobs or source forecast."""
from pathlib import Path
from decimal import Decimal as Q, ROUND_CEILING
import importlib.util, json, sys

D = Path(__file__).resolve().parent
R = D.parent
BASE = R / '2026-11-current-country-operating-and-source-reference'
q = lambda x: Q(str(x))
read = lambda p: json.loads(p.read_text())
ceil = lambda x: int(x.to_integral_value(rounding=ROUND_CEILING))

def clean(x):
    if isinstance(x, Q): return str(x)
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, list): return [clean(v) for v in x]
    return x

def tax(base, package, M=Q(30000)):
    allowance = q('.4') * M
    if package == 'C1' and base > M:
        allowance = max(Q(0), q('.4') * (2 * M - base))
    if package not in ('A', 'C1', 'C2'): raise ValueError('Uninterpreted tax package')
    left = max(Q(0), base - allowance)
    result = Q(0)
    for width, rate in [(q('.5')*M,q('.2')), (q('.5')*M,q('.35')), (M,q('.45')), (None,q('.55'))]:
        amount = left if width is None else min(left, width)
        result += amount * rate
        left -= amount
    return result

def person(wage, package, housing=Q(0), extra=Q(0), received=Q(1), taper=q('.5')):
    B = Q(13248)
    earned = wage * received
    y = earned * q('.1')
    pa = tax(earned-y, package)
    E = earned-y-pa
    U = B if package != 'A' else Q(0)
    award = max(Q(0), B+housing+extra-taper*max(Q(0),E-q('.2')*B)-U)
    return {'gross_due':wage,'gross_received':earned,'unpaid_wages':wage-earned,
            'Y':y,'PA':pa,'I05':award,'U':U,'cash_after_named_housing_and_extra':E+award+U-housing-extra}

def incidence():
    rows = []
    for package in ['A','C1','C2']:
        for housing,extra,name in [(Q(6000),Q(0),'ordinary_housing'),(Q(6000),Q(30000),'high_necessary_cost_stress')]:
            for wage in [Q(0),Q(10000),Q(30000),Q(40000),Q(50000),Q(60000),Q(80000),Q(120000)]:
                a=person(wage,package,housing,extra)
                b=person(wage+1,package,housing,extra)
                rows.append({'package':package,'profile':name,'housing':housing,'extra':extra,
                             **a,'next_CU_retained':b['cash_after_named_housing_and_extra']-a['cash_after_named_housing_and_extra'],
                             'scope':'Individual annual cash arithmetic, fixed necessary costs; no behavioral prediction or service-fee/indirect-tax estimate.'})
    return rows

def garment_offers(cfg):
    pb=read(R/'2026-11-ordinary-life-and-household-production/inputs.json')
    row=next(x for x in pb['basket'] if x['id']=='garments')
    adults=sum(x['households']*(x['working_age_adults_each']+x['older_adults_each']) for x in pb['household_types'])
    ages={a:sum(h['households']*h['child_ages_each'].count(a) for h in pb['household_types']) for a in pb['child_age_order']}
    nominal=q(row['annual_quantity'])*(adults+sum(q(w)*ages[a] for a,w in zip(pb['child_age_order'],row['child_quantity_weights'])))
    baseline=read(BASE/'cases/firm_plural_I05.json')['supply']
    power=q(baseline['power_exVAT_CU_kWh']);water=q(baseline['water_exVAT_CU_m3'])
    out=[]
    for choice,recipe in cfg['garment_recipes'].items():
        # Full protected annual payroll remains due when demand falls. No residual staffing.
        workers=ceil(nominal*q(recipe['hours_per_item'])/q(cfg['task_hours_per_paid_year']))
        instructors=ceil(q(workers)*64/(800*16))
        pay=q(workers)*30000+q(instructors)*60000
        for fx in cfg['CU_per_FU']:
            fx=q(fx)
            assets=q(recipe['new_asset_CU'])+q(recipe['capital_import_FU'])*(fx-1)
            annual_renewal=assets/5
            fixed=pay+annual_renewal+q(recipe['annual_site_and_other_CU'])
            var=q(recipe['foreign_material_or_finished_FU_per_item'])*fx+q(recipe['kWh_per_item'])*power+q(recipe['m3_per_item'])*water
            # Gross input VAT is fronted, not a permanent duplicate cost; all refunds conditional.
            initial_stock=nominal/12*q(recipe['foreign_material_or_finished_FU_per_item'])*fx
            startup=assets*q('1.1')+initial_stock*q('1.1')+pay/12
            target= q('.04')*startup
            exprice=(fixed+nominal*var+target)/nominal
            for demand in cfg['demand_fraction']:
                fraction=q(demand);sold=nominal*min(Q(1),fraction)
                revenue=sold*exprice;variable=sold*var
                profit=revenue-variable-fixed
                company=max(Q(0),profit)*q('.25')
                payroll_incidence={p:{k:Q(0) for k in ['PA','Y','I05','cash_after_named_housing_and_extra']} for p in ['A','C1','C2']}
                for p in payroll_incidence:
                    for n,w in [(workers,Q(30000)),(instructors,Q(60000))]:
                        v=person(w,p,Q(6000))
                        for k in payroll_incidence[p]: payroll_incidence[p][k]+=n*v[k]
                out.append({'choice':choice,'CU_per_FU':fx,'demand_fraction':fraction,
                            'reference_items_not_orders':nominal,'capacity_items':nominal,'sold_if_demand_is_paid':sold,
                            'unserved_if_demand_exceeds_capacity':max(Q(0),nominal*fraction-sold),
                            'worker_posts_not_actual_hires':workers,'instructor_posts_not_actual_hires':instructors,
                            'annual_gross_pay_due':pay,'initial_capital_stock_CU':assets,
                            'capital_import_FU_included_in_asset_quote':q(recipe['capital_import_FU']),
                            'gross_startup_finance_CU_before_refunds':startup,'initial_goods_stock_FU':initial_stock/fx,
                            'renewal_not_new_annual_capital_purchase_CU':annual_renewal,
                            'consumer_unit_offer_incVAT':exprice*q('1.1'),'performance_revenue_exVAT':revenue,
                            'variable_inputs_exVAT':variable,'fixed_cost_exVAT':fixed,
                            'profit_before_company_tax':profit,'company_assessment_due_next_April':company,
                            'operating_cash_before_stock_capital_VAT_and_distributions':revenue-variable-pay-q(recipe['annual_site_and_other_CU']),
                            'after_company_profit_or_loss_retained_not_personal_income':profit-company,
                            'annual_material_or_finished_import_FU':sold*q(recipe['foreign_material_or_finished_FU_per_item']),
                            'additional_process_GWh_not_physically_qualified':sold*q(recipe['kWh_per_item'])/1000000,
                            'additional_process_water_m3_not_physically_qualified':sold*q(recipe['m3_per_item']),
                            'personal_incidence_if_these_distinct_workers_are_paid':payroll_incidence,
                            'actual_orders_staff_title_finance_owned_FX_or_received_refunds':None,
                            'whole_country_source_increment_or_net_physical_change':None})
    return out

def current_country_C2():
    # Explicit, reversible adapter. Historical modules/files stay unchanged. C1's
    # U/age/payment semantics are reused; only the personal tax function changes.
    sys.path.insert(0,str(BASE))
    spec=importlib.util.spec_from_file_location('_design130_for_131',BASE/'model.py')
    base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    people=sys.modules['people'];oldtax=people.tax
    def revised(base_value,config,package):
        if config['band_widths_M']!=['.5','.5','1',None] or [q(x) for x in config['tax_rates']]!=[q('.2'),q('.35'),q('.45'),q('.55')]:
            raise ValueError('Changed tax schedule needs a new adapter')
        return tax(base_value,'C2' if package=='C1' else package,q(config['M']))
    try:
        people.tax=revised
        fresh=base.compute(read(BASE/'inputs.json'))
    finally:
        people.tax=oldtax
    old=base.read_results();out={};summaries=[]
    for label,case in fresh['cases'].items():
        prior=old['cases'][label]
        if label.endswith('/A'):
            if case != prior: raise AssertionError('Unchanged I05 case changed through tax adapter')
            continue
        newlabel=label[:-2]+'C2';case['assumptions']['id']=newlabel;case['assumptions']['package']='C2'
        a=prior['personal']['totals'];b=case['personal']['totals']
        summary={'case':newlabel,'PA_reduction_CU':q(a['PA_assessed'])-q(b['PA_assessed']),
                 'I05_reduction_CU':q(a['I05'])-q(b['I05']),
                 'additional_net_G_annual_personal_incidence_CU':q(a['PA_assessed'])-q(b['PA_assessed'])+q(b['I05'])-q(a['I05']),
                 'first_unfunded_G_date':case['cash_required_not_paid']['first_unfunded_date']['G'],
                 'scope':'Fixed wages/prices/receipt/needs, current 130 scope only; not general equilibrium, full tax yield or national deficit.'}
        for before,after in zip(prior['personal']['people'],case['personal']['people']):
            if before['id']!=after['id'] or before['count']!=after['count']:raise AssertionError('Changed people/identity')
            gain=q(before['tax_each'])-q(after['tax_each'])+q(after['I05_each_averaged_over_authored_home_profiles'])-q(before['I05_each_averaged_over_authored_home_profiles'])
            if gain<q('-.000000001'):raise AssertionError('Person loses in fixed-price C2 comparison')
        name=('firm' if 'firm_seven' in label else 'storage')+'_'+('plural' if 'plural_public' in label else 'direct')+'_C2.json'
        out[name]=case;summaries.append(summary)
    return out,summaries

def compute(include_country=True,cfg=None):
    cfg=read(D/'inputs.json') if cfg is None else cfg
    if set(cfg)!=set(read(D/'input-keys.json')): raise ValueError('Uninterpreted future input semantics')
    expected={'hours_per_item','foreign_material_or_finished_FU_per_item','kWh_per_item','m3_per_item','new_asset_CU','capital_import_FU','annual_site_and_other_CU'}
    if set(cfg['garment_recipes'])!={'local_making_and_retail','finished_import_and_retail'} or any(set(v)!=expected for v in cfg['garment_recipes'].values()):
        raise ValueError('Uninterpreted producer concept; preserve it for scoped review')
    if cfg['edition']!=131 or any(v is not None for k,v in cfg.items() if k.startswith('actual_')):
        raise ValueError('Actual observations need qualification, not relabeling of an authored case')
    if q(cfg['task_hours_per_paid_year'])<=0 or any(q(x)<=0 for x in cfg['CU_per_FU']) or any(q(x)<0 for x in cfg['demand_fraction']):
        raise ValueError('Invalid quantities')
    for recipe in cfg['garment_recipes'].values():
        if any(q(v)<0 for v in recipe.values()) or q(recipe['capital_import_FU'])>q(recipe['new_asset_CU']):raise ValueError('Unreconciled producer quantity/title scope')
    cases,summaries=current_country_C2() if include_country else ({},[])
    return clean({'edition':131,'format_revision':'131-tax-overlay-and-partial-offers-v1','incidence':incidence(),'garment_offers':garment_offers(cfg),
                  'country_C2_summaries':summaries,'actual_complete_country_or_superiority':None}),clean(cases)

if __name__=='__main__':
    result,cases=compute()
    (D/'cases').mkdir(exist_ok=True)
    result['country_C2_cases']={name:'cases/'+name for name in cases}
    for name,case in cases.items(): (D/'cases'/name).write_text(json.dumps(case,indent=2)+'\n')
    (D/'results.json').write_text(json.dumps(result,indent=2)+'\n')
