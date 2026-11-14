"""Explicit design88 derivative of the frozen design87 solve function.
The accompanying solve-changes.diff exposes every equation change. Prices,
public terms, cohorts and tax helper are scoped imports; no prior validator runs.
Investment phases are conditional annual cross-sections, not a funded trajectory.
"""
from model import baseline, households
public_terms=baseline.public_terms
prices=baseline.prices
SECTORS=baseline.SECTORS
def solve(c,p):
    t=public_terms(c);v=c['production'];price=prices(c,p);pub=c['public'];r=c['receiving'];fin=c['finance'];rep=c['replacement']
    WG=t['WG'];WE=t['WE'];OE=t['OE'];OG=t['OG'];DG=t['DG'];DE=t['DE'];B=t['B'];PE=t['PE']
    inv=c.get('investment',{});build=inv.get('build',0);newCFC=inv.get('CFC',0);reserve=inv.get('reserve',0);newstock=inv.get('opening_stock',0)
    coupon={holder:value*pub['G_coupon_rate'] for holder,value in pub['G_debt_initial_by_holder'].items()}
    # Extra participant wages are explicit household receipts; base worker compensation stays2,280. Backfill/public direct work reattributes that wage bill once.
    Wtot=sum(g['count']*sum(a.get('gross',0)*12 for a in g['members']) for g in c['household']['groups'])/1e6+c['baseline86']['participant_wages'];WF=Wtot-WG-WE
    DF=v['private_housing_units']*v['structure_value_unit']/v['structure_life']+v['nonhousing_F_stock']/v['nonhousing_F_life']+newCFC
    inventory=r['peak_people']*r['starting_inventory_days']*r['supply_place_night']
    JG=pub['G_renewal_fraction']*DG+pub['new_retrofit_G']+inventory;JE=pub['E_renewal_fraction']*DE+pub['new_retrofit_E'];JF=DF-newCFC+build
    # Import replacement asset scopes attributed once; new receiving structures use20%import share.
    MG=rep['G_operating_import_base']+.91*.2+.285*.3+.08*.7+.024*.2+.007616*.9
    ME=rep['E_operating_import_base']-.06*.2-.285*.3
    MIG=pub['G_renewal_fraction']*(rep['G_import_CFC_base']-.3*.2+(100/30)*.2+(.15))+pub['new_retrofit_G']*.5+inventory*.3
    MIE=pub['E_renewal_fraction']*(rep['E_import_CFC_base']-.2*.2)+pub['new_retrofit_E']*.5
    MIF=(v['private_housing_units']*v['structure_value_unit']/v['structure_life'])*v['F_renewal_housing_import_share']+(v['nonhousing_F_stock']/v['nonhousing_F_life'])*v['F_renewal_other_import_share']+build*inv.get('build_import_share',0)
    CIT_E=max(0,PE)*v['corporate_tax_rate'];D_E=max(0,PE-CIT_E)*v['posttax_profit_payout_fraction']
    def at(Q):
        MI=Q*v['other_F_intermediate_import_share_of_gross_output']-min(inv.get('displaced_imports',0),Q*v['other_F_intermediate_import_share_of_gross_output'])+inv.get('operating_imports',0);VA=Q-MI
        if MI<0:raise ArithmeticError('Named import displacement exceeds aggregate input scope')
        op_profit=VA-WF-DF-price['land_tax'];taxprofit=op_profit+coupon['F'];CIT=max(0,taxprofit)*v['corporate_tax_rate'];D=max(0,taxprofit-CIT)*v['posttax_profit_payout_fraction']
        h=households(c,p,price,D+D_E,coupon['H']);MH=h['ordinary_pre_tax']*v['H_ordinary_import_share']
        demand=h['H_consumption']-h['VAT']-h['G_rent']-MH+OG-MG+OE-ME+JG-MIG+JE-MIE+JF-MIF+v['exports']
        return dict(Q=Q,MI=MI,VA=VA,op_profit=op_profit,taxprofit=taxprofit,CIT=CIT,D=D,h=h,MH=MH,demand=demand)
    lo,hi=0,20000
    if at(lo)['demand']<lo or at(hi)['demand']>hi:raise ArithmeticError('No bracketed planned-output fixed point; do not force closure')
    for _ in range(80):
        mid=(lo+hi)/2;a=at(mid)
        if a['demand']>mid:lo=mid
        else:hi=mid
    a=at((lo+hi)/2);h=a['h'];M=a['MI']+a['MH']+MG+ME+MIG+MIE+MIF
    contrib=h['contributions'];Sback=max(0,h['pensions']+pub['S_admin_service_payment_to_G']-contrib-coupon['S']-pub['S_credit_transfer'])
    transactions=[];cash={s:0.0 for s in SECTORS}
    def pay(fr,to,amount,kind):
        cash[fr]-=amount;cash[to]+=amount;transactions.append({'payer':fr,'receiver':to,'amount_mCU':amount,'purpose':kind})
    for fr,w in [('G',WG),('E',WE),('F',WF)]:pay(fr,'H',w,'gross compensation')
    pay('H','S',contrib,'restricted wage contributions');pay('H','G',h['personal_tax'],'joint individual wage/pension/dividend/interest tax')
    pay('G','H',h['general_transfers'],'basic plus I05 and matching access compensation');pay('S','H',h['pensions'],'gross indexed earned and survivor pensions')
    pay('G','S',pub['S_credit_transfer'],'current credit transfer, not actuarial price');pay('G','S',Sback,'explicit current insurance-payment backing');pay('S','G',pub['S_admin_service_payment_to_G'],'administration already supplied in G')
    for holder,val in coupon.items():pay('G',holder,val,'opening public debt coupon')
    pay('E','G',CIT_E,'E corporate tax');pay('F','G',a['CIT'],'F corporate tax');pay('F','G',price['land_tax'],'private site-value levy')
    pay('E','H',D_E,'actual E cash dividend');pay('F','H',a['D'],'actual F cash dividend')
    pay('H','G',h['G_rent'],'public housing rent once');pay('H','G',h['VAT'],'consumer product tax once')
    pay('H','R',a['MH'],'ordinary final imports');pay('H','F',h['H_consumption']-h['G_rent']-h['VAT']-a['MH'],'domestic ordinary/rent purchases')
    for fr,op,imp,cap,capimp in [('G',OG,MG,JG,MIG),('E',OE,ME,JE,MIE)]:
        pay(fr,'R',imp,'imported operating inputs');pay(fr,'F',op-imp,'domestic operating inputs');pay(fr,'R',capimp,'imported actual capital/inventory');pay(fr,'F',cap-capimp,'domestic actual capital/inventory')
    pay('F','R',a['MI'],'market intermediate imports');pay('F','R',MIF,'F capital imports');pay('R','F',v['exports'],'authored exported output')
    # Own-account domestic F capital is output/investment but no F-to-F external cash transfer.
    pay('G','E',B,'commissioned service invoice');pay('G','E',pub['G_equity_subscription_to_E'],'financial equity subscription, not GDP investment again');pay('G','H',pub['campaign_restricted_transfer'],'restricted party/campaign cash, outside private consumption')
    QG=WG+OG+DG;VAG=WG+DG;VAE=B-OE;GDPbasic=VAG+VAE+a['VA'];GDP=GDPbasic+h['VAT']
    Cpublic=QG+B-h['G_rent'];GDPex=h['H_consumption']+Cpublic+JG+JE+JF+v['exports']-M
    # Due principal and willingness are separate from new financial saving; no fresh deposit or S sweep plugs an unmatched requirement.
    opening=fin['opening_settlement_claim_on_R'];mature={k:v*fin['maturing_principal_fraction'] for k,v in pub['G_debt_initial_by_holder'].items()};roll={k:v*fin['refinance_offer_fraction'] for k,v in mature.items()};unrolled=sum(mature[k]-roll[k] for k in mature)
    G_earmark=max(0,DG-pub['G_renewal_fraction']*DG)
    offers={'H':max(0,cash['H']-pub['campaign_restricted_transfer'])*fin['H_new_bond_share_of_voluntary_saving'],'F':max(0,cash['F']-(coupon['F']*(1-v['corporate_tax_rate'])*(1-v['posttax_profit_payout_fraction']))-reserve)*fin['F_new_bond_share_of_unrestricted_retention'],'E':max(0,cash['E']-max(0,DE-pub['E_renewal_fraction']*DE))*fin['E_new_bond_share_of_unrestricted_retention'],'S':fin['S_new_G_bond_offer'],'R':fin['foreign_new_bond_offer_cap']}
    need=max(0,fin['G_minimum_unrestricted_cash']+G_earmark-opening['G']-cash['G']+unrolled)
    accepted={};left=need
    for holder in ['H','F','E','R','S']:
        accepted[holder]=min(left,offers[holder]);left-=accepted[holder]
    # Closing positions are conditional all-payment plans; negative availableG/left makes them unexecutable, not lawful unpaid money or a loan.
    closing={k:opening[k]+cash[k] for k in opening}
    for holder in accepted:
        if holder!='R':closing[holder]+=mature.get(holder,0)-roll.get(holder,0)-accepted[holder]
    closing['G']-=unrolled;closing['G']+=sum(accepted.values())
    debt={k:pub['G_debt_initial_by_holder'].get(k,0)-mature.get(k,0)+roll.get(k,0)+accepted.get(k,0) for k in set(pub['G_debt_initial_by_holder'])|set(accepted)}
    closingRliability=sum(opening.values())-cash['R']-mature['R']+roll['R']+accepted['R']
    fixedFcapacity=t['remaining_market_FTE']*v['market_GVA_per_worker']
    return {'policy':p['id'],'prices':price,'public_terms':t,'household':h,'F_output':a['Q'],'F_GVA':a['VA'],'F_operating_profit':a['op_profit'],'F_taxable_profit_with_coupon':a['taxprofit'],'F_CIT':a['CIT'],'E_CIT':CIT_E,'F_dividend':a['D'],'E_dividend':D_E,'F_wages':WF,'actual_capital_plan':{'G':JG,'E':JE,'F':JF,'G_inventory':inventory},'GDP_basic':GDPbasic,'product_tax':h['VAT'],'GDP_purchasers':GDP,'GDP_expenditure':GDPex,'imports_total':M,'exports':v['exports'],'planned_output_residual':a['demand']-a['Q'],'planned_sector_cash_before_financing':cash,'transactions':transactions,'S_current_backing':Sback,'G_renewal_still_own_asset':G_earmark,'E_renewal_retained_cash':max(0,DE-pub['E_renewal_fraction']*DE),'finance':{'opening_claims_on_R':opening,'maturing_principal':mature,'rollover_offers':roll,'unrolled_principal':unrolled,'new_bond_offers':offers,'accepted_new_bonds':accepted,'funding_requirement':need,'unmatched_requirement':left,'unexecuted_cash_residuals_after_disclosed_sources':closing,'valid_closing_cash_assets':closing if left<1e-7 and min(closing.values())>=0 else None,'negative_G_is_unmatched_request_not_overdraft':True,'planned_closing_G_debt_by_holder':debt,'R_liability_diagnostic_if_all_planned_payments_were_funded':closingRliability,'next_year_coupon_if_same_rate':sum(debt.values())*pub['G_coupon_rate'],'executed_financing':None},'capital_positions':{'opening':{'G':t['KG'],'E':t['KE'],'F':v['private_housing_units']*v['structure_value_unit']+v['nonhousing_F_stock']+newstock},'closing':{'G':t['KG']+JG-inventory-DG,'E':t['KE']+JE-DE,'F':v['private_housing_units']*v['structure_value_unit']+v['nonhousing_F_stock']+newstock+JF-DF},'G_claim_on_E_equity':pub['G_equity_subscription_to_E'],'nondepreciating_land_separate':{'G':v['public_housing_units']*v['private_site_value_unit'],'F':v['private_housing_units']*v['private_site_value_unit']},'conditional_book_claims_not_executed':{'opening_H_claim_on_E':t['KE']+opening['E'],'closing_H_claim_on_E':t['KE']+JE-DE+closing['E']+debt.get('E',0)-pub['G_equity_subscription_to_E'],'opening_H_claim_on_F':v['private_housing_units']*v['structure_value_unit']+v['nonhousing_F_stock']+newstock+v['private_housing_units']*v['private_site_value_unit']+pub['G_debt_initial_by_holder']['F']+opening['F'],'closing_H_claim_on_F':v['private_housing_units']*v['structure_value_unit']+v['nonhousing_F_stock']+newstock+v['private_housing_units']*v['private_site_value_unit']+debt['F']+closing['F']+JF-DF},'legacy_bank_reference':{'opening_G_exposure':175,'closing_G_exposure_before_any_nonbank_new_claims':pub['G_debt_initial_by_holder']['F']-mature['F']+roll['F'],'opening_equity_hypothesis':200,'retention_ringfence':(coupon['F']*(1-v['corporate_tax_rate'])*(1-v['posttax_profit_payout_fraction'])),'all_new_F_G_claims_are_nonbank':True,'actual_qualified_bank_or_lender':None},'unknown_pension_asset_H_and_liability_S':None},'nominal_value_benchmark_comparisons':[{'nominal_benchmark_multiplier':z,'authored_GVA_benchmark':fixedFcapacity*z,'required_minus_benchmark':a['VA']-fixedFcapacity*z,'actual_achieved_capacity':None} for z in v['capacity_multipliers']],'F_reserved_cash_mCU':reserve+inv.get('reserve_after_prior_offer',0),'F_unrestricted_closing_request_mCU':closing['F']-reserve-inv.get('reserve_after_prior_offer',0),'investment_phase':inv,'F_CFC':DF,'unknown_impairment_adjustment_mCU':None,'capital_stock_is_pre_impairment_book_reference':True,'F_intermediate_imports':a['MI'],'F_capital_imports':MIF,'nominal_frontier_is_not_physical_supply_test':True,'actual':c['actual']}
