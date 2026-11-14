"""Authored rights-scope and cash examples; no governing or clinical authority."""
from pathlib import Path
from copy import deepcopy
import json
HERE=Path(__file__).resolve().parent
EXPECTED_SCOPE_KEYS=('right_id','holder_authority','territory','recipient','permitted_acts','purpose','period','conditions_met')

def complete_match(old,new,keys):
    if not isinstance(old,dict) or not isinstance(new,dict):raise ValueError('Unsupported rights semantics: supply explicit scoped records')
    if not isinstance(keys,list) or len(keys)!=len(EXPECTED_SCOPE_KEYS) or set(keys)!=set(EXPECTED_SCOPE_KEYS):raise ValueError('Schema change requires a newly interpreted case, not its own permission to reuse')
    for record in [old,new]:
        if set(record)!=set(EXPECTED_SCOPE_KEYS):raise ValueError('Missing or unfamiliar rights fields require explicit interpretation')
        if type(record['conditions_met']) is not bool:raise ValueError('A numeric flag is not an interpreted Boolean condition')
        if any(not isinstance(record[k],str) or not record[k] for k in EXPECTED_SCOPE_KEYS if k not in ['conditions_met','permitted_acts']):raise ValueError('Unsupported right or authority meaning')
        acts=record['permitted_acts']
        if not isinstance(acts,list) or not acts or any(not isinstance(v,str) or not v for v in acts) or len(set(acts))!=len(acts):raise ValueError('Unsupported acts need interpretation')
    return all(old[k]==new[k] for k in EXPECTED_SCOPE_KEYS) and old['conditions_met'] is True and new['conditions_met'] is True and old['holder_authority']=='fixture_verified'

def calculate(c=None):
    if c is None:c=json.loads((HERE/'inputs.json').read_text())
    if not isinstance(c,dict) or not c:raise ValueError('Explicit incomplete input cannot silently become the baseline')
    a=c['medicine'];q=a['quoted_current_supply'];match=complete_match(a['valid_prior_license'],a['requested_license'],c['scope_keys'])
    quote=sum(q.values());duplicate=q['same_foreground_license_fee'] if match else None
    net=quote-duplicate if duplicate is not None else None
    # A quote is not a legal finding that an unmatched new fee is payable.
    med=dict(quoted_supply=quote,scope_matched=match,duplicate_fee_if_already_bought=duplicate,
        distinct_current_uses_quote=net,prior_period_research_grant=a['prior_research_grant'],
        prior_and_current_distinct_cash_uses=a['prior_research_grant']+net if net is not None else None,
        nominal_quote_budget_test=a['fixture_current_CU_quote_cash']>=net if net is not None else None,
        fixture_foreign_quote_gap=max(0,q['foreign_API_packaging']-a['fixture_owned_foreign_quote_equivalent']),
        actual_payment_obligation_or_royalty=None,actual_safe_supply=None,actual_public_return=None)
    b=c['software'];fallback=b['background_permission_quote']+b['paid_staff_practice']+b['hardware_spares_security_testing']
    software=dict(foreground_grant=b['foreground_grant'],distinct_fallback_uses_quote=fallback,
        combined_quote_uses=b['foreground_grant']+fallback,optional_prize_plus_same_fallback_quote=b['optional_prize_instead_of_grant']+fallback,
        prize_requires_entrants_to_finance_attempts=True,background_permission_obtained=b['background_permission_obtained'],
        actual_qualified_receiver=b['actual_qualified_receiver'],actual_safe_operation=None,actual_net_saving=None)
    d=c['creator'];creator=dict(public_commission_quote=sum(d['commission_costs'].values()),
        public_use_scope=d['public_rights_purchased'],forecast_private_royalty=d['forecast_private_royalty'],
        public_royalty_source_credited=d['fixture_received_royalty'] if (d['public_royalty_title'] is True and d['fixture_receipt_verified'] is True and d['fixture_receipt_owned_unrestricted'] is True and isinstance(d['fixture_received_royalty'],(int,float)) and not isinstance(d['fixture_received_royalty'],bool) and d['fixture_received_royalty']>=0) else 0,
        actual_receipt_or_tax_or_source=d['actual_receipts'],actual_additional_archive_or_training_permission=None)
    e=c['delayed_medicine'];months=e['months'];delay=e['months_before_safe_alternative_hypothesis']
    if not 0<=delay<=months or months<=0 or e['annual_units']<0:raise ValueError('Unsupported period/quantity; cannot assume negative time')
    monthly=e['annual_units']/months;new_price=sum(e['new_unit_quotes_CU'].values());initial=e['initial_knowhow_quote_CU']+e['initial_validation_quote_CU']
    bridge=monthly*delay*e['incumbent_unit_quote_CU'];remaining=monthly*(months-delay)*new_price
    transition=dict(annual_units=e['annual_units'],new_unit_quote_CU=new_price,initial_distinct_uses_CU=initial,
        bridge_units=monthly*delay,bridge_quote_CU=bridge,first_year_alternative_units=monthly*(months-delay),
        first_year_alternative_supply_quote_CU=remaining,first_year_combined_quote_CU=bridge+remaining+initial,
        retained_incumbent_annual_quote_CU=e['annual_units']*e['incumbent_unit_quote_CU'],
        later_full_year_named_quote_CU=e['annual_units']*new_price,actual_qualified_acceptance=e['actual_safe_acceptance'],
        actual_finance_or_full_manufacturing_cost=e['actual_source'])
    f=c['operator_royalty'];public=f['public_procurer_validly_assumes_royalty'];due=f['fixture_royalty_due']
    released=f['rights_holder_validly_releases_operator']
    if released and not public:raise ValueError('Unspecified release without a valid replacement obligation needs separate interpretation')
    royalty=dict(due=due,due_day=f['due_month_day'],future_receipt_day=f['receipt_expected_month_day'],
        owned_operator_due_day_cash=f['fixture_owned_unrestricted_due_day_cash'],unreceived_invoice_not_credited=f['future_invoice_receivable'],
        fixture_operator_gap=max(0,due-f['fixture_owned_unrestricted_due_day_cash']) if not released else None,
        named_operator_liability=0 if released else due,express_public_assumption_liability=due if public else 0,
        single_royalty_claim_total=due,no_double_recovery_across_overlapping_payers=True,
        automatic_Treasury_guarantee=False,actual_source_or_receipt=f['actual_source_or_receipt'],
        actual_safe_receiving_or_remedy=None)
    return dict(edition=95,status=c['status'],medicine=med,software=software,creator=creator,
        delayed_medicine=transition,operator_royalty=royalty,actual=deepcopy(c['actual']))

if __name__=='__main__':(HERE/'results.json').write_text(json.dumps(calculate(),indent=2)+'\n')
