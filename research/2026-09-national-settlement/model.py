"""Conditional accounting for the country design, not an economic forecast."""
import json
from pathlib import Path


def calculate(data):
    results = []
    for scenario_id, shock in data['scenarios'].items():
        for package_id, package in data['packages'].items():
            cash, debt, arrears = data['opening_cash'], data['opening_debt'], 0
            years = []
            for i, year in enumerate(data['years']):
                active = shock.get('year') == year
                revenue = sum(v[i] for v in data['revenue'].values())
                revenue *= shock.get('revenue_factor', 1) if active else 1
                services = sum(s['expand_cost' if package['expand'] else 'retain_cost'][i]
                               for s in data['sectors'].values())
                grant = package['grant_per_person_cu'] * data['population']['residents'] / 1e6
                transfers = data['income_support'][i] + grant
                transfers += shock.get('extra_income_support', 0) if active else 0
                capital = package['capital'][i]
                primary = services + transfers + capital
                interest = debt * data['interest_rate']
                maturity = data['maturing_principal'][i]
                refinancing = min(maturity, data['assumed_refinancing_capacity'][i])
                opening_cash, opening_debt, opening_arrears = cash, debt, arrears
                need = primary + interest + maturity + arrears - revenue - refinancing
                borrowing = min(max(need, 0), data['max_new_borrowing'][i])
                draw = min(max(need - borrowing, 0), max(cash - data['minimum_cash_buffer'], 0))
                arrears = max(need - borrowing - draw, 0)
                cash += max(-need, 0) - draw
                # Financing arrears are separate from funded debt; they remain liabilities.
                debt += refinancing + borrowing - maturity
                staff = {}
                for sector_id, sector in data['sectors'].items():
                    allocated = sector['required_staff' if package['expand'] else 'retain_staff'][i]
                    available = sector['available_staff'][i]
                    if active and sector_id == 'care':
                        available *= shock.get('care_capacity_factor', 1)
                    staff[sector_id] = {
                        'required': sector['required_staff'][i], 'allocated': allocated,
                        'available': available,
                        'shortfall_against_need': max(0, sector['required_staff'][i] - min(allocated, available)),
                        'shortfall_against_allocation': max(0, allocated - available)}
                years.append({
                    'year': year, 'revenue': revenue, 'services': services,
                    'transfers': transfers, 'universal_grant_gross': grant,
                    'capital': capital, 'primary_outlays': primary,
                    'opening_cash': opening_cash, 'opening_debt': opening_debt,
                    'opening_arrears': opening_arrears, 'interest': interest,
                    'maturing_principal': maturity, 'refinancing': refinancing,
                    'new_borrowing': borrowing, 'cash_draw': draw,
                    'closing_cash': cash, 'closing_debt': debt, 'closing_arrears': arrears,
                    'cash_financing_gap': arrears, 'staff': staff,
                    'capital_delivery_gap': max(0, capital - data['capital_delivery_capacity'][i]),
                    'energy_supply_gap': max(0, package['energy'][i] - data['public_service_energy_capacity'][i]),
                    'energy_requirement_gap': max(0, data['essential_energy_requirement'][i] - package['energy'][i]),
                    'qualification': 'Conditional ledger only; arrears mean planned obligations are unpaid. Staffing is an upper-bound capacity check, not confirmed delivery.'})
            results.append({'scenario': scenario_id, 'package': package_id, 'years': years})
    return results


if __name__ == '__main__':
    inputs = json.loads(Path(__file__).with_name('inputs.json').read_text())
    print(json.dumps({'status': inputs['status'], 'results': calculate(inputs)}, indent=2))
