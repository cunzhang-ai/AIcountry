"""Bounded frozen-data units/definitions/reconciliations, not welfare or reform certification."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal as Q
import json,hashlib,subprocess,sys
import model
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text());q=lambda v:Q(str(v));checks=[]
def check(name,c):
 if not c:raise AssertionError(name)
 checks.append(name)
base=read(D/'baseline.json');check('1033 exact predecessor artifacts',len(base['sha256'])==1033)
for n,h in base['sha256'].items():check('snapshot:'+n,hashlib.sha256((D/'predecessor-design-133'/n).read_bytes()).hexdigest()==h)
pins=read(D/'source-manifest.json')
for n,h in pins['sha256'].items():check('pin:'+n,hashlib.sha256((R/n).read_bytes()).hexdigest()==h)
old=read(D/'predecessor-design-133/settlement/commitments/inventory.json');now=read(R/'settlement/commitments/inventory.json')
check('37 complete function objects exact',len(now['functions'])==37 and now['functions']==old['functions'])
check('61 original selections exact',len(now['selections'])==61 and now['selections']==old['selections'])
refs={k:v for k,v in old.items() if k.endswith('_reference')};check('73 inherited references exact',len(refs)==73 and all(now[k]==v for k,v in refs.items()))
for n in ['FRAMEWORK.md','DECISION-TEMPLATE.md']:check('common method unchanged:'+n,(R/n).read_bytes()==(D/'predecessor-design-133'/n).read_bytes())
x=model.compute();check('fresh frozen-data reproduction',x==read(D/'results.json'))
check('single reference economy/year',x['country']=='Denmark' and x['reference_year']=='2023')
cfg=read(D/'inputs.json');check('all six original selections',set(cfg['table_vintages'])=={'NAN1','NASL1','NASL2','NAN3','NASFK','OFF3'})
check('different companion vintages retained',len(set(x['source_vintages'].values()))==3 and x['source_vintages']['NASFK']=='2026-09-30T08:00:00')
for n in cfg['table_vintages']:
 t=model.Table(n);check('original query year:'+n,next(v['values'] for v in t.query['variables'] if v['code']=='Tid')==['2023'])
 check('original monetary source unit:'+n,t.meta['unit']==('-' if n in ['NAN1','NAN3'] else 'm DKK'))
check('archived failure not relabeled success',read(D/'original-sources/retrieval-failures.json')['VNASFK']['attempts'][0]['result'].startswith('HTTP500') and not (D/'original-sources/VNASFK-data.json').exists())
dem=x['demand'];check('original GDP and public final consumption',q(dem['GDP'])==q('2781.3') and q(dem['general_government_consumption'])==q('636.8'))
check('private consumption includes households/NPISH once',q(dem['household_final_consumption'])+q(dem['NPISH_final_consumption'])==q(dem['private_consumption_source_label']))
check('rounded source-use residual preserved not forced',q(dem['rounded_supply_use_residual'])==q('.1') and abs(q(dem['rounded_supply_use_residual']))<=q('.3'))
p=x['production_and_income'];check('public/nongovernment GVA partition',q(p['S13']['GVA'])+q(p['S1W']['GVA'])==q(p['S1']['GVA']))
for s in p:check('output less intermediate equals GVA within million rounding:'+s,abs(q(p[s]['output'])-q(p[s]['intermediate_consumption'])-q(p[s]['GVA']))<=q('.002'))
check('gross public surplus is CFC not free profit',q(p['S13']['gross_operating_surplus_mixed_income'])==q(p['S13']['CFC'])==q('65.866') and q(p['S13']['net_operating_surplus_mixed_income'])==0)
f=x['fiscal_companion'];check('million to billion fiscal conversion',q(f['general_government_total_expenditure'])==q('1321.267') and q(f['general_government_total_revenue_not_tax_only'])==q('1418.780'))
check('fiscal balance not consumption',q(f['revenue_expense_balance_residual'])==0 and q(f['general_government_total_expenditure'])>2*q(dem['general_government_consumption']))
check('consumption versus expenditure ratios',q('22.8')<q(x['shares_of_rounded_GDP_percent']['general_government_consumption'])<23 and q('47.4')<q(x['shares_of_rounded_GDP_percent']['total_general_government_expenditure'])<q('47.6'))
h=x['household_and_NPISH'];check('actual individual consumption not expenditure/cash',q(h['P41'])-q(h['P31'])==q(h['individual_in_kind_addition_not_cash'])==q('443.9'))
check('in-kind income/consumption reconciliation',q(h['B7G'])-q(h['B6G'])==q(h['individual_in_kind_addition_not_cash']))
check('pension adjustment participates in saving not independent cash',q(h['D8K'])==99 and q(h['gross_saving_identity_residual'])==0 and q(h['B6G'])-q(h['P31'])!=q(h['B8G']))
b=x['nonfinancial_net_lending'];check('national and foreign signs',q(b['S1'])==-q(b['S2'])==q('260.963'))
check('both domestic sectors positive without zero foreign balance',q(b['S13'])>0 and q(b['S1W'])>0 and q(b['S2'])<0)
check('published constituent rounding retained',q(b['S13'])+q(b['S1W'])-q(b['S1'])==q('-.001'))
for s,v in x['financial_by_sector'].items():check('financial stock/trans/revaluation/volume reconciliation:'+s,abs(q(v['stock_flow_residual']))<=q('.003'))
combined=x['financial_HH_plus_NPISH'];check('aligned financial household/NPISH scope',all(q(combined[k])==q(x['financial_by_sector']['S14'][k])+q(x['financial_by_sector']['S15'][k]) for k in combined))
check('wealth increase is not net lending alone',q(combined['closing_NFA'])-q(combined['opening_NFA'])>5*q(combined['net_transactions']) and q(combined['net_revaluation'])>4*q(combined['net_transactions']))
check('combined rounding remains visible',q(combined['stock_flow_residual'])==q('.001'))
check('matching published nonfinancial/financial totals without vintage merger',all(q(v)==0 for v in x['financial_nonfinancial_net_lending_differences'].values()))
missing=x['preserved_missing_example'];check('published missing pension cell preserved',missing['value'] is None and missing['status']=='..')
t=model.Table('NASL2')
for name,call in [('missing is not zero',lambda:t.val(TRANSAKT='D8K',SEKTOR='S13')),('ambiguous sector not defaulted',lambda:t.val(TRANSAKT='B9D')),('future meaning not silently ignored',lambda:t.val(TRANSAKT='B9D',SEKTOR='S13',future_mandate='unmapped'))]:
 try:call()
 except ValueError:check('decoder rejects:'+name,True)
 else:raise AssertionError(name)
for name,mutate in [('unknown context',lambda c:c.update(future_collective_scope='unmapped')),('mixed year',lambda c:c.update(reference_year='2024')),('false archive alignment',lambda c:c['table_vintages'].update(NASFK='2026-06-30T08:00:00')),('invented readiness',lambda c:c.update(actual_country_cost_source_or_readiness='ready'))]:
 bad=deepcopy(cfg);mutate(bad)
 try:model.compute(bad)
 except ValueError:check('changed semantics rejected:'+name,True)
 else:raise AssertionError(name)
check('whole alternatives and actual reform-cost unknown',len(x['country_proposals'])==4 and x['actual_A_or_U_incremental_DKK_cost_tax_yield_or_better_lives'] is None)
proc=subprocess.run([sys.executable,str(R.parent/'scripts/check-research-structure.py')],capture_output=True,text=True);check('organization and current links',proc.returncode==0)
report={'edition':134,'status':'pass','substantive_checks':sum(not n.startswith(('snapshot:','pin:')) for n in checks),'predecessor_artifacts':1033,'source_pins':len(pins['sha256']),'structure':proc.stdout.strip(),'scope':'Exact preservation and frozen original statistical decoding, unit/vintage/sector/missing semantics, observed account/stock-flow/rounding identities and adverse inputs. Not complete raw-record audit, matched reform microsimulation, new-country source, service quality, legitimate mandate, independent affected review or better lives.'}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
