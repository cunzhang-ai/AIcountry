"""Independent authored amount/date probes, not a tax/identity/legal readiness engine."""
from pathlib import Path
from datetime import date,timedelta
import calendar,json,math
HERE=Path(__file__).resolve().parent
PARTITION='distinct cash wage after separate Y; pension; interest; exempt U I05 costs; restored owned principal'
NONCASH='actually delivered private employer-owned dwelling; comparable price assumed; distinct employee payment'
CALENDAR='working-day indices only, no actual holiday calendar'
def keys(x,names):
    if not isinstance(x,dict) or set(x)!=set(names.split()):raise ValueError('Unsupported or missing declared semantics')
def number(x,positive=False):
    if isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) or x<0 or (positive and x<=0):raise ValueError('Unknown/invalid amount, not zero')
    return x
def integer(x,limit=None):
    number(x)
    if not isinstance(x,int) or (limit is not None and x>limit):raise ValueError('Unsupported integer range')
    return x
def day(s):
    if not isinstance(s,str):raise ValueError('Missing date')
    try:d=date.fromisoformat(s)
    except (ValueError,TypeError):raise ValueError('Unsupported Gregorian date')
    if d.isoformat()!=s:raise ValueError('Noncanonical date')
    return d
def months(d,n):
    year=d.year+(d.month-1+n)//12;month=(d.month-1+n)%12+1
    return date(year,month,min(d.day,calendar.monthrange(year,month)[1]))
def tax(income,M):
    number(income);number(M,True)
    return round(min(income,.5*M)*.20+min(max(0,income-.5*M),.5*M)*.35+min(max(0,income-M),M)*.45+max(0,income-2*M)*.55,8)
def calculate(c=None):
    if c is None:c=json.loads((HERE/'inputs.json').read_text())
    keys(c,'edition unit personal two_jobs withholding scale business foreign noncash refund_ordinals interest_quantity commencement assessment collection grossup')
    if type(c['edition']) is not int or c['edition']!=100 or c['unit']!='invented CU; separate authored probes, not one national budget':raise ValueError('Different scope')
    p=c['personal'];keys(p,'partition M worked_cash paid_Y earned_pension interest ordinary_U residual_I05 cost_refund restored_principal')
    if p['partition']!=PARTITION:raise ValueError('Unsupported income ownership/category semantics')
    for k,v in p.items():
        if k!='partition':number(v,k=='M')
    if p['paid_Y']>p['worked_cash']:raise ValueError('Y fixture exceeds worked cash')
    base=p['worked_cash']-p['paid_Y']+p['earned_pension']+p['interest']
    out={'personal':{'taxable_base':base,'tax':tax(base,p['M']),'excluded_not_cash_source':sum(p[k] for k in ['ordinary_U','residual_I05','cost_refund','restored_principal'])}}
    j=c['two_jobs'];keys(j,'M post_Y_job_A post_Y_job_B provisional_withheld')
    for k,v in j.items():number(v,k=='M')
    total=tax(j['post_Y_job_A']+j['post_Y_job_B'],j['M'])
    out['two_jobs']={'one_annual_tax':total,'wrong_two_bandsets':tax(j['post_Y_job_A'],j['M'])+tax(j['post_Y_job_B'],j['M']),'remaining_balance':max(0,total-j['provisional_withheld'])}
    h=c['withholding'];keys(h,'annual_liability proved_deducted actually_remitted')
    for v in h.values():number(v)
    if h['actually_remitted']>h['proved_deducted']:raise ValueError('Different remittance/credit scope')
    out['withholding']={'taxpayer_refund':max(0,h['proved_deducted']-h['annual_liability']),'taxpayer_balance':max(0,h['annual_liability']-h['proved_deducted']),'payer_receivable':h['proved_deducted']-h['actually_remitted'],'Treasury_cash_before_refund':h['actually_remitted']}
    s=c['scale'];keys(s,'prior_M new_verified_CPI_ratio new_verified_W');old=number(s['prior_M'],True)
    candidates=[old]
    if s['new_verified_CPI_ratio'] is not None:candidates.append(old*number(s['new_verified_CPI_ratio'],True))
    if s['new_verified_W'] is not None:candidates.append(number(s['new_verified_W'],True))
    out['scale']={'next_M':max(candidates),'missing_components':[k for k in ['new_verified_CPI_ratio','new_verified_W'] if s[k] is None]}
    b=c['business'];keys(b,'M received_sales paid_current_cost equipment_basis lawful_paid_Y')
    for k,v in b.items():number(v,k=='M')
    net=b['received_sales']-b['paid_current_cost']-b['equipment_basis']/5
    if net<0 or b['lawful_paid_Y']>net:raise ValueError('This positive business probe does not establish loss/Y eligibility')
    out['business']={'capital_first_year':b['equipment_basis']/5,'net_before_Y':net,'taxable_after_Y':net-b['lawful_paid_Y'],'tax':tax(net-b['lawful_paid_Y'],b['M'])}
    f=c['foreign'];keys(f,'M domestic_positive foreign_positive qualifying_foreign_paid domestic_tax_actually_paid_on_same_income')
    for k,v in f.items():number(v,k=='M')
    positive=f['domestic_positive']+f['foreign_positive']
    if positive<=0:raise ValueError('No attributable positive income')
    domestic=tax(positive,f['M']);cap=domestic*f['foreign_positive']/positive;credit=min(cap,f['qualifying_foreign_paid'])
    out['foreign']={'tax_before_credit':domestic,'foreign_attributable_cap':cap,'credit':credit,'tax_after_credit':domestic-credit,'late_relief_max_if_other_lawful_conditions':min(credit,f['domestic_tax_actually_paid_on_same_income'])}
    n=c['noncash'];keys(n,'declared_meaning monthly_comparable monthly_employee_payment delivered_months')
    if n['declared_meaning']!=NONCASH:raise ValueError('Unsupported delivery/necessity/value semantics')
    number(n['monthly_comparable']);number(n['monthly_employee_payment']);integer(n['delivered_months'],12)
    out['noncash']={'benefit_value_if_proved':max(0,n['monthly_comparable']-n['monthly_employee_payment'])*n['delivered_months'],'actual_valuation_or_safe_cash_or_grossup':None}
    q=c['refund_ordinals'];keys(q,'declared_calendar first_sufficient later_referral actual_payment_index_fixture')
    if q['declared_calendar']!=CALENDAR:raise ValueError('Unknown calendar semantics')
    for k,v in q.items():
        if k!='declared_calendar':integer(v)
    if q['later_referral']<q['first_sufficient'] or q['actual_payment_index_fixture']<q['first_sufficient']:raise ValueError('Invalid ordered indices')
    due=q['first_sufficient']+10
    out['refund_ordinals']={'original_due_index':due,'within_original_bound':q['actual_payment_index_fixture']<=due,'misleading_later_referral_bound':q['actual_payment_index_fixture']<=q['later_referral']+10,'actual_undisputed_status_or_legal_calendar_or_receipt':None}
    i=c['interest_quantity'];keys(i,'principal annual_rate unpaid_days_in_year calendar_year_days')
    number(i['principal']);number(i['annual_rate']);integer(i['unpaid_days_in_year']);integer(i['calendar_year_days'])
    if i['annual_rate']>.05 or i['calendar_year_days'] not in (365,366) or i['unpaid_days_in_year']>i['calendar_year_days']:raise ValueError('Different annual simple-interest scope')
    out['interest_quantity']={'simple_amount':i['principal']*i['annual_rate']*i['unpaid_days_in_year']/i['calendar_year_days'],'actual_rate_or_accrual_entitlement':None}
    a=c['commencement'];keys(a,'hypothetical_Act');act=day(a['hypothetical_Act']);ann=months(act,12)
    first=date(ann.year,1,1)
    if first<ann:first=date(ann.year+1,1,1)
    out['commencement']={'procedure_180_calendar_days':(act+timedelta(days=180)).isoformat(),'new_personal_tax_first_Jan1_after_12months':first.isoformat(),'actual_law_or_U_readiness':None}
    a=c['assessment'];keys(a,'statutory_due final_service_date_fixture court_proved_concealed_months_fixture');due=day(a['statutory_due']);served=day(a['final_service_date_fixture']);toll=integer(a['court_proved_concealed_months_fixture'],24)
    ordinary=months(due,48);outer=months(ordinary,toll)
    out['assessment']={'ordinary_final_service_outer':ordinary.isoformat(),'conditional_concealment_outer':outer.isoformat(),'ordinary_date_bound':due<=served<=ordinary,'conditional_date_bound':due<=served<=outer,'actual_tax_or_usable_final_notice_or_intent_or_order':None}
    a=c['collection'];keys(a,'first_administrative_due later_judgment attempt_date_fixture court_proved_evasion_months_fixture');due=day(a['first_administrative_due']);judgment=day(a['later_judgment']);attempt=day(a['attempt_date_fixture']);toll=integer(a['court_proved_evasion_months_fixture'],24)
    if judgment<due or attempt<due:raise ValueError('Invalid first-due chronology')
    outer=months(due,72+toll)
    out['collection']={'original_all_in_outer':outer.isoformat(),'attempt_within_original_bound':attempt<=outer,'wrong_judgment_reset_outer':months(judgment,72).isoformat(),'misleading_reset_bound':attempt<=months(judgment,72),'actual_enforceable_tax_or_evasion_or_collection_order':None}
    g=c['grossup'];keys(g,'declared_scope M other_taxable benefit_values actually_remitted')
    if g['declared_scope']!='standalone PA10 arithmetic; no foreign credit or prior net-promise rule inferred':raise ValueError('Different tax-inclusive benefit semantics')
    number(g['M'],True);number(g['other_taxable']);number(g['actually_remitted'])
    if not isinstance(g['benefit_values'],list) or not g['benefit_values']:raise ValueError('Missing declared distinct employer values')
    V=sum(number(x) for x in g['benefit_values']);O=g['other_taxable']
    if V<=0:raise ValueError('No positive delivered benefit fixture')
    lo,hi=0,V*.55/.45
    for _ in range(100):
        mid=(lo+hi)/2
        if mid<tax(O+V+mid,g['M'])-tax(O,g['M']):lo=mid
        else:hi=mid
    topup=round((lo+hi)/2,8)
    if g['actually_remitted']>topup:raise ValueError('Different excess-remittance/refund scope')
    out['grossup']={'total_benefit':V,'tax_inclusive_employer_g':topup,'pro_rata_employer_g':[round(topup*x/V,8) for x in g['benefit_values']],'worker_extra_cash_burden':0,'conditional_statutory_credit':topup,'employer_receivable':topup-g['actually_remitted'],'Treasury_actual_cash':g['actually_remitted'],'actual_benefit_or_designated_employer_or_credit_entitlement':None}
    out['actual']={k:None for k in ['legal_adoption','affected_participation','independent_professional_review','qualified_staff_and_courts','source_cash_and_FX','received_remedies','observed_outcomes']}
    return out
if __name__=='__main__':(HERE/'results.json').write_text(json.dumps(calculate(),indent=2,allow_nan=False)+'\n')
