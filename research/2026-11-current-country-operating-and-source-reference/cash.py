"""Dated required-payment counterfactual; negative balances are missing source, never paid cash."""
from decimal import Decimal as Q
from datetime import date,timedelta
from calendar import monthrange
q=lambda n:Q(str(n))
def working_after(d,n):
 for _ in range(n):
  d+=timedelta(days=1)
  while d.weekday()>=5:d+=timedelta(days=1)
 return d

def compute(cfg,case,personal,services,bridge=False):
 year=cfg['year'];book=services['service_cases'][case['service']];rows=book['component_rows'];localids=set(cfg['local_teacher_component_ids']);byid={v['id']:v for v in rows};nlocal=len(cfg['local_sites']);t={k:q(v) for k,v in personal['totals'].items()};pay={k:{a:q(b) for a,b in v.items()} for k,v in personal['payer_withheld'].items()}
 localneed=sum(q(byid[k]['named_allocation_CU']) for k in localids);localpub=sum(q(byid[k]['direct_public_salary_CU']) for k in localids);localpurchase=localneed-localpub
 Gpub=sum(q(v['direct_public_salary_CU']) for v in rows)-localpub;Gnonpay=sum(q(v['supplier_invoice_CU'])+q(v['direct_public_nonpay_CU']) for v in rows)-localpurchase
 credit=q(services['democratic_fullfield_reference']['credit_total_envelope_CU']);Gnonpay-=credit;renewal=q(book['public_owned_renewal_reservation_CU']);care=q(personal['care_credit_G_to_S']);pension=t['insurance_gross']/12;reserve=pension*q(cfg['S_postdue_months']);events=[];locals=[]
 def add(d,src,dst,amount,kind):
  amount=q(amount)
  if amount<0:raise ValueError('Negative nominal event')
  if amount:events.append({'date':d.isoformat(),'from':src,'to':dst,'CU':str(amount),'kind':kind})
 for site in cfg['local_sites']:
  levy=q(site['taxable_site_base'])*q(cfg['local_rate']);cash=levy-q(site['deferral'])-q(site['stay']);C=q(cfg['local_share'])*cash;N=localneed/nlocal;grant=max(Q(0),N-q(cfg['equalization_withdrawal'])*C)
  locals.append({'id':site['id'],'named_common_duty':str(N),'representative_capacity':str(C),'annual_grant':str(grant),'annual_cash_site':str(C),'post_grant_plus_own_cash':str(C+grant),'actual_full_local_need_or_source':None})
 for m in range(1,13):
  start=date(year,m,1);end=date(year,m,monthrange(year,m)[1]);next15=date(year+(m==12),m%12+1,15)
  add(start,'G','S',care/12,'qualifiedcarecredit_not_general_income');add(start,'G','people', sum(q(personal['monthly_totals'][m-1][k]) for k in ['I05','nonolder_U','Y_basic']),'advance_personal_protection_conditional');add(start,'G','suppliers_and_civic',Gnonpay/12,'named_nonpay_and_supplier_prepay');add(start,'S','pension_receivers',pension-pay['S']['PA']/12,'net_earned_survivor_advance');add(start,'S','S_tax_custody',pay['S']['PA']/12,'pension_withheld_PA_protected');add(next15,'S_tax_custody','G',pay['S']['PA']/12,'prior_month_pension_PA_settlement')
  # Payroll clears gross first; withholding cannot create an independent national source.
  add(end,'G','workers', (Gpub-pay['G']['PA']-pay['G']['Y'])/12,'G_net_wage_after_actual_deduction');add(end,'G','G_Y_custody',pay['G']['Y']/12,'G_worked_Y_protected');add(next15,'G_Y_custody','S',pay['G']['Y']/12,'prior_month_G_worked_Y_settlement');housing_reserve=q(book['housing_renewal_reservation_CU'])
  add(end,'G','Renewal_other_G',(renewal-housing_reserve)/12,'other_owned_renewal_reserved_not_external_invoice')
  if services['housing_reserve_funding_timing']=='month_end':add(end,'G','Renewal_housing_G',housing_reserve/12,'housing_renewal_formation_month_end_sensitivity')
  if services['housing_reserve_funding_timing']=='quarter_start' and m in [1,4,7,10]:add(start,'G','Renewal_housing_G',housing_reserve/4,'housing_renewal_quarter_start_source_before_capital_draw')
  if m in [1,4,7,10]:add(start,'Renewal_housing_G','housing_operator',q(book['housing_rebuild_reserve_draw_CU'])/4,'public_rebuild_call_from_own_housing_reserve_not_second_G_invoice')
  add(start,'G','Continuing_scope_G',q(book['continuing_scope_reservation_CU'])/12,'held_unmatched_continuing_scope_not_a_supplier_invoice')
  for owner in ['private','food','water','power','housing']:
   add(next15,owner+'_employers','G',pay[owner]['PA']/12,'prior_month_'+owner+'_PA_only_if_paid_deducted_remitted');add(next15,owner+'_employers','S',pay[owner]['Y']/12,'prior_month_'+owner+'_Y_only_if_paid_deducted_remitted')
  for loc in locals:
   lid=loc['id'];add(start,'G',lid,q(loc['annual_grant'])/12,'local_equalization_firstday');add(start,lid,'suppliers',localpurchase/nlocal/12,'local_named_supplier_prepay');add(end,lid,'workers',(localpub-pay['local']['PA']-pay['local']['Y'])/nlocal/12,'local_net_wage');add(end,lid,lid+'_tax_custody',pay['local']['PA']/nlocal/12,'local_PA_protected');add(end,lid,lid+'_Y_custody',pay['local']['Y']/nlocal/12,'local_Y_protected');add(next15,lid+'_tax_custody','G',pay['local']['PA']/nlocal/12,'prior_month_local_PA');add(next15,lid+'_Y_custody','S',pay['local']['Y']/nlocal/12,'prior_month_local_Y')
  # Actual collected public-owner rent is a separate receipt after the advance, not a preexisting source.
  add(end,'public_tenants','G',q(26600000)/12,'same_month_rent_if_actual_title_collection')
  if m in [1,6]:add(start,'G','political_custody',q(883200 if m==1 else 1324800),'fully_assigned_credit_sensitivity_not_all_actual_spend')
 # Each quarterly receipt belongs to the actual floor-rate/held shares, not assessed gross.
 for quarter in range(0,5):
  month=quarter*3+1;due=date(year+(month>12),(month-1)%12+1,30)
  for site,loc in zip(cfg['local_sites'],locals):
   cash=q(loc['annual_cash_site'])/q(cfg['local_share'])/4;add(due,'site_taxpayers','G',cash*(1-q(cfg['local_share'])),'quarterly_national_site_share_if_received');add(due,'site_taxpayers','site_local_custody',cash*q(cfg['local_share']),'quarterly_local_owned_collection');add(working_after(due,5),'site_local_custody',site['id'],cash*q(cfg['local_share']),'local_distribution_five_workdays_no_holiday_assumption')
 bond=cfg['named_legacy_bond']
 for month in [6,12]:
  end=date(year,month,monthrange(year,month)[1])
  for holder,principal in bond['holders'].items():add(end,'G',holder,q(principal)*q(bond['coupon'])/2,'existing_coupon_not_new_output')
 for holder,principal in bond['holders'].items():add(date(year,12,31),'G',holder,q(principal)*q(bond['redemption_fraction_Dec31']),'maturing_principal_not_current_income')
 if bridge:
  z=cfg['conditional_bridge'];add(date.fromisoformat(z['draw']),z['lender'],'G',z['principal'],'conditional_new_borrowing_not_tax_or_income')
  for month in range(1,13):add(date(year,month,monthrange(year,month)[1]),'G',z['lender'],q(z['principal'])*q(z['coupon'])/12,'conditional_bridge_coupon')
  add(date.fromisoformat(z['repay']),'G',z['lender'],z['principal'],'bridge_principal_repayment_no_automatic_rollover')
 # Proposed bounded source/recovery schedule under NF24: loan is a separate financial claim, never grant revenue.
 advances=[]
 if services['local_cash_advance_mode']=='bounded_first_receipt':
  original_events=list(events);dates=sorted({e['date'] for e in original_events})
  for loc in locals:
   lid=loc['id'];running=q(cfg['opening_CU'][lid]);path=[]
   for ds in dates:
    running+=sum(q(e['CU'])*(int(e['to']==lid)-int(e['from']==lid)) for e in original_events if e['date']==ds);path.append((ds,running))
   amount=max(Q(0),-min([q(cfg['opening_CU'][lid])]+[value for _,value in path]));recovery=None
   if amount:
    add(date(year,1,1),'G',lid,amount,'bounded_local_working_advance_financial_claim_not_grant')
    # A conditional model date is admissible only after an owned receipt and when all later named common dues remain covered.
    receipt_dates=sorted({e['date'] for e in original_events if e['to']==lid and e['kind']=='local_distribution_five_workdays_no_holiday_assumption'})
    for ds in receipt_dates:
     received=sum(q(e['CU']) for e in original_events if e['date']==ds and e['to']==lid and e['kind']=='local_distribution_five_workdays_no_holiday_assumption')
     if received>=amount and all(value>=0 for day,value in path if day>=ds):recovery=ds;add(date.fromisoformat(ds),lid,'G',amount,'actual_receipt_conditioned_local_principal_recovery_not_revenue');break
   advances.append({'local':lid,'amount_CU':str(amount),'earliest_conditional_recovery':recovery,'principal_carry_if_no_safe_named_recovery_CU':str(amount if recovery is None else 0),'actual_appropriation_loan_authority_receipt_or_repayment':None})
 # Daily bundles contain simultaneous obligations; no model-chosen payment priority is executed.
 opening={k:q(v) for k,v in cfg['opening_CU'].items()};balances=dict(opening);accounts=['G','S','Renewal_housing_G','Renewal_other_G','Continuing_scope_G']+[v['id'] for v in locals];minimum={k:opening[k] for k in accounts};peakgap={k:Q(0) for k in accounts};first={k:None for k in accounts};daily=[];resolved=[];backing=Q(0);yearend=None;withheld_claims={}
 days=sorted({v['date'] for v in events}|{date(year+1,1,1).isoformat()})
 for ds in days:
  d=date.fromisoformat(ds);current=[v for v in events if v['date']==ds];newback=Q(0)
  # Before each known pension due event, care transfer and explicit G backing must exist.
  if d.day==1 and (d.year==year or d==date(year+1,1,1)):
   incoming=sum(q(v['CU']) for v in current if v['to']=='S');out=sum(q(v['CU']) for v in current if v['from']=='S');extra_due=pension if d.year>year else Q(0)
   newback=max(Q(0),out+extra_due+reserve-balances.get('S',Q(0))-incoming);backing+=newback
   if newback:current.insert(0,{'date':ds,'from':'G','to':'S','CU':str(newback),'kind':'required_G_insurance_backing_no_source_claim'})
   if d.year>year:current.append({'date':ds,'from':'S','to':'pension_receivers','CU':str(pension),'kind':'next_known_nominal_due_index_and_newcohorts_unpriced'})
  resolved.extend(current)
  before=dict(balances);Gfirsthold=Q(1324800) if d<date(year,6,1) else Q(0)
  for v in current:
   amount=q(v['CU']);balances[v['from']]=balances.get(v['from'],Q(0))-amount;balances[v['to']]=balances.get(v['to'],Q(0))+amount
  # Check gross clearance before reusing own same-event tax; local gross withholding stays protected.
  gross_extra=pay['G']['PA']/12 if d.year==year and d.day==monthrange(d.year,d.month)[1] else Q(0)
  for acc in accounts:
   target=reserve if acc=='S' else Gfirsthold if acc=='G' else Q(0);pos=balances.get(acc,Q(0))-target-(gross_extra if acc=='G' else 0);gap=max(Q(0),-pos);minimum[acc]=min(minimum[acc],pos);peakgap[acc]=max(peakgap[acc],gap)
   if gap and first[acc] is None:first[acc]=ds
  if d.year==year and d.month==12 and d.day==31:yearend={k:str(v) for k,v in balances.items() if k in accounts or 'custody' in k or k in ['Renewal_housing_G','Renewal_other_G','Continuing_scope_G']}
  daily.append({'date':ds,'required_balances':{k:str(balances.get(k,Q(0))) for k in accounts},'required_extra_G_to_S':str(newback),'unfunded_source_by_account':{k:str(max(Q(0),-balances.get(k,Q(0))+(reserve if k=='S' else Gfirsthold if k=='G' else 0))) for k in accounts},'actual_receipt_or_executed_priority':None})
 imported=sum(q(v['annual_foreign_quote_FU']) for v in services.get('unused_goods',[])) if 'unused_goods' in services else q(15250000)
 fxopening=q(cfg['private_goods_source']['opening_owned_FU'])
 return {'scope':'Source-year2030 plus specified nextJanuary pension/settlement/site events only, not full2031Gduty coverage. Required-payment conditional path; later receipts depend on earlier delivery/valid deduction/collection. Stop funded claim at firstgap; signedbalances not actual overdraft, actual receipts or priority.','conditional_bridge':bridge,'local_working_advance_reference':advances,'local_working_advance_total_CU':str(sum(q(a['amount_CU']) for a in advances)),'local_advance_is_financial_receivable_not_new_tax_or_grant':True,'local_common_named_scope_CU':str(localneed),'local_sites':locals,'events':resolved,'daily_required':daily,'yearend_before_next_due':yearend,'first_unfunded_date':first,'peak_additional_source_over_required_accounts_CU':{k:str(v) for k,v in peakgap.items()},'G_to_S_backing_including_next_known_due':str(backing),'S_known_gross_monthly_due':str(pension),'S_four_month_postdue_partial_reserve':str(reserve),'S_administration_extra_index_priorclaims_or75year_tail':None,'known_bond_closing_principal':str(q(bond['principal'])*(1-q(bond['redemption_fraction_Dec31']))),'yearend_withheld_PA_Y_still_owned_and_due_nextJan15':{k:str(v) for k,v in (yearend or {}).items() if 'custody' in k},'private_goods_FX':{'owner':cfg['private_goods_source']['owner'],'named_annual_FU':str(imported),'supplied_opening_owned_FU':str(fxopening),'additional_owned_FU_required_for_full_named_year':str(max(Q(0),imported-fxopening)),'first_month_required_FU':str(imported/12),'first_month_missing_FU':str(max(Q(0),imported/12-fxopening)),'actual_foreign_source_or_route':None},'S_no_gap_requires_all_requested_G_backing_actually_received':True,'full_nextyear_G_personal_service_index_or_cohort_scope':None,'actual_funded_path_or_source_or_safe_operation':None}
