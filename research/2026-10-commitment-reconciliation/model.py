"""Pinned historical envelope + explicit compound shocks; not a country forecast."""

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
OLD = RESEARCH / '2026-09-national-settlement'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    assumptions = json.loads((HERE / 'assumptions.json').read_text())
    for filename, expected in assumptions['historical_sha256'].items():
        if digest(OLD / filename) != expected:
            raise ValueError(f'Historical dependency changed: {filename}')
    spec = importlib.util.spec_from_file_location('historical_ledger', OLD / 'model.py')
    ledger = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ledger)
    data = json.loads((OLD / 'inputs.json').read_text())
    original = ledger.calculate(data)
    combined = deepcopy(data)
    combined['scenarios'] = {'compound_shortfall': assumptions['cash_and_care_shock']}
    year_index = combined['years'].index(assumptions['institutional_staff_loss']['year'])
    for sector in assumptions['institutional_staff_loss']['sectors']:
        combined['sectors'][sector]['available_staff'][year_index] *= assumptions['institutional_staff_loss']['factor']
    results = ledger.calculate(combined)
    for result in results:
        for year in result['years']:
            year['current_country_cost'] = None
            year['current_country_feasibility'] = 'Not established; unallocated current obligations and subannual/control paths are unknown'
    return {'status': assumptions['status'], 'units': data['units'],
            'historical_reproduction': original, 'compound_results': results,
            'institutional_condition': assumptions['unquantified_institutional_condition'],
            'current_country_cost': None, 'current_country_feasibility': 'undetermined',
            'scope': 'Annual gross sector test only; no new cost calibration, authority, actual capacity, welfare ranking or observed result'}


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
