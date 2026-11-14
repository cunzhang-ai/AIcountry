"""Finite preserved-scope, coverage and clock checks; not legal/operational certification."""
from pathlib import Path
from decimal import Decimal as Q
from copy import deepcopy
import json,hashlib,subprocess,sys
import model
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text());q=lambda x:Q(str(x));checks=[]
def check(name,c):
 if not c:raise AssertionError(name)
 checks.append(name)
baseline=read(D/'baseline.json')
check('1015 predecessor artifacts',len(baseline['sha256'])==1015)
for n,h in baseline['sha256'].items():check('snapshot:'+n,hashlib.sha256((D/'predecessor-design-131'/n).read_bytes()).hexdigest()==h)
pins=read(D/'source-manifest.json')
for n,h in pins['sha256'].items():check('pin:'+n,hashlib.sha256((R/n).read_bytes()).hexdigest()==h)
old=read(D/'predecessor-design-131/settlement/commitments/inventory.json');now=read(R/'settlement/commitments/inventory.json')
check('37 complete original function objects',now['functions']==old['functions'] and len(now['functions'])==37)
check('61 original selections',now['selections']==old['selections'] and len(now['selections'])==61)
refs={k:v for k,v in old.items() if k.endswith('_reference')}
check('71 inherited references',len(refs)==71 and all(now[k]==v for k,v in refs.items()))
for n in ['FRAMEWORK.md','DECISION-TEMPLATE.md']:check('common method unchanged:'+n,(R/n).read_bytes()==(D/'predecessor-design-131'/n).read_bytes())
x=model.compute();check('fresh result equality',x==read(D/'results.json'))
rows=x['public_purchase_scope']['rows'];prior=read(R/'2026-11-current-country-operating-and-source-reference/cases/firm_plural_I05.json')
expected=[r for r in prior['public_book']['component_rows'] if r['kind']=='purchase']
check('all66 current purchase identities once',len(rows)==66 and len({r['id'] for r in rows})==66 and {r['id'] for r in rows}=={r['id'] for r in expected})
check('amounts and original function owners unchanged',all((r['function_owner'],r['named_allocation_CU'])==(p['owner'],p['named_allocation_CU']) for r,p in zip(rows,expected)))
check('named purchase subset conserved',sum(q(r['named_allocation_CU']) for r in rows)==q(x['public_purchase_scope']['named_total_CU']))
check('partial-linked and unprovided partitions reconcile',abs(q(x['public_purchase_scope']['linked_partial_scope_CU'])+q(x['public_purchase_scope']['remaining_budget_or_task_scope_CU'])-q(x['public_purchase_scope']['named_total_CU']))<q('.00000001'))
check('only four partial linked rows',sum(r['linked_scope'] is not None for r in rows)==4)
check('six clinical budget rows retained',q(x['public_purchase_scope']['six_clinical_budget_rows_CU'])==43520000)
check('no actual suppliers invented',all(r['actual_output_quantity_recipe_acceptance_or_paid_source'] is None for r in rows))
private=x['private_nonfood_reference'];pb=read(R/'2026-11-ordinary-life-and-household-production/inputs.json')
check('all13 nonfood rows and meanings retained',len(private)==13 and {r['id'] for r in private}=={r['id'] for r in pb['basket'] if r['purpose']!='01'})
check('unassigned envelope not output',len([r for r in private if r['coverage']=='not_output_or_tax_base'])==1)
check('garment remains partial external scope',next(r for r in private if r['id']=='garments')['coverage']=='131_partial_garment_offer_not_in_national_book')
check('no actual nonfood buyer/output invented',all(r['actual_need_buyer_recipe_order_receipt_or_source'] is None for r in private))
cfg=read(D/'inputs.json');cases={r['id']:r for r in x['proposed_clock_cases']}
split=cases['split_related_need'];check('split related purchase exceeds threshold',split['material'] and q(split['aggregated_gross_commitment_CU'])==160000)
check('30 full calendar days',split['earliest_bid_date_without_material_revision']=='2030-02-06')
check('notice day excluded and10 full working days',split['standstill_ends_at_close_of_day']=='2030-02-25' and split['ordinary_contract_not_before']=='2030-02-26')
check('declared holiday extends full standstill',cases['holiday_and_challenger_access']['ordinary_contract_not_before']=='2030-02-27')
check('micro does not fabricate a full tender',cases['small_purchase']['micro'] and cases['small_purchase']['earliest_bid_date_without_material_revision']=='2030-01-07')
check('intermediate quotation has5 working days',cases['ordinary_quotation']['earliest_bid_date_without_material_revision']=='2030-01-14' and not cases['ordinary_quotation']['material'])
challenged=cases['challenged_medicine_award'];check('continuity does not override main award hold',challenged['ordinary_contract_not_before'] is None and challenged['continuity_contract_is_separate_limited_source_authority_not_main_award'])
for label,mutate in [('unfamiliar concept',lambda c:c.update(future_collective_semantics={'unmapped':True})),('invented exception',lambda c:c.update(urgency='AI_approved')),('early material award',lambda c:c.update(usable_award_notice='2030-01-08')),('negative source commitment',lambda c:c.update(related_expected_gross_commitments=['-1']))]:
 bad=deepcopy(cfg['procurement_cases'][0]);mutate(bad)
 try:model.procurement_case(bad)
 except ValueError:check('reject unsupported input:'+label,True)
 else:raise AssertionError(label)
check('no actual country qualification',x['actual_national_source_capacity_authority_or_better_lives'] is None)
proc=subprocess.run([sys.executable,str(R.parent/'scripts/check-research-structure.py')],text=True,capture_output=True)
check('organization and current links',proc.returncode==0)
report={'edition':132,'status':'pass','substantive_checks':sum(not n.startswith(('snapshot:','pin:')) for n in checks),'predecessor_artifacts':1015,'source_pins':len(pins['sha256']),'structure':proc.stdout.strip(),'scope':'Exact preservation and all-row purchase/nonfood coverage, partition/owner/unknown identities and authored clock/adverse-input examples. Legal scenarios are qualified reasoning, not executable adjudication. No actual source, cost, mandate, independent/affected review, safe supply or outcome proof.'}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
