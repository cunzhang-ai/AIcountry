"""Authored sector-flow/owned-FX comparison; independent of the100k country quantities."""
from pathlib import Path
from decimal import Decimal as Q
import json
D=Path(__file__).resolve().parent
q=lambda x:Q(str(x))
read=lambda p:json.loads(p.read_text())
def clean(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,list):return [clean(v) for v in x]
 return x

def circuit(cfg,scenario):
 expected={'id','u_per_f','export_f','voluntary_offer_of_after_own_import_surplus','public_owned_opening_f','public_floor_f','gross_annual_public_sale_cap_f','bond_offer_u','finance','fiscal_issue_cap_u','issue_authorized_periods','bond_authorized_periods'}
 if set(scenario)!=expected:raise ValueError('Uninterpreted strategy/ownership meaning retained for review')
 if scenario['finance'] not in ['bonds','finite_fiscal_issue']:raise ValueError('Unsupported monetary authority')
 if any(type(scenario[k]) is not int or scenario[k]<0 for k in ['issue_authorized_periods','bond_authorized_periods']):raise ValueError('Unsupported authorization period')
 v=cfg['flows'];r=q(scenario['u_per_f']);exports=q(scenario['export_f']);offer=q(scenario['voluntary_offer_of_after_own_import_surplus'])
 if r<=0 or exports<0 or not 0<=offer<=1:raise ValueError('Invalid authored source quantities')
 public=q(scenario['public_owned_opening_f']);floor=q(scenario['public_floor_f']);cap=q(scenario['gross_annual_public_sale_cap_f'])
 if public<floor or floor<0 or cap<0:raise ValueError('Invalid owned public foreign stock/limit')
 hp=q(v['household_import_f']);fp=q(v['firm_import_f'])
 private_sale=min(hp,max(Q(0),exports-fp)*offer)
 private_retained=max(Q(0),exports-fp)-private_sale
 G_to_H=hp-private_sale;G_to_F=max(Q(0),fp-exports);public_sale=G_to_H+G_to_F
 Gpay=q(v['public_pay_u']);Gbuy=q(v['public_purchase_u']);transfer=q(v['public_transfer_u']);HT=q(v['household_tax_u']);FT=q(v['firm_tax_u']);Fpay=q(v['firm_pay_u']);HC=q(v['household_domestic_consumption_u'])
 deficit=Gpay+Gbuy+transfer-HT-FT
 H=Gpay+Fpay+transfer-HT-HC-hp*r
 F=Gbuy+HC+exports*r-Fpay-fp*r-FT
 W=(hp+fp-exports)*r
 cash_finance=deficit-public_sale*r
 if cash_finance<0:raise ValueError('Surplus/redemption semantics need an explicit adapter')
 Fcash=Gbuy+HC-Fpay-FT+private_sale*r-G_to_F*r
 periods=[];first_FX=None;first_finance=None
 for period in range(1,cfg['repeat_periods_for_conditional_foreign_stress']+1):
  foreign_ok=public_sale<=cap and public-public_sale>=floor
  financing_ok=cash_finance<=q(scenario['bond_offer_u']) and period<=scenario['bond_authorized_periods'] if scenario['finance']=='bonds' else cash_finance<=q(scenario['fiscal_issue_cap_u']) and period<=scenario['issue_authorized_periods']
  if not foreign_ok and first_FX is None:first_FX=period
  if not financing_ok and first_finance is None:first_finance=period
  after=public-public_sale if foreign_ok else None
  periods.append({'period':period,'authored_opening_public_f':public,'requested_public_FX_sale_f':public_sale,'foreign_only_stress_closing_f':after,
                  'foreign_title_floor_and_gross_cap_pass':foreign_ok,'separate_domestic_finance_authority_or_offer_pass':financing_ok,
                  'scope':'FX-only repetition assumes the same completed physical/receipt flows, even if the separate finance test fails. Not an executed path or renewed authority.'})
  if foreign_ok:public=after
  else:break
 return {'id':scenario['id'],'unit':'u and f are independent authored circuit units; no conversion/scale to country CU/FU or GDP.',
         'net_public_nonfinancial_borrowing_u':deficit,'household_net_financial_lending_u':H,
         'firm_and_financial_sector_net_financial_lending_u':F,'rest_of_world_net_financial_lending_u':W,
         'balance_identity_residual_u':-deficit+H+F+W,
         'public_owned_FX_sold_f':public_sale,'household_FX_from_public_f':G_to_H,'firm_FX_from_public_f':G_to_F,
         'private_owned_surplus_voluntarily_sold_f':private_sale,'private_owned_surplus_retained_f':private_retained,
         'new_public_domestic_claims_needed_u':cash_finance,'household_domestic_claim_increase_u':H,
         'firm_sector_domestic_claim_increase_u':Fcash,'private_FX_asset_increase_u':private_retained*r,
         'next_period_5percent_cost_on_new_domestic_public_claims_u':cash_finance*q('.05'),
         'first_foreign_stock_or_gross_limit_failure_in_conditional_repetition':first_FX,
         'first_separate_finance_failure_before_foreign_stress_stops':first_finance,'periods':periods,
         'actual_suppliers_receipts_sources_holders_authority_output_or_inflation':None}

def compute(cfg=None):
 cfg=read(D/'inputs.json') if cfg is None else cfg
 if set(cfg)!={'edition','scope','flows','repeat_periods_for_conditional_foreign_stress','scenarios'} or cfg['edition']!=133:raise ValueError('Uninterpreted country/circuit concept')
 fields={'public_pay_u','public_purchase_u','public_transfer_u','household_tax_u','firm_tax_u','firm_pay_u','household_domestic_consumption_u','household_import_f','firm_import_f'}
 if set(cfg['flows'])!=fields or any(q(v)<0 for v in cfg['flows'].values()):raise ValueError('Unknown or invalid transaction definition')
 if type(cfg['repeat_periods_for_conditional_foreign_stress']) is not int or cfg['repeat_periods_for_conditional_foreign_stress']<=0:raise ValueError('Invalid stress horizon')
 return clean({'edition':133,'format_revision':'133-conditional-sector-circuit-v1','cases':[circuit(cfg,s) for s in cfg['scenarios']],
               'scope':cfg['scope'],'actual_country_net_borrowing_or_output_or_ready_source':None})
if __name__=='__main__':(D/'results.json').write_text(json.dumps(compute(),indent=2)+'\n')
