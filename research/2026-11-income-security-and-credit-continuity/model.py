"""Authored first-service-year credit interfaces, not household welfare or solvency."""
from decimal import Decimal as D
from pathlib import Path
import json
HERE = Path(__file__).resolve().parent
FIELDS = {'id','ordinary_mode','ordinary_cash_received','eligible_fraction',
          'qualified','covered_eligible','covered_other','labor_cash_received',
          'actual_G_to_S_received','prior_annual_units'}
def dec(x):
    if isinstance(x, bool) or x is None: raise ValueError('explicit number required')
    q = D(str(x))
    if not q.is_finite() or q < 0: raise ValueError('finite nonnegative number required')
    return q

def compute_case(row, W='30000'):
    if set(row) != FIELDS: raise ValueError('unknown or missing semantics')
    if row['ordinary_mode'] not in ('A/I05','conditional U+C2'): raise ValueError('unmapped cash architecture')
    if type(row['qualified']) not in (bool,type(None)): raise ValueError('qualification must be explicit or unknown')
    if not isinstance(row['id'],str) or not row['id']: raise ValueError('case identity required')
    w=dec(W)
    if not w: raise ValueError('positive source-year W required')
    f=dec(row['eligible_fraction'])
    if f>1: raise ValueError('eligible time exceeds one year')
    a,b,c=map(dec,[row['covered_eligible'],row['covered_other'],row['labor_cash_received']])
    ordinary=dec(row['ordinary_cash_received']);old=dec(row['prior_annual_units'])
    if f==1 and b: raise ValueError('work outside a full-year eligible period')
    if row['qualified'] is False and f: raise ValueError('unqualified time cannot accrue credit')
    if f==0 and a: raise ValueError('no covered earnings assigned to an absent eligible period')
    received=row['actual_G_to_S_received']
    if received is not None: received=dec(received)
    target=None if row['qualified'] is None else D('.5')*w*f
    extra=None if target is None else min(max(D(0),target-a),max(D(0),w-a-b))
    base=None if extra is None else min(w,a+b+extra)
    new=None if base is None else D('.0125')*base
    required=None if extra is None else D('.10')*extra
    serialize=lambda q: None if q is None else format(q,'f')
    return {'id':row['id'],'ordinary_mode':row['ordinary_mode'],
        'ordinary_cash_received':serialize(ordinary),'covered_work_base':serialize(min(w,a+b)),
        'known_work_annual_unit_floor':serialize(D('.0125')*min(w,a+b)),
        'credit_target':serialize(target),'additional_credit_base':serialize(extra),
        'required_G_to_S':serialize(required),'actual_G_to_S_received':serialize(received),
        'labor_levy_on_received_cash_only_in_this_cash_only_fixture':serialize(D('.10')*c),
        'new_first_year_annual_unit':serialize(new),'prior_annual_units_unchanged':serialize(old),
        'combined_annual_units_not_current_cash':serialize(None if new is None else old+new),
        'actual_funded_lifetime_liability':None,'actual_country_net_cost_or_source':None}

def compute(config=None):
    if config is None: config=json.loads((HERE/'inputs.json').read_text())
    if set(config)!={'edition','source_year_W','context','cases'} or config['edition']!=135 or config['context']!='authored CU first-service-year; no foreign calibration':
        raise ValueError('unmapped context')
    ids=[r['id'] for r in config['cases']]
    if len(ids)!=len(set(ids)): raise ValueError('duplicate case/person-period identity')
    return {'edition':135,'context':config['context'],'cases':[compute_case(r,config['source_year_W']) for r in config['cases']],
        'actual_matched_household_services_retirement_comparison':None,
        'actual_legitimate_authority_or_affected_review':None}
if __name__=='__main__':
    (HERE/'results.json').write_text(json.dumps(compute(),indent=2)+'\n')
