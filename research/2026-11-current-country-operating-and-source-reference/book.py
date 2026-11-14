"""Replace declared components once and retain unmatched continuing scope; no source/authority created."""
from decimal import Decimal as Q,ROUND_CEILING
from copy import deepcopy
q=lambda x:Q(str(x));ceil=lambda x:int(q(x).to_integral_value(rounding=ROUND_CEILING))
def direct(i,owner,kind,value,posts=0,people=None,role='professional'):
 v=q(value);return {'id':i,'owner':owner,'kind':kind,'role':role,'posts':str(posts),'people_min':people,'annual_base_CU':str(v),'public_operator_fraction':'1','supplier_base_CU':'0','supplier_margin_CU':'0','supplier_invoice_CU':'0','direct_public_salary_CU':str(v if kind=='staff' else 0),'direct_public_nonpay_CU':str(v if kind not in ['staff','hold'] else 0),'external_cash_requirement_CU':str(v if kind!='hold' else 0),'public_renewal_reservation_CU':'0','continuing_scope_reservation_CU':str(v if kind=='hold' else 0),'named_allocation_CU':str(v)}
def build(cfg,base,election,einputs,supply,pubinputs,QEbaseline):
 rows={r['id']:deepcopy(r) for r in base['component_rows']};actions=[];hold=Q(0)
 def remove(i):
  if i not in rows:raise ValueError('Missing exact predecessor component '+i)
  old=rows.pop(i);actions.append({'removed':i,'old_named_CU':old['named_allocation_CU']});return old
 def purchase(i,owner,value,retain_old=False):
  nonlocal hold
  prior=remove(i);rows[i]=direct(i,owner,'purchase',value)
  if retain_old and q(prior['named_allocation_CU'])>q(value):
   h=q(prior['named_allocation_CU'])-q(value);hold+=h;rows['hold:'+i]=direct('hold:'+i,owner,'hold',h)
  return prior
 local_old=remove('labor:local_elected_roles');local_people=sum(v['N_fixed'] for v in election['capacity']['local']);local_fraction=q(local_old['posts'])/q(local_old['people_min']);local_posts=q(local_people)*local_fraction;rows['labor:local_elected_roles']=direct('labor:local_elected_roles','D08','staff',local_posts*q(einputs['pay']['professional']),local_posts,local_people)
 plan=election['capacity']['named_work_plan'];s=einputs['source_hours'];j=einputs['judicial'];info=einputs['information'];pro=q(einputs['pay']['professional']);front=q(einputs['pay']['frontline'])
 for i in ['labor:EL_fullfield_source','labor:EL_judicial_peak','labor:EL_legal_aid_peak','labor:EL_clerk_peak']:remove(i)
 specs=[('source','D04',plan['source_people'],s['source_paid_role_fraction'],pro,'professional'),('judges','D11',plan['judges'],j['paid_role_fraction_each'],pro,'professional'),('counsel','D11',plan['counsel'],j['paid_role_fraction_each'],pro,'professional'),('clerks','D11',plan['clerks'],j['clerk_paid_role_fraction_each'],front,'frontline'),('helpers','D05',plan['information_helpers'],info['help_paid_role_fraction'],front,'frontline'),('drill_instructors','D04',plan['additional_drill_instructors'],1,pro,'professional')]
 for label,owner,n,fraction,pay,role in specs:
  i='labor:current_EL_'+label;rows[i]=direct(i,owner,'staff',q(n)*q(fraction)*pay,q(n)*q(fraction),n,role)
 purchase('op:EL_fullscope_paper','D05',election['capacity']['paper']['fullrequest_including_choice_CU'])
 purchase('op:national_service_electricity','R05',supply['bills']['public_electricity_CU'],True);purchase('op:national_service_water','R05',supply['bills']['public_water_CU'],True)
 prior_meals=[remove(i) for i in ['op:health_meal_ingredients','op:learning_meal_ingredients']];oldfood=sum(q(r['named_allocation_CU']) for r in prior_meals);newfood=q(supply['bills']['public_ingredients_payable_sensitivity_CU']);rows['op:current_institutional_ingredients']=direct('op:current_institutional_ingredients','L07','purchase',newfood)
 # Tax/menu/quality/source mismatch remains a held part of the old reference, not a saving or an invoice.
 if oldfood>newfood:
  h=oldfood-newfood;hold+=h;rows['hold:current_menu_scope']=direct('hold:current_menu_scope','L07','hold',h)
 oldhouse=remove('asset:supported_dwellings');frac=q(pubinputs['service_cases'][base['case_name']]['public_operator_fraction']);margin=q(pubinputs['service_cases'][base['case_name']]['supplier_margin']);maintenance=q(supply['housing']['public_operating_resource_call_CU']);rows['op:current_public_housing_programme']=direct('op:current_public_housing_programme','L10','purchase',maintenance);renew=q(oldhouse['public_renewal_reservation_CU']);rows['reserve:public_housing_renewal']=direct('reserve:public_housing_renewal','L10','reservation',0);rows['reserve:public_housing_renewal'].update(public_renewal_reservation_CU=str(renew),named_allocation_CU=str(renew),retained_public_housing_title_quote_CU=oldhouse['public_all_new_quote_CU'])
 oldmaintenance=q(oldhouse['external_cash_requirement_CU']);continuing=oldmaintenance if not cfg['housing_upkeep_scope_compatible_hypothesis'] else max(Q(0),oldmaintenance-maintenance)
 if continuing:hold+=continuing;rows['hold:public_housing_scope']=direct('hold:public_housing_scope','L10','hold',continuing)
 oldteachers=remove('labor:current_learning_instructors');n=sum(q(r['posts']) for r in rows.values() if r['kind']=='staff' and r['id']!='labor:current_EL_drill_instructors');load=q(pubinputs['calendar']['learning_activity_hours'])/q(pubinputs['calendar']['learning_group'])*(1+q(pubinputs['calendar']['instructor_preparation_fraction']));H=q(pubinputs['calendar']['annual_task_hours']);k=0
 for _ in range(100):
  new=ceil((n+k)*load/H)
  if new==k:break
  k=new
 else:raise ValueError('No bounded ordinary instruction fixedpoint')
 #128already prices its drill instructors own learning;127prices new physical/seasonal learning separately.
 row=direct('labor:current_learning_instructors','L07','staff',q(k)*pro,k,k);row.update(public_operator_fraction=str(frac),supplier_base_CU=str((1-frac)*k*pro),supplier_margin_CU=str((1-frac)*k*pro*margin),supplier_invoice_CU=str((1-frac)*k*pro*(1+margin)),direct_public_salary_CU=str(frac*k*pro),external_cash_requirement_CU=str(k*pro*(1+(1-frac)*margin)),named_allocation_CU=str(k*pro*(1+(1-frac)*margin)));rows[row['id']]=row
 remove('asset:shared_new_secure_workstations');distinct=sum(ceil(max(q(r['posts']),q(r['people_min'] or 0))) for r in rows.values() if r['kind']=='staff');baseline=q(QEbaseline)*q(cfg['station_baseline_compatible_fraction_hypothesis']);stations=ceil(max(Q(0),q(distinct)-baseline));sc=pubinputs['new_shared_stations'];up=q(stations)*q(sc['upkeep_CU_year']);reservation=q(stations)*q(sc['unit_CU'])/q(sc['life_years']);asset=direct('asset:shared_new_secure_workstations','K03','asset',up);asset.update(annual_upkeep_CU=str(up),renewal_CU=str(reservation),all_new_quote_CU=str(q(stations)*q(sc['unit_CU'])),public_title_fraction='1',public_renewal_reservation_CU=str(reservation),named_allocation_CU=str(up+reservation),public_all_new_quote_CU=str(q(stations)*q(sc['unit_CU'])));rows[asset['id']]=asset
 values=list(rows.values());annual=sum(q(r['named_allocation_CU']) for r in values);return {'case_name':base['case_name'],'component_rows':values,'replacement_actions':actions,'named_annual_allocation_CU':str(annual),'external_cash_requirement_CU':str(sum(q(r['external_cash_requirement_CU']) for r in values)),'public_owned_renewal_reservation_CU':str(sum(q(r['public_renewal_reservation_CU']) for r in values)),'continuing_scope_reservation_CU':str(hold),'housing_renewal_reservation_CU':str(renew),'housing_rebuild_reserve_draw_CU':str(supply['housing']['public_rebuild_reserve_draw_CU']),'employee_pay_both_public_and_supplier_CU':str(sum(q(r['annual_base_CU']) for r in values if r['kind']=='staff')),'paid_role_equivalents':str(sum(q(r['posts']) for r in values if r['kind']=='staff')),'distinct_service_people_not_fungible':distinct,'new_workstation_quote_units':stations,'learning_instructors':k,'actual_full_current_cost_or_source_or_roster':None}
