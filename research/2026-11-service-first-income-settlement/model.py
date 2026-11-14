"""Two separate comparison layers; never a calibrated country microsimulation."""
from pathlib import Path
from decimal import Decimal as Q
import json
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text())
def q(x):
    if x is None or isinstance(x,bool):raise ValueError('explicit numeric value required')
    v=Q(str(x))
    if not v.is_finite():raise ValueError('finite value required')
    return v

def retained(row):
    fields={'id','source_table','page_zero_based','UI','children','previous_AW_fraction','return_full_time_equivalent_wage_AW_fraction','time_fraction','AETR_percent'}
    if set(row)!=fields or set(row['AETR_percent'])!={'published_current','published_BI','published_UC'}:raise ValueError('unmapped source-case semantics')
    if type(row['UI']) is not bool or not (0<q(row['time_fraction'])<=1):raise ValueError('unmapped household scope')
    return {'id':row['id'],'net_income_change_per_100_new_gross':{k:str(100-q(v)) for k,v in row['AETR_percent'].items()},
            'actual_absolute_income_or_retired_service_effect':None}

def country_case(entry):
    if set(entry)!={'id','path'}:raise ValueError('unknown country case meaning')
    allowed={
      'A_plural':'2026-11-current-country-operating-and-source-reference/cases/firm_plural_I05.json',
      'A_direct':'2026-11-current-country-operating-and-source-reference/cases/firm_direct_I05.json',
      'U_C2_plural':'2026-11-productive-choice-and-work-incidence/cases/firm_plural_C2.json',
      'U_C2_direct':'2026-11-productive-choice-and-work-incidence/cases/firm_direct_C2.json'}
    if allowed.get(entry['id'])!=entry['path']:raise ValueError('unmatched country/source/provider scope')
    x=read(R/entry['path']);p=x['personal']['totals'];b=x['public_book'];c=x['cash_required_not_paid']
    payment=q(p['I05'])+q(p['nonolder_U'])+q(p['Y_basic'])
    return {'id':entry['id'],'source':entry['path'],'units':'authored CU; not observed national quantities',
      'named_service_allocation':b['named_annual_allocation_CU'],
      'I05_plus_nonolder_U_plus_Y_basic':str(payment),'PA_assessed_not_cash':p['PA_assessed'],
      'service_personal_net_assessment_incidence_not_full_G_cost':str(q(b['named_annual_allocation_CU'])+payment-q(p['PA_assessed'])),
      'earned_survivor_insurance_gross_separate_S':p['insurance_gross'],
      'Y_basic':p['Y_basic'],'Y_new_annual_units_not_due_cash':p['Y_new_annual_units'],
      'care_credit_required_G_to_S':x['personal']['care_credit_G_to_S'],
      'recognized_housing':p['recognized_housing'],
      'cash_after_named_housing':p['cash_after_named_housing'],
      'distinct_service_people_not_fungible':b['distinct_service_people_not_fungible'],
      'named_stress_first_unfunded_G_date':c['first_unfunded_date']['G'],
      'actual_complete_country_cost_source_or_better_lives':None}

def compute(config=None,published=None):
    cfg=read(D/'inputs.json') if config is None else config
    if set(cfg)!={'edition','published_cases','normalization','country_layer','cases'} or cfg['edition']!=136 or cfg['published_cases']!='published-cases.json':raise ValueError('unknown comparison context')
    if cfg['normalization']!='100 units of new gross earnings; not currency, level income, marginal slope or paid outcome' or cfg['country_layer']!='unchanged authored 130/131 firm_seven_extended context, separate CU units':raise ValueError('incompatible units/context')
    pub=read(D/cfg['published_cases']) if published is None else published
    if set(pub)!={'source','doi','original_family','reference_rules','kind','unit','cases','unresolved_source_fields'} or pub['reference_rules']!='2015-07-01' or pub['kind']!='published model households, not observed individual records' or pub['unit']!='AETR percentage, rounded at source':raise ValueError('unmatched evidence semantics')
    if len(pub['cases'])!=4 or len({c['id'] for c in pub['cases']})!=4:raise ValueError('changed household denominator')
    cc=[country_case(e) for e in cfg['cases']];by={c['id']:c for c in cc}
    if len(cc)!=4 or set(by)!={'A_plural','A_direct','U_C2_plural','U_C2_direct'}:raise ValueError('changed country rival set')
    differences=[]
    for provider in ['plural','direct']:
      a=by['A_'+provider];u=by['U_C2_'+provider]
      differences.append({'provider':provider,'U_minus_A_partial_G_incidence_CU':str(q(u['service_personal_net_assessment_incidence_not_full_G_cost'])-q(a['service_personal_net_assessment_incidence_not_full_G_cost'])),
        'U_minus_A_personal_cash_after_named_housing_CU':str(q(u['cash_after_named_housing'])-q(a['cash_after_named_housing'])),
        'actual_extra_source_tax_or_behavior':None})
    return {'edition':136,'published_model_case_retention':[retained(c) for c in pub['cases']],
      'country_cases':cc,'country_partial_differences':differences,
      'unresolved_published_source_fields':pub['unresolved_source_fields'],
      'actual_rights_preserving_foreign_U_or_A_country_cost':None,
      'actual_matched_lifetime_service_quality_or_transition_outcome':None,
      'research_choice':'service-first individual guarantee; U is a live rival, no presumed destination',
      'actual_lawful_adoption_or_independent_affected_review':None}
if __name__=='__main__':(D/'results.json').write_text(json.dumps(compute(),indent=2)+'\n')
