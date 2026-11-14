"""Planned five-sector reference with GDP, finance and resource identities.

No identity supplies cash, authority, independent control or actual production.
"""

from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def clean(v):
    if isinstance(v,F):return float(v)
    if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
    if isinstance(v,list):return [clean(x) for x in v]
    return v


def evaluate(data,case,income_module,income_data):
    scale=F(str(case['wage_scale']));gdp=F(case['gdp'])
    wages=F(2280)*scale; public_wages=F(400)*scale
    service_cash=F(374)+public_wages
    cfc_public=F(24)*scale;cfc_private=F(96)*scale
    government_consumption=service_cash+cfc_public
    public_capital=F(case['public_capital']);private_capital=F(case['private_capital'])
    household_consumption=gdp-government_consumption-public_capital-private_capital
    products_tax=household_consumption*F(265,1800)
    production_tax=F(155)*scale
    gross_surplus=gdp-wages-products_tax-production_tax
    private_gross_surplus=gross_surplus-cfc_public
    taxable_profit=private_gross_surplus-cfc_private
    assert taxable_profit>=0
    corp=taxable_profit*F(str(case['corporate_rate']))
    distribution=(taxable_profit-corp)*F('0.5')
    public_share=F(str(case['public_share']))
    dividend_public=distribution*public_share
    dividend_household=distribution-dividend_public
    # Acquisition is financed debt in this branch; not an assumed free transfer.
    purchase=F(1920)*scale*max(F(0),public_share-F('0.25'))
    purchase_interest=purchase*F('0.05')
    household_interest=F(20)+purchase_interest
    insurance_interest=F(5);foreign_interest=F('6.5')
    interest=household_interest+insurance_interest+foreign_interest
    capital_cash_per_owner=(dividend_household+household_interest)*F(10**6)/(5000*12)
    rebate_monthly=F(40)*F(10**6)/(100000*12)
    labour_tax=F(0);capital_tax=F(0);general_transfer=F(0);insurance_benefits=F(0)
    contribution=F(0);population=0
    p=income_data['policy']
    for group in income_data['population_groups']:
        for original in group['members']:
            person=dict(original);count=group['count'];population+=count
            gross=F(str(person.get('gross',0)))*scale
            monthly=F(1000)*(F('0.6') if person['kind']=='child' else 1)
            needed_support=min(F(str(person.get('support_paid',0))),F(900))
            needs=monthly+300+needed_support
            basic=monthly if person['kind']=='older' else F(0)
            insurance=F(250) if person['kind']=='older' else F(0)
            credited_insurance=insurance-min(insurance*F('0.2'),monthly*F('0.2'))
            capital=capital_cash_per_owner if original.get('gross',0)>=10000 else F(0)
            capital_due=capital*F('0.4')
            nonwork=basic+credited_insurance+rebate_monthly+F(str(person.get('support_received',0)))+capital-capital_due
            tax,contr,net=income_module.tax_and_net(gross,p)
            if case['income_method']=='current':
                topup=max(F(0),needs-nonwork-F('0.5')*max(F(0),net-monthly*F('0.2')))
            else:
                # Candidate alternative, not a revision of adopted I05 or an automatic set-off.
                credit=max(F(0),needs-nonwork)
                retained=F(str(case.get('retained_work_share',0.25)))
                position=(F(1)-F('0.1')-retained)*gross-credit
                tax=max(F(0),position);topup=max(F(0),-position)
            multiplier=count*12/F(10**6)
            labour_tax+=tax*multiplier;capital_tax+=capital_due*multiplier
            general_transfer+=(basic+topup+F(str(person.get('disability_cost',0))))*multiplier
            insurance_benefits+=insurance*multiplier;contribution+=contr*multiplier
    assert population==100000
    general_transfer+=40  # Actual separately paid relief, already credited in need.
    revenues=labour_tax+capital_tax+products_tax+production_tax+corp+dividend_public
    current_cash_out=service_cash+general_transfer+interest
    recurring_balance=revenues-current_cash_out
    deficit=current_cash_out+public_capital-revenues
    cash_room=F(60)+F(50)
    financing_gap=max(F(0),deficit-cash_room)
    funded_borrowing=min(F(60),max(F(0),deficit))
    cash_draw=min(F(50),max(F(0),deficit-funded_borrowing))
    imports=F(case['imports']);exports=F(case['exports'])
    h_import=imports*F(280,600);g_import=imports*F(110,600)
    f_import=imports-h_import-g_import
    public_intermediate_import=imports*F(80,600)
    public_cap_import=g_import-public_intermediate_import
    assert public_cap_import<=public_capital and public_intermediate_import<=374
    # Entries are planned obligations/transactions, not claims that payments happened.
    flows=[]
    def post(payer,receiver,amount,label):
        assert amount>=0,(label,amount)
        flows.append({'payer':payer,'receiver':receiver,'amount':amount,'label':label})
    post('H','F',household_consumption-products_tax-h_import,'domestic consumption before product tax')
    post('H','G',products_tax,'product tax');post('H','R',h_import,'household imports')
    post('R','F',exports,'exports');post('G','H',public_wages,'public wages')
    post('F','H',wages-public_wages,'market-enterprise wages')
    post('G','F',F(374)-public_intermediate_import,'domestic public intermediate purchases')
    post('G','R',public_intermediate_import,'public intermediate imports')
    post('G','F',public_capital-public_cap_import,'domestic public capital')
    post('G','R',public_cap_import,'public capital imports');post('F','R',f_import,'private investment/intermediate imports')
    post('F','G',production_tax,'land/ecological/business production taxes')
    post('F','G',corp,'corporate income tax');post('F','G',dividend_public,'public portfolio dividend')
    post('F','H',dividend_household,'private dividend')
    post('H','G',labour_tax+capital_tax,'personal net charges, positive component')
    post('H','S',contribution,'restricted employee contribution')
    post('S','H',insurance_benefits,'earned pension paid in full')
    post('G','H',general_transfer,'general payments including paid tax relief')
    post('G','H',household_interest,'domestic household interest')
    post('G','S',insurance_interest,'insurance-held government interest')
    post('G','R',foreign_interest,'foreign government interest')
    balances={s:F(0) for s in ['H','F','G','S','R']}
    for flow in flows:balances[flow['payer']]-=flow['amount'];balances[flow['receiver']]+=flow['amount']
    resource=data['resources']
    energy_need=F(320)+F(600)*scale
    water_need=F(2)+F(4)*scale
    energy_available=F(resource['firm_energy'])-F(resource['energy_standby'])
    water_available=F(resource['raw_water'])-F(resource['ecological_water'])-F(resource['water_standby'])
    fx_need=max(F(0),imports+foreign_interest-exports)
    fx_gap=max(F(0),fx_need-F(25))
    fx_shock_gap=max(F(0),imports+foreign_interest-exports*F('0.9')-25)
    closing_cash=F(150)-cash_draw+max(F(0),-deficit)
    repeated_gap=max(F(0),deficit-F(60)-max(F(0),closing_cash-F(100)))
    return {'case':case['name'],'GDP':gdp,'wages':wages,'cash_public_services':service_cash,
      'GDP_public_consumption':government_consumption,'household_consumption':household_consumption,
      'public_capital':public_capital,'private_capital':private_capital,
      'product_tax':products_tax,'other_production_tax':production_tax,
      'gross_operating_surplus':gross_surplus,'enterprise_taxable_profit':taxable_profit,
      'corporate_tax':corp,'public_dividend':dividend_public,'private_dividend':dividend_household,
      'acquisition_price':purchase,'acquisition_interest':purchase_interest,
      'opening_acquisition_bridge':{'proposed_extra_debt':purchase,'proposed_extra_equity_asset':purchase,'required_prior_financing':purchase,'actually_committed':None},
      'personal_charges':labour_tax+capital_tax,'general_transfer':general_transfer,
      'restricted_contributions':contribution,'insurance_paid':insurance_benefits,
      'receipts':revenues,'recurring_cash_balance':recurring_balance,
      'planned_general_financing_need':max(F(0),deficit),'funded_new_borrowing':funded_borrowing,
      'cash_draw':cash_draw,'unfunded_cash':financing_gap,
      'closing_general_cash':closing_cash,'repeat_same_operations_cash_gap':repeated_gap,
      'repeat_qualification':'Unchanged annual flows/limits before debt-interest, prices or investment effects; not a multiyear forecast',
      'planned_sector_balances':balances,'planned_flows':flows,
      'household_planned_financing_need':max(F(0),-balances['H']),
      'enterprise_planned_financing_need':max(F(0),-balances['F']),
      'conditional_combined_G_F_balance':balances['G']+balances['F'],
      'control_classification':'Actual public-sector/control scope unknown; combination is a counterfactual consolidation, not classification by share alone',
      'foreign_interest':foreign_interest,'imports':imports,'exports':exports,
      'foreign_currency_gap':fx_gap,'export_shock_FX_gap':fx_shock_gap,
      'energy_requirement':energy_need,'energy_available':energy_available,
      'energy_gap':max(F(0),energy_need-energy_available),
      'water_requirement':water_need,'water_available':water_available,
      'water_gap':max(F(0),water_need-water_available),
      'depreciation_public':cfc_public,'depreciation_private':cfc_private,
      'care_staff_shock_gap':155,'institutional_staff_shock_gaps':[82,82],
      'unknown_full_function_cost':None,'observed_outcomes':None,
      'qualification':'Planned accounting identities only. Larger GDP/wages with fixed basket is an assumption, not observed productivity or an attainable transition. No financial surplus certifies physical, legal or democratic readiness.'}


def calculate():
    data=json.loads((HERE/'inputs.json').read_text())
    for source,digest in data['pinned_sources'].items():
        if hashlib.sha256((ROOT/source).read_bytes()).hexdigest()!=digest:raise ValueError(source)
    spec=importlib.util.spec_from_file_location('income_reference',ROOT/'2026-10-income-floor/model.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    income=json.loads((ROOT/'2026-10-income-floor/inputs.json').read_text())
    return clean({'status':data['status'],'cases':[evaluate(data,c,module,income) for c in data['cases']],
      'actual_national_feasibility':'unestablished','actual_cost':None,'limits':data['limits']})


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
