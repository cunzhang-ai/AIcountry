"""Reprice compatible items/meters while retaining old larger nominal rights and unqualified needs."""
from copy import deepcopy
from decimal import Decimal as Q
import importlib.util
from pathlib import Path
R=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('_PB124_scope',R/'2026-11-ordinary-life-and-household-production/model.py');PB=importlib.util.module_from_spec(spec);spec.loader.exec_module(PB)
q=lambda x:Q(str(x))
def reprice(cfg,pb,pbr,supply,physical,pinputs,services):
 data=deepcopy(pb);price=supply['products'];mapping=pinputs['food']['mapping']
 for row in data['basket']:
  if row['purpose']=='01':row['purchaser_unit_quote_CU']=str(sum(q(weight)*q(price[target]['cost_allocation_exVAT_CU_unit'])*(1+q(cfg['food_VAT_sensitivity_by_product'][target])) for target,weight in mapping[row['id']].items()))
 data['home_bills']['power_quote_CU_kWh']=str(supply['power_exVAT_CU_kWh']);data['home_bills']['water_quote_CU_m3']=str(supply['water_exVAT_CU_m3'])
 oldenergy=sum(q(r['energy_cost_CU']) for r in data['goods']);retailenergy=q(physical['power']['end_use_meters_GWh']['private_goods_retail'])*1000000*q(supply['power_exVAT_CU_kWh'])
 for r in data['goods']:r['energy_cost_CU']=str(retailenergy*q(r['energy_cost_CU'])/oldenergy)
 helperenergy=q(physical['power']['end_use_meters_GWh']['private_help_depot'])*1000000*q(supply['power_exVAT_CU_kWh'])
 if cfg['helper_energy_in_old_inputs_hypothesis']:
  if helperenergy>q(data['home_help']['inputs_CU']):raise ValueError('Helper electricity exceeds assumed included old inputs')
 else:data['home_help']['inputs_CU']=str(q(data['home_help']['inputs_CU'])+helperenergy)
 # Evaluate the compatible old PB functions with revised inputs; old B/envelopes and all actual-null meanings stay.
 out=PB.compute(data);out['scope']='Current compatible food/household/retail/help meter repricing, not adequate B or a compulsory basket.'
 private=deepcopy(services['private_learning_and_reprice']);label=cfg['helper_case'];cal=private[label];oldhelp=out['home_help'][label];cal['new_helper_customer_unit_CU']=str((q(oldhelp['named_cost_exVAT_CU'])+q(cal['helper_share_CU']))*q('1.06')*q('1.1')/q(oldhelp['task_hours']));cal['repriced_retail_with_learning']=[{'id':g['id'],'learning_share_CU':old['learning_share_CU'],'revised_consumer_unit_CU':str((q(g['household_cash_CU'])+q(old['learning_share_CU'])*q('1.06')*q('1.1'))/q(g['new_units']))} for g,old in zip(out['goods_base'],cal['repriced_retail_with_learning'])]
 return data,out,private,{'retail_electricity_replacement_CU':retailenergy,'retired_retail_electricity_CU':oldenergy,'helper_electricity_CU':helperenergy,'helper_energy_inside_old_inputs_hypothesis':cfg['helper_energy_in_old_inputs_hypothesis'],'actual_adequate_B_replacement_need_or_market_price':None}
def extra_people(cfg,physical,pinputs,housing,services):
 result=[];pro=q(pinputs['pay']['professional']);front=q(pinputs['pay']['frontline'])
 def add(i,n,pay,weights):
  if n:result.append({'id':i,'count':n,'gross_each':q(pay),'public_fraction':Q(0),'salary_payer':'private','private_payer_weights':weights,'civic_each':Q(0)})
 for role,n in physical['food']['roles'].items():add('food:'+role,n,front,{'food':Q(1)})
 add('food:seasonal',physical['food']['seasonal_additional_people'],front*q(pinputs['food']['harvest_weeks'])/52,{'food':Q(1)})
 support=pinputs['existing_R05_component_support']
 for key in ['water','power']:
  part=physical[key];add(key+':professional',part['professional_people']-support['professional_people_each_utility'],pro,{key:Q(1)});add(key+':frontline',part['frontline_people']-support['frontline_people_each_utility'],front,{key:Q(1)})
 seasonal=q(physical['food']['seasonal_additional_people'])*q(pinputs['food']['harvest_weeks'])/52;food=q(physical['food']['core_people'])+seasonal;water=q(physical['water']['professional_people']+physical['water']['frontline_people']-22);power=q(physical['power']['professional_people']+physical['power']['frontline_people']-22);den=food+water+power
 add('physical:instruction',physical['additional_instructors'],pro,{'food':food/den,'water':water/den,'power':power/den})
 for role,r in housing['roles'].items():add('housing:'+role,r['posts'],q(r['pay_CU'])/q(r['posts']),{'housing':Q(1)})
 add('housing:instruction',services['housing_learning_overlay']['additional_instructors'],pro,{'housing':Q(1)})
 return result
