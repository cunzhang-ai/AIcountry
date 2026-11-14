"""Joined named component book; unknown current cost/source never becomes zero."""
from pathlib import Path
from decimal import Decimal as Q,ROUND_CEILING
from copy import deepcopy
import json,sys
D=Path(__file__).resolve().parent;R=D.parent
sys.path.insert(0,str(D))
from public_book import build,cost,staff
from democratic_capacity import apply
read=lambda p:json.loads(p.read_text())
q=lambda n:Q(str(n))
ceil=lambda n:int(n.to_integral_value(rounding=ROUND_CEILING))

def instructors(n,H,load=5):
    k=0
    for _ in range(100):
        new=ceil((q(n)+k)*q(load)/q(H))
        if new==k:return k
        k=new
    raise ValueError('No bounded instructor fixedpoint')

def run(cfg):
    expected={'edition','scope','year','public_base','clinical_care','private_households','service_cases','calendar','pay','clinical_choice','public_housing_title_fraction','declared_no_new_actual_title_transfer','retired_generic_network_component','replacement_physical_portfolio_price','democratic_reference','added_staff','added_fee_blocks','added_operating','contingency_draw_cases','new_shared_stations','unknown_full_current_scope','actual_complete_country_cost_or_source','private_paid_time_case'}
    if set(cfg)!=expected:raise ValueError('Unsupported future semantics require fresh scoped model review')
    if set(cfg['service_cases'])!={'plural_public_backbone','direct_public_rival'}:raise ValueError('Uninterpreted provider regime')
    if any(set(v)!={'public_operator_fraction','supplier_margin'} or not 0<=q(v['public_operator_fraction'])<=1 or q(v['supplier_margin'])<0 for v in cfg['service_cases'].values()):raise ValueError('Invalid provider scope')
    if cfg['edition']!=125 or cfg['actual_complete_country_cost_or_source'] is not None:raise ValueError('Unsupported actual country claim')
    cal=cfg['calendar'];load=q(cal['learning_activity_hours'])/q(cal['learning_group'])*(1+q(cal['instructor_preparation_fraction']))
    original=read(R/'settlement/commitments/inventory.json')['functions'];base,actions=build(cfg)
    political=apply(base,cfg)
    if any(v['owner'] not in {f['id'] for f in original} for v in base.values()):raise ValueError('Uninterpreted new function needs denominator/source review')
    legacy=read(R/cfg['public_base'])['cases']['A']['labor_components']
    baseline_roles=sum(q(x['paid_role_equivalents']) for x in legacy if x['family']=='QE_named_current_demand')
    cases={}
    for name,rule in cfg['service_cases'].items():
        core=deepcopy(base)
        # Genuine direct-provider rival retains smaller40contract logistics, not300private service interfaces.
        if name=='direct_public_rival':
            core['labor:current_contract_procurement']=staff('labor:current_contract_procurement','D07','professional',q(40)*(q(8)/3+6+8+4+4),None,cfg,False,note='40service procurement contracts; public staff/management/other goods/source costs remain')
            core['op:current_tender_publication']['annual_base_CU']='4000'
        n=sum(q(v['posts']) for v in core.values() if v['kind']=='staff')
        k=instructors(n,cfg['calendar']['annual_task_hours'],load)
        core['labor:current_learning_instructors']=staff('labor:current_learning_instructors','L07','professional',(n+k)*load,k,cfg,True,k,'Recomputed64learnerhours/16group+25%prep; owninstructorlearning included, not duplicate learnerdemand')
        extra=max(Q(0),n+k-baseline_roles)
        stations=ceil(extra)+political['verifier_people_demand']
        sc=cfg['new_shared_stations']
        core['asset:shared_new_secure_workstations']={'id':'asset:shared_new_secure_workstations','owner':'K03','kind':'asset','annual_upkeep_CU':str(q(stations)*q(sc['upkeep_CU_year'])),'renewal_CU':str(q(stations)*q(sc['unit_CU'])/q(sc['life_years'])),'all_new_quote_CU':str(q(stations)*q(sc['unit_CU'])),'eligible_operator':False,'public_title_fraction':1,'note':'Onecurrentincrementalnew-roleanddeclaredpeak workstationpool replacesold107pool; actual baseline overlap/compatibility unknown'}
        records=cost(core,cfg,rule)
        frows=[]
        for f in original:
            r=[v for v in records if v['owner']==f['id']]
            frows.append({'id':f['id'],'function':f['function'],'components':[v['id'] for v in r],'paid_role_equivalents':str(sum((q(v['posts']) for v in r if v['kind']=='staff'),Q(0))),
                'named_allocation_CU':str(sum((q(v['named_allocation_CU']) for v in r),Q(0))),
                'actual_full_current_cost':None,'actual_qualified_simultaneous_capacity':None,'actual_due_source_and_received_remedy':None})
        allocation=sum((q(v['named_allocation_CU']) for v in records),Q(0));external=sum((q(v['external_cash_requirement_CU']) for v in records),Q(0));reserve=sum((q(v['public_renewal_reservation_CU']) for v in records),Q(0))
        supplier_prepay=sum((q(v['supplier_invoice_CU']) for v in records),Q(0))
        direct_nonpay=sum((q(v['direct_public_nonpay_CU']) for v in records if v['kind']!='transfer_envelope'),Q(0))
        cases[name]={'function_rows':frows,'component_rows':records,'named_annual_allocation_CU':str(allocation),'external_cash_requirement_CU':str(external),'public_owned_renewal_reservation_CU':str(reserve),'employee_pay_both_public_and_supplier_CU':str(sum((q(v['annual_base_CU']) for v in records if v['kind']=='staff'),Q(0))),
            'paid_role_equivalents':str(n+k),'learning_instructors':k,'new_workstation_quote_units':stations,
            'public_all_new_asset_quote_CU':str(sum((q(v.get('public_all_new_quote_CU',0)) for v in records),Q(0))),
            'public_housing_title_quote_CU':next(v['public_all_new_quote_CU'] for v in records if v['id']=='asset:supported_dwellings'),
            'mature_year_monthly_external_average_CU':str(external/12),
            'opening_month_supplier_prepay_and_nontransfer_nonpay_sensitivity_CU':str((supplier_prepay+direct_nonpay)/12),
            'separate_fullyear_political_credit_source_envelope_CU':political['credit_total_envelope_CU'],
            'opening_separate_public_renewal_reservation_CU':str(reserve),
            'source_or_cash_balance':None,'actual_legal_appropriation_or_receipt_or_safe_roster':None}
    household=read(R/cfg['private_households']);privatecases={}
    for label in ['retained_source','prospective_wholeposts']:
        people=household['home_help'][label]['people']
        retail_people=sum(x['retail_posts'] for x in household['goods_base']);n=people+retail_people;k=instructors(n,cfg['calendar']['annual_task_hours'],load);pay=q(k)*q(cfg['pay']['professional'])
        helper=pay*q(people)/q(n);retail=pay-helper
        old=household['home_help'][label];revised=(q(old['named_cost_exVAT_CU'])+helper)*q('1.06')*q('1.1')/q(old['task_hours'])
        retail_prices=[{'id':g['id'],'learning_share_CU':str(retail*q(g['retail_posts'])/q(retail_people)),'revised_consumer_unit_CU':str((q(g['household_cash_CU'])+retail*q(g['retail_posts'])/q(retail_people)*q('1.06')*q('1.1'))/q(g['new_units']))} for g in household['goods_base']]
        privatecases[label]={'repriced_retail_with_learning':retail_prices,'existing_named_workers':n,'additional_learning_instructors':k,'private_employer_learning_pay_CU':str(pay),'helper_share_CU':str(helper),'retail_share_CU':str(retail),'new_helper_customer_unit_CU':str(revised),'old_PB_quote_without_matched_instructor_CU':old['consumer_unit_CU'],'actual_paid_private_source':None}
    housing=read(R/cfg['clinical_care'])['housing_integer_peak_corrected_quote'];hp=sum(v['posts'] for v in housing['roles'].values());hi=instructors(hp,cfg['calendar']['annual_task_hours'],load)
    private_time=cfg['private_paid_time_case'];boardhours=(private_time['medium_enterprises']*private_time['medium_worker_board_seats']+private_time['large_enterprises']*private_time['large_worker_board_seats'])*private_time['meetings_year']*private_time['hours_each']
    return {'edition':125,'scope':cfg['scope'],'replacement_actions':actions,'democratic_fullfield_reference':political,'service_cases':cases,
        'household_reference_source':cfg['private_households'],'private_learning_and_reprice':privatecases,
        'housing_learning_overlay':{'prior_scoped_program_CU':housing['named_program_CU'],'role_posts':hp,'additional_instructors':hi,'additional_pay_CU':str(hi*q(cfg['pay']['professional'])),'named_program_with_this_learning_CU':str(q(housing['named_program_CU'])+hi*q(cfg['pay']['professional'])),'public_private_funding_and_care_adaptation_overlap':None},
        'private_worker_board_case':{'paid_existing_employee_hours_displaced':boardhours,'additional_cover_post_bound':ceil(q(boardhours)/q(cfg['calendar']['annual_task_hours'])),'additional_cover_pay_quote_CU':str(ceil(q(boardhours)/q(cfg['calendar']['annual_task_hours']))*q(private_time['private_role_pay'])),'actual_scope_overlap_and_employer_source':None},
        'contingency_draw_cases':cfg['contingency_draw_cases'],'same_loss_scope_probe':{'economic_wage_loss_CU':5000,'qualified_AS_claim_CU':5000,'qualified_WL_claim_CU':2500,'actually_received_same_loss_WL_CU':1000,'remaining_same_loss_AS_due_CU':4000,'AS_due_if_WL_only_promised_CU':5000,'source_eligibility_or_actual_claim_judgment':None},'full_current_country_cost':None,'national_GDP_or_source_yield':None,'actual_public_private_legacy_S_FX_sources':None,'actual_independent_affected_authority':None,'actual_paid_receiving_or_better_lives':None,'unknown_full_current_scope':cfg['unknown_full_current_scope']}

if __name__=='__main__':(D/'results.json').write_text(json.dumps(run(read(D/'inputs.json')),indent=2)+'\n')
