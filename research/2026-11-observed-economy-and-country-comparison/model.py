"""Pinned observed2023 economy, with explicit units, sectors, vintages and missing cells."""
from pathlib import Path
from decimal import Decimal as Q
import json
D=Path(__file__).resolve().parent;S=D/'original-sources'
q=lambda x:Q(str(x));read=lambda p:json.loads(p.read_text())
def clean(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,list):return [clean(v) for v in x]
 return x

class Table:
 def __init__(self,name,year='2023'):
  self.name=name;self.meta=read(S/(name+'-metadata.json'));self.query=read(S/(name+'-query.json'));self.data=read(S/(name+'-data.json'))['dataset'];self.year=year
  if self.query['table']!=name or self.query['lang']!='en' or self.query['format']!='JSONSTAT':raise ValueError('Uninterpreted source format/language')
  if next(v for v in self.query['variables'] if v['code']=='Tid')['values']!=[year]:raise ValueError('Mixed reference years need a new comparison')
  dim=self.data['dimension']
  expected={'TRANSAKT','PRISENHED','ContentsCode','Tid'} if name in ['NAN1','NAN3'] else {'SEKTORNAT','KONTO1','BALANCE','FININS','MODSEKNAT','ContentsCode','Tid'} if name=='NASFK' else {'UI','SEKTOR','ContentsCode','Tid'} if name=='OFF3' else {'TRANSAKT','SEKTOR','ContentsCode','Tid'}
  if set(dim['id'])!=expected:raise ValueError('New source dimension needs semantic review')
  if name in ['NAN1','NAN3'] and dim['PRISENHED']['category']['label']!={'V_M':'Current prices, (bill. DKK.)'}:raise ValueError('Uninterpreted price/unit meaning')
  if set(dim['ContentsCode']['category']['index'])!={name}:raise ValueError('Wrong source content')
 def cell(self,**selectors):
  dim=self.data['dimension'];idx=0;used=set()
  for name,size in zip(dim['id'],dim['size']):
   choices=dim[name]['category']['index']
   if name in selectors:
    key=selectors[name];used.add(name)
    if key not in choices:raise ValueError('Unknown source category: '+name)
    coordinate=choices[key]
   elif size==1:coordinate=0
   else:raise ValueError('Ambiguous source dimension: '+name)
   idx=idx*size+coordinate
  if used!=set(selectors):raise ValueError('Uninterpreted selector preserved for review')
  values=self.data['value'];value=values[idx] if isinstance(values,list) else values.get(str(idx))
  status=self.data.get('status',{}).get(str(idx))
  return {'value':None if value is None else q(value),'status':status,'table':self.name,'selectors':selectors,'year':self.year}
 def val(self,**selectors):
  c=self.cell(**selectors)
  if c['value'] is None:raise ValueError('Missing source value is not zero: '+str(c))
  return c['value']

def compute(cfg=None):
 cfg=read(D/'inputs.json') if cfg is None else cfg
 if set(cfg)!={'edition','country','reference_year','table_vintages','scope','actual_country_cost_source_or_readiness'} or cfg['edition']!=134 or cfg['reference_year']!='2023' or cfg['country']!='Denmark':raise ValueError('Uninterpreted comparator context')
 if cfg['actual_country_cost_source_or_readiness'] is not None:raise ValueError('A comparator cannot certify country readiness')
 t={n:Table(n) for n in cfg['table_vintages']}
 for n,vintage in cfg['table_vintages'].items():
  if t[n].meta['updated']!=vintage:raise ValueError('Changed vintage needs fresh scope interpretation')
  expected='-' if n in ['NAN1','NAN3'] else 'm DKK'
  if t[n].meta['unit']!=expected:raise ValueError('Changed declared source unit')
 a=lambda code:t['NAN1'].val(TRANSAKT=code,PRISENHED='V_M')
 sec=lambda code,s:t['NASL2'].val(TRANSAKT=code,SEKTOR=s)/1000
 prod=lambda code,s:t['NASL1'].val(TRANSAKT=code,SEKTOR=s)/1000
 h=lambda code:t['NAN3'].val(TRANSAKT=code,PRISENHED='V_M')
 off=lambda code:t['OFF3'].val(UI=code,SEKTOR='TOTAL')/1000
 gdp=a('B1GQK');demand={k:a(code) for k,code in {'GDP':'B1GQK','imports':'P7K','exports':'P6D','household_final_consumption':'P31S14D','NPISH_final_consumption':'P31S15D','private_consumption_source_label':'P31S1MD','general_government_consumption':'P3S13D','gross_capital_formation':'P5GD'}.items()}
 demand['rounded_supply_use_residual']=gdp+demand['imports']-demand['private_consumption_source_label']-demand['general_government_consumption']-demand['gross_capital_formation']-demand['exports']
 balances={s:sec('B9D',s) for s in ['S1','S13','S1W','S2']}
 production={s:{k:prod(code,s) for k,code in {'output':'P1K','intermediate_consumption':'P2D','GVA':'B1GD','compensation':'D1D','gross_operating_surplus_mixed_income':'B2A3GD','CFC':'P51CD','net_operating_surplus_mixed_income':'B2A3ND'}.items()} for s in ['S1','S13','S1W']}
 household={code:h(code) for code in ['P31','P41','B6G','B7G','D8K','B8G','P51C']}
 household['individual_in_kind_addition_not_cash']=h('P41')-h('P31')
 household['adjusted_income_addition_not_cash']=h('B7G')-h('B6G')
 household['gross_saving_identity_residual']=h('B6G')+h('D8K')-h('P31')-h('B8G')
 financial={}
 for s in ['S1','S11','S12','S13','S14','S15','S2']:
  out={}
  for code,label in [('P','opening_NFA'),('U','closing_NFA'),('T','net_transactions'),('O','net_revaluation'),('A','net_other_volume_change')]:
   out[label]=(t['NASFK'].val(SEKTORNAT=s,KONTO1=code,BALANCE='AS',FININS='F',MODSEKNAT='SALLE')-t['NASFK'].val(SEKTORNAT=s,KONTO1=code,BALANCE='LI',FININS='F',MODSEKNAT='SALLE'))/1000
  out['stock_flow_residual']=out['closing_NFA']-out['opening_NFA']-out['net_transactions']-out['net_revaluation']-out['net_other_volume_change'];financial[s]=out
 combined={k:financial['S14'][k]+financial['S15'][k] for k in financial['S14']}
 finance_nonfin={s:financial[s]['net_transactions']-balances[s] for s in ['S1','S13','S2']}
 fiscal={'general_government_total_expenditure':off('1.17'),'general_government_total_revenue_not_tax_only':off('2.17'),'general_government_net_lending':off('2.19')}
 fiscal['revenue_expense_balance_residual']=fiscal['general_government_total_revenue_not_tax_only']-fiscal['general_government_total_expenditure']-fiscal['general_government_net_lending']
 return clean({'edition':134,'format_revision':'134-observed-economy-boundaries-v1','country':'Denmark','reference_year':'2023','output_unit':'billion DKK, current prices/nominal positions; no country CU/FU conversion',
  'source_vintages':cfg['table_vintages'],'demand':demand,'production_and_income':production,'nonfinancial_net_lending':balances,'fiscal_companion':fiscal,
  'household_and_NPISH':household,'financial_by_sector':financial,'financial_HH_plus_NPISH':combined,
  'financial_nonfinancial_net_lending_differences':finance_nonfin,
  'shares_of_rounded_GDP_percent':{k:v/gdp*100 for k,v in {**{z:demand[z] for z in ['general_government_consumption','gross_capital_formation','exports','imports']},'total_general_government_expenditure':fiscal['general_government_total_expenditure']}.items()},
  'preserved_missing_example':t['NASL2'].cell(TRANSAKT='D8K',SEKTOR='S13'),
  'country_proposals':{'retain_observed_mix':'Observed accounting baseline only, not endorsement of all institutions or outcomes.','A_I05_plus_protected_services':'Current-country additions/deletions/legacy and distribution unqualified; actual matched incremental cost/source unknown.','conditional_U_C2_same_services':'Gross U, displaced same-person cash, tax, pension, extra needs, price/work/care/provider and paid transition require matching; actual incremental cost/source unknown.','paid_direct_public_provider_rival':'Actual title/acquisition/workforce/management/overlap/renewal/user control and source remain; no free nationalization.'},
  'actual_A_or_U_incremental_DKK_cost_tax_yield_or_better_lives':None})

if __name__=='__main__':(D/'results.json').write_text(json.dumps(compute(),indent=2)+'\n')
