"""Required effective demand, paired cash/stocks and conditional timing.

This is an authored reference, not supply, legal mandate or social superiority.
"""
from fractions import Fraction as F
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent

def Q(x):return F(str(x))
def clean(x):
    if isinstance(x,F):return float(x)
    if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
    if isinstance(x,list):return [clean(v) for v in x]
    return x

def fx_timeline(d,imports,base_interest,factor,years=1):
    o=d['opening'];rate=Q(d['rates']['fx_line_interest']);floor=Q(o['reserve_floor'])
    reserve=Q(o['foreign_reserves']);debt=F(0);limit=Q(o['contingent_fx_limit'])
    monthly_base=(imports+base_interest)/12
    normal_draw=max(F(0),monthly_base-(reserve-floor))
    normal_carry=normal_draw*rate*F(20,360)*12
    normal_exports=imports+base_interest+normal_carry
    rows=[];unpaid=F(0)
    for month in range(1,12*years+1):
        previous_interest=debt*rate*F(10,360)
        due=monthly_base+previous_interest
        use=min(max(F(0),reserve-floor),due);reserve-=use
        draw=min(max(F(0),limit-debt),due-use);debt+=draw
        missed=due-use-draw;unpaid+=missed;peak=debt
        receipt=normal_exports*factor/12
        current_interest=peak*rate*F(20,360)
        interest_paid=min(receipt,current_interest);unpaid+=current_interest-interest_paid
        left=receipt-interest_paid;repay=min(debt,left);debt-=repay;reserve+=left-repay
        rows.append({'month':month,'day1_foreign_due':due,'reserve_used':use,
            'new_draw':draw,'peak_facility_debt':peak,'export_received':receipt,
            'interest':previous_interest+current_interest,'repayment':repay,
            'reserve_close':reserve,'facility_close':debt,'unpaid_cumulative':unpaid})
    return {'normal_export_contract':normal_exports,'normal_line_carry':normal_carry,
        'annual':[{'year':y,'interest':sum(r['interest'] for r in rows[(y-1)*12:y*12]),
                  'exports':sum(r['export_received'] for r in rows[(y-1)*12:y*12]),
                  'reserve_close':rows[y*12-1]['reserve_close'],
                  'facility_close':rows[y*12-1]['facility_close'],
                  'unpaid_cumulative':rows[y*12-1]['unpaid_cumulative']} for y in range(1,years+1)],
        'monthly':rows,'first_unpaid_month':next((r['month'] for r in rows if r['unpaid_cumulative']>0),None)}

def people(d,case,profit,income,im,interest_h):
    c=Q('0.1') if case['insurance_mode']=='current' else F(*d['insurance']['closed_legacy_contribution_exact'])
    policy={**income['policy'],'contribution_rate':c}
    corp=profit*Q(d['rates']['corporate']);distribution=(profit-corp)*Q(case['payout'])
    div_g=distribution*Q(d['opening']['public_equity_share']);div_h=distribution-div_g
    capital_month=(div_h+interest_h)*10**6/(5000*12)
    vat=F(40)*10**6/(100000*12);pits=F(0);caps=F(0);trans=F(40);cons=F(0);contr=F(0);earned=F(0);rows=[]
    for group in income['population_groups']:
        count=group['count'];out=[]
        for person in group['members']:
            m=F(600) if person['kind']=='child' else F(1000);g=Q(person.get('gross',0))
            support=Q(person.get('support_paid',0));received=Q(person.get('support_received',0))
            n=m+300+min(support,F(900));basic=m if person['kind']=='older' else F(0)
            ins=Q(d['insurance']['monthly_earned']) if person['kind']=='older' else F(0)
            credited=ins-min(ins*F('0.2'),m*F('0.2'))
            cap=capital_month if person.get('gross',0)>=10000 else F(0)
            cap_tax=cap*Q(d['rates']['capital_personal']);cap_net=cap-cap_tax
            if case['method']=='current':
                tax,contribution,net=im.tax_and_net(g,policy)
                topup=max(F(0),n-basic-credited-received-vat-cap_net-F('0.5')*max(F(0),net-m*F('0.2')))
                bonus=F(0)
            else:
                contribution=g*c
                bonus=Q(d['work']['bonus_rate'])*min(g-contribution,Q(d['work']['bonus_disregard_monthly']))
                allowance=max(F(0),n-basic-credited-received-vat)
                position=(1-c-Q(case['retention']))*g-allowance-bonus
                tax=max(F(0),position);topup=max(F(0),-position-cap_net)
            disability=Q(person.get('disability_cost',0))
            disposable=g-contribution-tax+basic+ins+received+vat+topup+cap_net-support
            mul=count*12/F(10**6)
            pits+=tax*mul;caps+=cap_tax*mul;contr+=contribution*mul;earned+=ins*mul
            trans+=(basic+topup+disability)*mul;cons+=(disposable+disability)*mul
            out.append({'kind':person['kind'],'gross':g,'work_tax':tax,'contribution':contribution,
                'basic':basic,'insurance_paid':ins,'topup':topup,'bonus':bonus,'capital_net':cap_net,
                'ordinary_disposable_after_support':disposable,'ordinary_declared_need':m+300,
                'excess_over_declared_need':disposable-(m+300),'disability_cost_and_payment':disability})
        rows.append({'group':group['label'],'count':count,'people':out})
    return {'personal_work_tax':pits,'personal_capital_tax':caps,'contributions':contr,
        'insurance_paid':earned,'general_transfer':trans,'consumption_from_available_cash':cons,
        'corporate_tax':corp,'dividend_g':div_g,'dividend_h':div_h,
        'minimum_person_declared_need_margin':min(p['excess_over_declared_need'] for r in rows if r['count'] for p in r['people']),
        'person_groups':rows,'retained_profit':profit-corp-distribution}

def evaluate(d,case,income,im):
    o=d['opening'];rate=Q(d['rates']['government_bond_interest'])
    cfc_g=Q(o['public_real_assets'])*Q(d['rates']['depreciation'])
    cfc_f=Q(o['market_real_assets'])*Q(d['rates']['depreciation']);ig=cfc_g;iv=cfc_f
    service=d['public_services'];cash=Q(service['legacy_cash'])+Q(service['reassigned_wages'])+Q(service['maintenance'])+Q(service['foreign_line_fee'])+Q(case.get('extra_public_cash',0))+Q(case.get('additional_reassigned_pay',0))
    public_wages=Q(service['legacy_wages'])+Q(service['reassigned_wages'])+Q(case.get('additional_reassigned_pay',0));wages=Q(d['work']['wages'])
    mi=d['imports'];hg=Q(mi['households']);ginter=Q(mi['public_intermediate_base'])+Q(mi['maintenance'])+Q(mi['foreign_line_fee'])
    gcap=ig*Q(mi['capital_import_fraction']);fimport=Q(mi['private_intermediate'])+iv*Q(mi['capital_import_fraction'])
    imports=hg+ginter+gcap+fimport
    ih=Q(o['household_bonds'])*rate;is_=Q(o['insurance_bonds'])*rate;ir=Q(o['foreign_bonds'])*rate
    fx=fx_timeline(d,imports,ir,Q(case['export_factor']),2 if Q(case['export_factor'])<1 else 1)
    exports=fx['annual'][0]['exports'];fxinterest=fx['annual'][0]['interest'];interest=ih+is_+ir+fxinterest
    k=cash+cfc_g+ig+iv+exports-imports;p=F(*d['exact_product_tax']);prod=F(155)
    def at(h):
        gdp=h+k;profit=gdp-wages-p*h-prod-cfc_g-cfc_f
        assert profit>0
        return people(d,case,profit,income,im,ih),profit
    a,_=at(F(2000));b,_=at(F(3000));slope=(b['consumption_from_available_cash']-a['consumption_from_available_cash'])/1000
    assert 0<=slope<1
    h=(a['consumption_from_available_cash']-slope*2000)/(1-slope)
    persons,profit=at(h);assert persons['consumption_from_available_cash']==h
    gdp=h+k;flows=[]
    def post(payer,receiver,amount,label):
        assert amount>=0,(label,amount);flows.append({'payer':payer,'receiver':receiver,'amount':amount,'label':label})
    post('H','F',h-p*h-hg,'domestic consumption');post('H','G',p*h,'product tax');post('H','R',hg,'household imports')
    post('R','F',exports,'received-export condition');post('G','H',public_wages,'public wages');post('F','H',wages-public_wages,'market wages')
    post('G','F',cash-public_wages-ginter,'domestic intermediate services');post('G','R',ginter,'public imports incl maintenance/line fee')
    post('G','F',ig-gcap,'domestic replacement capital');post('G','R',gcap,'imported public replacement');post('F','R',fimport,'market intermediate/replacement imports')
    post('F','G',prod,'production levies');post('F','G',persons['corporate_tax'],'corporate tax');post('F','G',persons['dividend_g'],'lawfully owned dividend')
    post('F','H',persons['dividend_h'],'private dividends');post('H','G',persons['personal_work_tax']+persons['personal_capital_tax'],'positive personal taxes')
    post('H','S',persons['contributions'],'restricted levy/contribution');post('S','H',persons['insurance_paid'],'scheduled legacy earned pension')
    post('G','H',persons['general_transfer'],'basic/topup/access/tax relief');post('G','H',ih,'household bond interest')
    post('G','S',is_,'insurance bond interest');post('G','R',ir+fxinterest,'foreign bond/facility interest')
    balances={s:F(0) for s in ['G','H','F','S','R']}
    for t in flows:balances[t['payer']]-=t['amount'];balances[t['receiver']]+=t['amount']
    assert sum(balances.values())==0
    need=max(F(0),-balances['G']);foreign_finance=max(F(0),balances['R'])
    fx_financed=Q(o['foreign_reserves'])-fx['annual'][0]['reserve_close']+fx['annual'][0]['facility_close']
    dom_need=max(F(0),need-fx_financed)
    lenders=max(F(0),balances['F'])+max(F(0),balances['S'])+max(F(0),balances['H'])
    new_bonds=min(F(60),dom_need,lenders);cash_draw=min(Q(o['public_cash'])-Q(o['cash_floor']),max(F(0),dom_need-new_bonds))
    unmet=max(F(0),dom_need-new_bonds-cash_draw)+max(F(0),foreign_finance-fx_financed)
    out=cash+ig+persons['general_transfer']+interest
    receipts=sum(t['amount'] for t in flows if t['receiver']=='G')
    assert receipts-out==balances['G']
    cash_first=Q(o['public_cash'])+new_bonds-out/12
    # Net fiscal FX realization/conversion is conditional on the same usable path.
    cash_last=Q(o['public_cash'])+new_bonds+fx_financed-need
    cash_schedule=[]; running=Q(o['public_cash'])+new_bonds
    previous_reserve=Q(o['foreign_reserves']);previous_facility=F(0)
    for row in fx['monthly'][:12]:
        before_receipts=running-out/12
        net_fx_finance=previous_reserve-row['reserve_close']+row['facility_close']-previous_facility
        running=before_receipts+receipts/12+net_fx_finance
        cash_schedule.append({'month':row['month'],'cash_before_day21_receipts':before_receipts,'net_FX_realization_or_borrowing_credited_day21':net_fx_finance,'cash_close':running})
        previous_reserve=row['reserve_close'];previous_facility=row['facility_close']
    trough=min(row['cash_before_day21_receipts'] for row in cash_schedule)
    assert running==cash_last
    next_same_gap=max(F(0),dom_need-F(60)-max(F(0),cash_last-Q(o['cash_floor'])))
    mature=F(0) if case['rollover'] else Q(o['scheduled_maturity'])
    cash_after_maturity=cash_last-mature*F('0.8');fx_after_maturity=fx['annual'][0]['reserve_close']-mature*F('0.2')
    mature_gap=max(F(0),Q(o['cash_floor'])-cash_after_maturity)+max(F(0),Q(o['reserve_floor'])-fx_after_maturity)
    r=d['resources'];market_gva=gdp-(cash+cfc_g);scale=market_gva/Q(r['private_GVA_reference'])
    energy=Q(r['public_energy'])+Q(case.get('additional_public_energy',0))+Q(r['private_energy_at_GVA_2202'])*scale
    firm=Q(r['firm_energy_opening'])+(Q(r['commissioned_energy_target']) if case['commissioned'] else 0)
    water=Q(r['public_water'])+Q(case.get('additional_public_water',0))+Q(r['private_water_at_GVA_2202'])*scale-(Q(r['verified_saving_target']) if case['commissioned'] else 0)
    extra=Q(r['independent_water_target']) if case['commissioned'] else F(0)
    wa=Q(r['raw_water'])-Q(r['ecological_water'])-Q(r['water_standby'])+extra
    ea=firm-Q(r['energy_standby']);es=firm*F('0.9')-Q(r['energy_standby'])
    ws=Q(r['raw_water'])*F('0.9')-Q(r['ecological_water'])-Q(r['water_standby'])+extra
    additional=case.get('additional_role_targets',{});moved=sum(additional.values())
    staff={k:(F(n)+F(additional.get(k,0)))*(1-Q(d['staffing']['loss_fraction'])) for k,n in d['staffing']['post_stage_if_qualified'].items()}
    staff_required=d['staffing']['required_by_distinct_role']
    private_count=44490-moved;public_count=10510+moved
    payroll=(wages-public_wages)/12
    peak_gap=max(F(0),(Q(o['settlement_deposit_liability'])+payroll)*F('0.6')-Q(o['monetary_reserve_liability']))
    conditional_collateral=Q(case.get('eligible_collateral_face',0))*(1-Q(case.get('collateral_haircut',0)))
    bank_capacity=min(conditional_collateral,Q(case.get('conditional_monetary_liquidity_limit',0)))
    staff_gaps={k:max(F(0),F(staff_required[k])-v) for k,v in staff.items()}
    return {'case':case['name'],'required_GDP_for_declared_demand':gdp,'required_household_consumption':h,'private_required_GVA':market_gva,
      'private_productivity_vs_pre_move_reference':(market_gva/private_count)/(F(2202)/44910),
      'gap_if_total_output_is_only_3000':max(F(0),gdp-3000),
      'public_service_cash':cash,'public_GDP_cost_convention':cash+cfc_g,'public_wages':public_wages,'wages':wages,'product_tax':p*h,'production_levies':prod,'enterprise_taxable_profit':profit,
      'private_gross_replacement':iv,'public_gross_replacement':ig,'public_depreciation':cfc_g,'private_depreciation':cfc_f,'receipts':receipts,'cash_out':out,
      'sector_current_cash_balances':balances,'planned_paired_flows':flows,'people':persons,'exports':exports,'imports':imports,'foreign_bond_interest':ir,'facility_interest':fxinterest,
      'financial_closure_without_new_debt':all(v==0 for v in balances.values()),'conditional_domestic_new_bonds':new_bonds,'conditional_cash_draw':cash_draw,
      'unfunded_cash_reference':unmet,'cash_monthly_first_day':cash_first,'cash_monthly_trough':trough,'monthly_general_cash_schedule':cash_schedule,'cash_close':cash_last,'repeat_same_flow_gap_before_new_interest':next_same_gap,
      'refinancing_principal_due':mature,'next_repeated_maturity_cash_before_changed_flows':cash_after_maturity-mature*F('0.8'),
      'next_repeated_maturity_FX_before_changed_flows':fx_after_maturity-mature*F('0.2'),'cash_after_maturity':cash_after_maturity,'FX_after_maturity':fx_after_maturity,'principal_buffer_gap':mature_gap,
      'fx_timeline':fx,'required_energy':energy,'ordinary_energy_available':ea,'energy_at_10_percent_loss':es,'required_water':water,'ordinary_water_available':wa,'water_at_10_percent_raw_loss':ws,
      'physical_ordinary_fit':energy<=ea and water<=wa,'physical_declared_loss_fit':energy<=es and water<=ws,
      'staff_at_10_percent_loss_if_qualified':staff,'staff_loss_gaps_by_distinct_role':staff_gaps,'public_staff_if_qualified':public_count,'private_staff_after_move':private_count,
      'conditional_bank_liquidity_capacity':bank_capacity,'bank_gap_after_conditionally_approved_capacity':max(F(0),peak_gap-bank_capacity),
      'additional_initial_training_or_sites_cost':None,
      'fixed_input_repetition_preserves_modeled_cash_and_replaced_assets':case['method']=='work_credit' and case['insurance_mode']=='closed_legacy' and case['payout']==1 and case['export_factor']==1 and case['rollover'],
      'actual_ownership_or_pledges':None,'actual_pension_claims_or_supply':None,'unknown_full_function_cost':None,'actual_operating_readiness':False,'observed_superiority':None,
      'private_monthly_payroll':(wages-public_wages)/12,
      'private_working_line_limit':Q(o['private_payroll_working_limit']),
      'private_working_line_needed':(wages-public_wages)/12,
      'peak_bank_deposits_with_working_payroll':Q(o['settlement_deposit_liability'])+(wages-public_wages)/12,
      'peak_bank_60_percent_withdrawal_liquidity_gap':max(F(0),(Q(o['settlement_deposit_liability'])+(wages-public_wages)/12)*F('0.6')-Q(o['monetary_reserve_liability'])),
      'qualification':'Conditional planned ledger. Output is required effective demand, not achieved/attested supply. No current law, I05, pension accrual or ownership schedule is amended.'}

def opening_book(d):
    o=d['opening'];publicshare=Q(o['public_equity_share']);eq=Q(o['market_equity'])
    g=Q(o['public_real_assets'])+Q(o['public_cash'])+Q(o['foreign_reserves'])+Q(o['monetary_foreign_assets'])+publicshare*eq- (Q(o['general_bonds'])-Q(o['monetary_bonds']))-Q(o['monetary_reserve_liability'])
    h=Q(o['household_bonds'])+Q(o['household_cash'])+(1-publicshare)*eq
    s=Q(o['insurance_bonds'])+Q(o['insurance_cash'])
    f=Q(o['market_real_assets'])+Q(o['monetary_reserve_liability'])-Q(o['settlement_deposit_liability'])-eq
    r=Q(o['foreign_bonds'])-Q(o['foreign_reserves'])-Q(o['monetary_foreign_assets'])
    return {'known_net_positions_excluding_pension_symbol':{'G':g,'H':h,'S':s,'F':f,'R':r},
      'pension_H_asset_and_S_liability':'L(t), both unknown; changes must be paired, never zeroed','total_known_real_assets':Q(o['public_real_assets'])+Q(o['market_real_assets']),
      'market_book_equity':eq,'public_market_equity':publicshare*eq,'private_market_equity':(1-publicshare)*eq,
      'opening_transactions_actually_verified':None,'other_household_assets_or_claims':None,
      'producer_subledger':{'real_assets':Q(o['market_real_assets']),'internal_bank_loan':Q(o['internal_market_bank_loan']),'equity':Q(o['market_real_assets'])-Q(o['internal_market_bank_loan'])},
      'bank_subledger':{'producer_loans':Q(o['internal_market_bank_loan']),'monetary_reserves':Q(o['monetary_reserve_liability']),'deposit_liabilities':Q(o['settlement_deposit_liability']),'equity':Q(o['bank_equity'])},
      'monetary_subledger':{'government_bonds':Q(o['monetary_bonds']),'foreign_assets':Q(o['monetary_foreign_assets']),'bank_reserve_liability':Q(o['monetary_reserve_liability'])},
      'bank_reference_withdrawal_60_percent':Q(o['settlement_deposit_liability'])*F('0.6'),
      'bank_liquid_monetary_reserves':Q(o['monetary_reserve_liability']),
      'bank_unfunded_liquidity_without_new_valid_facility':max(F(0),Q(o['settlement_deposit_liability'])*F('0.6')-Q(o['monetary_reserve_liability']))}

def calculate():
    d=json.loads((HERE/'inputs.json').read_text())
    for p,h in d['pinned_sources'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    income=json.loads((ROOT/'2026-10-income-floor/inputs.json').read_text())
    spec=importlib.util.spec_from_file_location('income_reference',ROOT/'2026-10-income-floor/model.py');im=importlib.util.module_from_spec(spec);spec.loader.exec_module(im)
    return clean({'status':'Authored conditional demand/steady-asset/timing references; no case certifies a country','opening':opening_book(d),'cases':[evaluate(d,c,income,im) for c in d['cases']],'limits':d['limits']})

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
