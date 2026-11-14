"""Conditional person-resource stress with explicit producer/utility/housing counterparties; actual other resources remain unknown."""
from decimal import Decimal as Q,ROUND_CEILING
q=lambda n:Q(str(n))
ceil=lambda n:int(n.to_integral_value(rounding=ROUND_CEILING))
def tax(base,cfg,package):
 M=q(cfg['M']);A=q('.4')*M if package=='A' or base<=M else max(Q(0),q('.4')*(2*M-base))
 left=max(Q(0),base-A);t=Q(0)
 for width,rate in zip(cfg['band_widths_M'],cfg['tax_rates']):
  z=left if width is None else min(left,q(width)*M);t+=z*q(rate);left-=z
 return t

def housing(cfg,pb):
 out={'working':[],'older':[]};b=pb['home_bills'];totals={};sites=cfg['local_sites'];ownhomes=q(pb['opening_structures']['occupied_owner'])/len(sites)
 for site in sites:
  primary=q(site['taxable_site_base'])*q(site['primary_fraction'])*q(cfg['local_rate'])-q(site['deferral'])-q(site['stay'])
  if primary<0:raise ValueError('Held primary levy exceeds base')
  totals[site['id']]=str(primary)
  for h in pb['household_types']:
   adults=h['working_age_adults_each']+h['older_adults_each'];persons=adults+len(h['child_ages_each']);kind='older' if h['older_adults_each'] else 'working'
   utility=(q(b['power_base_kWh_home'])+q(b['power_kWh_person'])*persons)*q(b['power_quote_CU_kWh'])*(1+q(b['power_VAT']))+(q(b['water_base_m3_home'])+q(b['water_m3_person'])*persons)*q(b['water_quote_CU_m3'])+q(b['home_broadband_annual_CU'])
   for tenure,frac in cfg['housing_tenure_fraction'].items():
    rent=q(b['private_rent_each'] if tenure=='private_rent' else b['public_rent_each'] if tenure=='public_rent' else b['owner_repair_each'])
    if tenure=='owner':rent+=q(b['insurance_each'])+primary/ownhomes
    homes=q(h['households'])*q(frac)/len(sites);out[kind].append({'type':h['id'],'local':site['id'],'tenure':tenure,'adult_count':homes*adults,'home_count':homes,'N_housing_each':(rent+utility)/adults,'annual_site_each':primary/ownhomes/adults if tenure=='owner' else Q(0)})
 return out,totals

def compute(cfg,case,services,pb,pbr,extra_groups):
 book=services['service_cases'][case['service']];cal=services['private_learning_and_reprice'][case['helper']];groups=[];paid=q(case['private_wage_received_fraction']);local=set(cfg['local_teacher_component_ids'])
 for r in book['component_rows']:
  if r['kind']!='staff':continue
  n=ceil(max(q(r['posts']),q(r['people_min'] or 0)));gross=q(r['annual_base_CU']);pub=q(r['direct_public_salary_CU'])/gross if gross else Q(0)
  groups.append({'id':r['id'],'count':n,'gross_each':gross/n,'public_fraction':pub,'salary_payer':'local' if r['id'] in local else 'G','civic_each':Q(0)})
 helper=pbr['home_help'][case['helper']];n=helper['people'];groups.append({'id':'private:help','count':n,'gross_each':q(helper['salary_CU'])/n,'public_fraction':Q(0),'salary_payer':'private','civic_each':Q(0)})
 retail=sum(g['retail_posts'] for g in pbr['goods_base']);groups.append({'id':'private:retail','count':retail,'gross_each':q(30000),'public_fraction':Q(0),'salary_payer':'private','civic_each':Q(0)})
 groups.append({'id':'private:learning','count':cal['additional_learning_instructors'],'gross_each':q(60000),'public_fraction':Q(0),'salary_payer':'private','civic_each':Q(0)})
 civic=sum((q(r['annual_base_CU']) for r in book['component_rows'] if r['id'].startswith('civic:')),Q(0))+q(next(r['annual_base_CU'] for r in book['component_rows'] if r['id']=='fee:OJ_ordinary_selection_release'))
 groups.append({'id':'civic:paid_release','count':cfg['civic_recipient_people'],'gross_each':Q(0),'public_fraction':Q(0),'salary_payer':'G','civic_each':civic/cfg['civic_recipient_people']})
 groups.append({'id':'qualified:care_credit','count':cfg['care_credit_people'],'gross_each':Q(0),'public_fraction':Q(0),'salary_payer':'G','civic_each':Q(0)})
 groups.extend(extra_groups)
 remainder=cfg['working_people']-sum(g['count'] for g in groups)
 if remainder<0:raise ValueError('Named distinct person demand exceeds available adults')
 groups.append({'id':'other:unsupplied_resource_stress','count':remainder,'gross_each':Q(0),'public_fraction':Q(0),'salary_payer':'G','civic_each':Q(0)})
 homes,primary=housing(cfg,pb);B={'adult':max(q(pb['old_reference_adult_B']),q(pbr['ordinary']['per_person_component_quotes_CU']['adult']))}
 for age in cfg['children']:B[age]=max(q(pb['old_reference_adult_B'])*q(pb['old_child_factor']),q(pbr['ordinary']['per_person_component_quotes_CU'][age]))
 P=cfg['pension'];earned=q(P['years'])*q(P['accrual'])*q(P['higher_prior_base'] if case['higher_prior_units'] else P['past_revalued_base']);prior=earned
 if case['net_makewhole_hypothesis']:
  lo=earned;hi=earned*3
  for _ in range(100):
   mid=(lo+hi)/2
   if mid-tax(mid,cfg,case['package'])>=prior:hi=mid
   else:lo=mid
  earned=q(ceil(hi*100))/100
 allgroups=[{**g,'kind':'working','age':'adult','basic':Q(0),'insurance':Q(0)} for g in groups]
 allgroups.append({'id':'older:past_units','kind':'older','age':'adult','count':cfg['older_people'],'gross_each':Q(0),'civic_each':Q(0),'public_fraction':Q(0),'salary_payer':'S','basic':B['adult'],'insurance':earned})
 for age,n in cfg['children'].items():
  pots=P['survivor_pots'] if age==P['survivor_age'] else 0
  for label,count,pension in [('ordinary',n-pots,0),('survivor',pots,P['survivor_annual_each'])]:
   if count:allgroups.append({'id':'child:'+age+':'+label,'kind':'child','age':age,'count':count,'gross_each':Q(0),'civic_each':Q(0),'public_fraction':Q(0),'salary_payer':'S','basic':Q(0),'insurance':q(pension)})
 totals={k:Q(0) for k in ['I05','nonolder_U','Y_basic','insurance_gross','PA_assessed','Y_withheld','worked_gross_due','worked_gross_received','unpaid_wages','civic_received','recognized_housing','Y_new_annual_units','cash_after_named_housing']};payer={k:{'PA':Q(0),'Y':Q(0)} for k in ['G','local','private','S','food','water','power','housing']};rows=[];monthly=[{k:Q(0) for k in ['I05','nonolder_U','Y_basic','recognized_housing']} for _ in range(12)]
 for g in allgroups:
  count=q(g['count']);wage=g['gross_each']*(g['public_fraction']+(1-g['public_fraction'])*paid);y=wage*q(cfg['Y_rate']);labor=wage-y+g['civic_each'];base=labor+g['insurance'];t=tax(base,cfg,case['package']);netlabor=labor-(t*labor/base if base else 0);netpension=g['insurance']-(t*g['insurance']/base if base else 0);O=g['basic']+netpension-min(q(cfg['pension_disregard'])*netpension,q(cfg['disregard_B'])*B[g['age']]);U=B[g['age']] if case['package']=='C1' and g['kind']!='older' else Q(0)
  profiles=homes[g['kind']] if g['kind']!='child' else [{'adult_count':Q(1),'N_housing_each':Q(0),'annual_site_each':Q(0)}];den=sum(p['adult_count'] for p in profiles);benefit=after=hcost=Q(0)
  for month in range(1,13):
   monthlybenefit=monthlyhousing=Q(0)
   for h in profiles:
    weight=h['adult_count']/den;monthhousing=(h['N_housing_each']-h['annual_site_each'])/12+(h['annual_site_each']/4 if month in [1,4,7,10] else Q(0));N=max(B[g['age']]-q(cfg['ordinary_Q']),q('.2')*B[g['age']])/12+monthhousing
    award=max(Q(0),N-O/12-q(cfg['asset_draw_in_named_resource_stress'])/12-q(cfg['withdrawal'])*max(Q(0),netlabor/12-q(cfg['disregard_B'])*B[g['age']]/12)-U/12)
    monthlybenefit+=weight*award;monthlyhousing+=weight*monthhousing
   benefit+=monthlybenefit;hcost+=monthlyhousing
   for key,value in [('I05',monthlybenefit),('nonolder_U',U/12),('Y_basic',g['basic']/12),('recognized_housing',monthlyhousing)]:monthly[month-1][key]+=value*count
  after=netlabor+netpension+g['basic']+U+benefit-hcost
  vals={'I05':benefit,'nonolder_U':U,'Y_basic':g['basic'],'insurance_gross':g['insurance'],'PA_assessed':t,'Y_withheld':y,'worked_gross_due':g['gross_each'],'worked_gross_received':wage,'unpaid_wages':g['gross_each']-wage,'civic_received':g['civic_each'],'recognized_housing':hcost,'Y_new_annual_units':q(P['accrual'])*min(g['gross_each'],q(cfg['W'])),'cash_after_named_housing':after}
  for k,v in vals.items():totals[k]+=v*count
  # One tax assessment, attributed to actual mixed sources, never one allowance per payer.
  public_work=g['gross_each']*g['public_fraction'];private_work=g['gross_each']*(1-g['public_fraction'])*paid
  contributions=[(g['salary_payer'],public_work)]+[(owner,private_work*weight) for owner,weight in g.get('private_payer_weights',{'private':Q(1)}).items()]
  for owner,value in contributions:
   if value:
    payer[owner]['Y']+=value*q(cfg['Y_rate'])*count;payer[owner]['PA']+=(t*(value*(1-q(cfg['Y_rate'])))/base if base else 0)*count
  payer['G']['PA']+=(t*g['civic_each']/base if base else 0)*count;payer['S']['PA']+=(t*g['insurance']/base if base else 0)*count
  rows.append({'id':g['id'],'kind':g['kind'],'count':g['count'],'private_source_weights':{k:str(v) for k,v in g.get('private_payer_weights',{'private':Q(1)}).items()},'gross_wage_due_each':str(g['gross_each']),'gross_wage_received_each':str(wage),'civic_received_each':str(g['civic_each']),'insurance_each':str(g['insurance']),'tax_each':str(t),'I05_each_averaged_over_authored_home_profiles':str(benefit),'U_each':str(U),'actual_other_resources_or_eligibility':None})
 totals['Y_new_annual_units']+=q(cfg['care_credit_people'])*q('.5')*q(cfg['W'])*q(P['accrual'])
 return {'monthly_totals':[{k:str(v) for k,v in row.items()} for row in monthly],'people':rows,'population':sum(g['count'] for g in allgroups),'distinct_service_worker_demand':sum(ceil(max(q(r['posts']),q(r['people_min'] or 0))) for r in book['component_rows'] if r['kind']=='staff'),'unsupplied_resource_stress_people':remainder,'B':{k:str(v) for k,v in B.items()},'totals':{k:str(v) for k,v in totals.items()},'payer_withheld':{k:{a:str(b) for a,b in v.items()} for k,v in payer.items()},'primary_home_cash_site_levy':primary,'care_credit_G_to_S':str(q(cfg['care_credit_people'])*q('.5')*q(cfg['W'])*q(cfg['Y_rate'])),'prior_earned_each':str(prior),'annual_new_insurance_makewhole':str((earned-prior)*cfg['older_people']),'unpriced_actual_other_income_or_fee_mapping_or_old_rights':None}
