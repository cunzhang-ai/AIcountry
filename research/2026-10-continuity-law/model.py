"""Authored inclusion, displacement, clock and controller tests; no forecast."""

from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def calculate():
    data = json.loads((HERE / 'inputs.json').read_text())
    for source, expected in data['pinned_sources'].items():
        if hashlib.sha256((ROOT / source).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Dependency changed: {source}')
    spec = importlib.util.spec_from_file_location('compound', ROOT / '2026-10-commitment-reconciliation/model.py')
    compound = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compound)
    base = compound.calculate()
    old = json.loads((ROOT / '2026-09-national-settlement/inputs.json').read_text())
    services = next(x for x in base['compound_results'] if x['package'] == 'S_services')['years'][1]
    allocation = []
    for sector, core in data['reference_core_fte'].items():
        staff = services['staff'][sector]
        required = Fraction(str(staff['required']))
        available = Fraction(str(staff['available']))
        cost = Fraction(str(old['sectors'][sector]['expand_cost'][1]))
        core = Fraction(str(core))
        assert 0 <= core <= required
        # Declared scenario attribution of the whole operating envelope, not wage/unit-cost evidence.
        core_cost = cost * core / required
        allocated_core=min(core,available)
        remaining_capacity = max(Fraction(0), available - allocated_core)
        allocation.append({'sector': sector, 'required_fte': float(required),
          'available_fte': float(available), 'assumed_protected_core_fte': float(core),
          'allocated_core_fte':float(allocated_core),'core_shortfall_fte':float(core-allocated_core),
          'remaining_required_fte': float(required-core),
          'remaining_available_fte': float(remaining_capacity),
          'remaining_shortfall_fte': float(max(Fraction(0), required-core-remaining_capacity)),
          'reference_total_cost': float(cost), 'assumed_core_cost': float(core_cost),
          'remaining_reference_cost': float(cost-core_cost),
          'cost_identity_exact': str(core_cost + cost-core_cost),
          'status':'Authored included allocation; no qualified/independent shifts or adequate service established'})
    rosters = []
    for role, rule in data['six_hour_sample'].items():
        available = rule['staff'] * rule['productive_hours_each']
        demand = rule['required_hours']
        rosters.append({'role': role, 'per_block_available_hours': available,
          'per_block_required_hours': demand, 'per_block_shortfall_hours':max(0,demand-available),
          'four_block_shortfall_hours':4*max(0,demand-available),
          'status':'Four authored consecutive blocks; replacement staff differ by block; no full-country roster'})
    clocks = []
    for event in data['clock_cases']:
        limit = min(event['statutory_outer_hours'],event['latest_useful_hours'])
        clocks.append({**event, 'effective_latest_hours': limit,
          'outer_clock_met': event['completed_hours']<=event['statutory_outer_hours'],
          'protection_time_met':event['completed_hours']<=limit,
          'claim_survives_failure': True})
    orders=[]
    for order in data['interim_orders']:
        extensions=min(order['extensions_requested'],1) if order['fresh_necessity_finding'] else 0
        expiry=min(72+72*extensions,order['shorter_source_limit_hours'])
        opportunity=order['meaningful_hearing_opportunity_hours']
        heard=opportunity is not None and opportunity<=expiry
        heard_by_test=heard and opportunity<=order['test_hour']
        orders.append({**order,'maximum_ex_parte_hours':expiry,
          'hearing_opportunity_timely':heard,
          'hearing_opportunity_occurred_by_test':heard_by_test,
          'ex_parte_power_available_at_test':order['test_hour']<expiry and not heard_by_test,
          'underlying_claim_cancelled':False,
          'qualification':'Time-bound scope test; no force or new adjudicator authorized'})
    controllers = []
    for name, paths in data['controller_packages'].items():
        for function, path in paths.items():
            functioning = [p for p in path if not set(p) & set(data['failed_nodes'])]
            controllers.append({'package':name,'function':function,'paths':path,
              'path_available_in_sample':bool(functioning),
              'actual_delivery':None,
              'qualification':'Path test only; not proof of legal power, independent controllers, due cash or staffed execution'})
    return {'status':data['status'],'allocation':allocation,
      'year2_six_envelope_cost':services['services'],
      'year2_transfer_envelope':services['transfers'],
      'unclosed_year2_cash_gap':services['cash_financing_gap'],
      'sample_roster':rosters,'clock_cases':clocks,'interim_orders':orders,'controller_paths':controllers,
      'actual_national_cost':None,'full_country_feasibility':'undetermined',
      'conditions':data['conditions'],
      'interpretation':'Protected core allocation moves unmet work; separate paths do not create cash, qualified labor or authority. Earlier protection time prevails over administrative outer clocks.'}


if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))
