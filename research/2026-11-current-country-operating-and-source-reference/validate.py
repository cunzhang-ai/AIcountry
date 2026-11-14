#!/usr/bin/env python3
"""Bounded preservation, replacement, counterparty and temporal identities; no national source certificate."""
from pathlib import Path
from decimal import Decimal as Q
from copy import deepcopy
import hashlib,json,re,subprocess,sys
D=Path(__file__).resolve().parent;R=D.parent;sys.path.insert(0,str(D));from model import compute,read_results
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(ok,why):
 if not ok:raise AssertionError(why)
 checks.append(why)
def near(a,b):return abs(Q(str(a))-Q(str(b)))<Q('.000001')
def rejects(fn):
 try:fn()
 except (ValueError,TypeError):return True
 return False
(D/'validation.json').write_text(json.dumps({'edition':130,'status':'incomplete'})+'\n')
b=read(D/'baseline.json');P=D/'predecessor-design-129';old=read(P/'settlement/commitments/inventory.json');inv=read(R/'settlement/commitments/inventory.json')
check(len(b['sha256'])==996,'996exact129artifacts:995currentMarkdown and fullinventory')
check(all(sha(P/n)==h for n,h in b['sha256'].items()),'Everyexactpredecessor artifact preserved')
check(inv['functions']==old['functions'] and len(inv['functions'])==37,'All37complete originalfunction/bid/actualnullobjects exact')
check(inv['selections']==old['selections'] and len(inv['selections'])==61,'All61originalselections exact')
refs={k:v for k,v in old.items() if k.endswith('_reference') and isinstance(v,dict)}
check(len(refs)==69 and all(inv[k]==v for k,v in refs.items()),'All69inheritedreferenceobjects exact, no transferredfinalapproval')
check(all(sha(R/n)==h for n,h in old['source_hashes'].items() if n.startswith('2026-')),'Allinheriteddatedsources/models/manifests/validation exact')
check(all(sha(R/n)==b['sha256'][n] for n in ['FRAMEWORK.md','DECISION-TEMPLATE.md']),'Commonproposedmethod/template unchanged; newfinancialcandidate adoptsneitheritselfnorprocedure')
check(all(sha(R/n)==h for n,h in b['sha256'].items() if n.startswith(('country/C01/','country/C02/','country/C03/','country/C04/','country/C07/','country/C08/','country/C09/','country/C10/','country/C11/','country/C12/'))),'Existingrights/democracy/administration/services/justice/physical/defense/AI/collaboration clauses unchanged')
cfg=read(D/'inputs.json');x=compute(cfg);stored=read_results();check(x==stored,'Eightfullcurrentcases reproduce from index/separateartifacts')
idx=read(D/'results.json');check(len(idx['cases'])==8 and len({c['artifact'] for c in idx['cases'].values()})==8 and x['format_revision']=='130-current-country-v1','Explicitformatrevision/eightdistinctcaseartifacts, not a silentlychangedold125schema')
C=x['cases'];F=C['water_limited/firm_seven_extended/plural_public_backbone/A'];U=C['water_limited/firm_seven_extended/plural_public_backbone/C1'];DP=C['water_limited/firm_seven_extended/direct_public_rival/A'];S=C['water_limited/storage_extended/plural_public_backbone/A'];book=F['public_book'];person=F['personal'];supply=F['supply'];cash=F['cash_required_not_paid'];rows={r['id']:r for r in book['component_rows']}
check(len({k.split('/')[1] for k in C})==2 and {v['assumptions']['service'] for v in C.values()}=={'plural_public_backbone','direct_public_rival'} and {v['assumptions']['package'] for v in C.values()}=={'A','C1'},'Two power portfolios cross same provider/income alternatives')
for label,c in C.items():
 br=c['public_book'];rr=br['component_rows'];pp=c['personal'];ff=c['function_rows']
 check(len({r['id'] for r in rr})==len(rr) and all(r['owner'] in {f['id'] for f in old['functions']} for r in rr),'Uniquecomponent IDs/knownfunctionowners: '+label)
 check(len(ff)==37 and all(f['components'] and f['actual_full_current_cost'] is None and f['actual_owned_source_or_received_remedy'] is None for f in ff),'All37positive scopedinterfaces keepactual fullcost/source/remedynull: '+label)
 check(near(sum(Q(r['named_allocation_CU']) for r in rr),br['named_annual_allocation_CU']) and near(sum(Q(f['named_current_allocation_CU']) for f in ff),br['named_annual_allocation_CU']),'Component/function allocations reconcileonce: '+label)
 check(near(Q(br['external_cash_requirement_CU'])+Q(br['public_owned_renewal_reservation_CU'])+Q(br['continuing_scope_reservation_CU']),br['named_annual_allocation_CU']),'Externalcall/renewal/heldscope separated: '+label)
 check(pp['population']==100000 and sum(r['count'] for r in pp['people'])==100000,'Same100000personaccount, no extraagentmandates: '+label)
 check(near(sum(Q(v['PA']) for v in pp['payer_withheld'].values()),pp['totals']['PA_assessed']) and near(sum(Q(v['Y']) for v in pp['payer_withheld'].values()),pp['totals']['Y_withheld']),'Oneassessment/withholding attributedacrossactualhypotheticalpayerclasses: '+label)
 check(near(Q(pp['totals']['worked_gross_due'])-Q(pp['totals']['worked_gross_received']),pp['totals']['unpaid_wages']),'Wagedue/received/unpaidclaims conserved: '+label)
check(len(rows)==410 and all(i not in rows for i in ['labor:EL_fullfield_source','labor:EL_judicial_peak','labor:EL_legal_aid_peak','labor:EL_clerk_peak','op:health_meal_ingredients','op:learning_meal_ingredients','asset:supported_dwellings']),'Declaredoldcomponents removed once, no old-plus-newpay/ingredient/housing bill')
newpay=sum(Q(r['annual_base_CU']) for r in rows.values() if r['id'].startswith('labor:current_EL_'));check(near(newpay,11181000),'128source/court/clerk/help/drillpay carriedonce')
check(rows['labor:local_elected_roles']['people_min']==60 and near(rows['labor:local_elected_roles']['posts'],15) and near(rows['labor:local_elected_roles']['annual_base_CU'],900000),'Explicit15seatcharters require60places/15roles/900k, not old36places')
check(near(cash['local_common_named_scope_CU'],71494560) and near(sum(Q(v['named_common_duty']) for v in cash['local_sites']),71494560),'Localteachercouncillor duties attributedonce, not Gcostplusduplicatedgrant')
check(book['learning_instructors']==67 and book['new_workstation_quote_units']==5212 and DP['public_book']['new_workstation_quote_units']==5206,'Ordinaryinstruction recomputed and distinctpeakstationpool, no annualpostequality')
check(near(Q(book['new_workstation_quote_units'])*5000,26060000) and near(F['source_calls']['public_station_prestart']['new_capital_CU'],26060000),'Prestart26.06mstationcapital separatefrom annualupkeep/renewal')
check(near(sum(Q(rows[i]['annual_base_CU']) for i in ['labor:power_control','labor:power_repair','labor:water_control','labor:water_repair']),2280000),'Old44utility supportpay remains in G')
extra=[r for r in person['people'] if r['id'].startswith(('food:','water:','power:','physical:','housing:'))]
check(sum(r['count'] for r in extra)==4876 and person['unsupplied_resource_stress_people']==29556,'Newphysical/seasonal/housing groups and explicitunprovidedremainder, not unemploymentforecast')
check(near(sum(Q(r['gross_wage_due_each'])*r['count'] for r in extra),Q(56640000)+Q(372)*30000*8/52+Q(97080000)),'Physicalnetprovided/seasonal/housing/instructor wagecalls joinonce')
check(all(Q(person['B'][k])>=Q(13248)*(1 if k=='adult' else Q('.6')) for k in person['B']) and person['B']['adult']=='13248','LargeroldnominalB retained; partialrepricing cannot establishadequacy or cutrights')
check(near(F['household_prices']['named_component_quotes_CU']['adult'],Q('7981.598302482147081579825095')),'Samecompatiblefoodprices reach the partialordinaryperson quote')
check(near(F['supply']['power_exVAT_CU_kWh'],Q('.2044705947414018425871105226')) and near(S['supply']['power_exVAT_CU_kWh'],Q('.4451400947019839913163641443')),'Bothpowercapital/renewal/interest arrangements repriced, no assumedcheapstorage')
check(near(sum(Q(r['private_exVAT_invoice_CU'])+Q(r['public_exVAT_invoice_CU']) for r in supply['products'].values()),supply['food_chain_resource_plus_interest_CU']),'Samefoodprivate/publiccostallocations reconcile, no secondnationaloutputsum')
check(all(cfg['food_VAT_sensitivity_by_product'][k]=='0' for k in ['cereals','roots','vegetables','fruit','pulses','nuts']) and F['tax_scope']['actual_net_VAT_yield_input_refund_company_or_transfer_source'] is None,'Plainfoodzero-rate scope preserved; consumerVAT not actualnetTreasuryyield')
check(near(rows['hold:current_menu_scope']['external_cash_requirement_CU'],0) and near(rows['hold:current_menu_scope']['direct_public_nonpay_CU'],0) and Q(rows['hold:current_menu_scope']['named_allocation_CU'])>0,'Heldunmatchedmenu scope is not invoice, saving or a second bill')
check(near(book['continuing_scope_reservation_CU'],Q('9867812.486326042721395375544')),'Heldmenu/housing protection visible in current allocation')
h=supply['housing'];check(near(Q(h['rebuild_investment_call_reference_CU'])+Q(h['repair_temporary_learning_operating_call_CU']),181098000),'Housingrebuild versus repair/temporary/instruction sameprogramme once')
check(near(Q(h['public_rebuild_reserve_draw_CU'])+Q(h['private_rebuild_call_CU']),h['rebuild_investment_call_reference_CU']) and near(Q(h['public_operating_resource_call_CU'])+Q(h['private_operating_resource_call_CU']),h['repair_temporary_learning_operating_call_CU']),'Public/privatehousingstructuretitlehypothesis reconciles; no occupiedhomefraction/freepool')
check(rows['reserve:public_housing_renewal']['kind']=='reservation' and rows['reserve:public_housing_renewal'].get('retained_public_housing_title_quote_CU')=='600000000' and 'public_all_new_quote_CU' not in rows['reserve:public_housing_renewal'],'Retainedpublichomequote not a new600mpurchase; reserve separatefromcapitalstock')
adv=cash['local_working_advance_reference'];check([Q(a['amount_CU']) for a in adv]==[Q(45000),Q(85000),Q(150000),Q(180000)] and near(cash['local_working_advance_total_CU'],460000),'Bounded45/85/150/180k localprincipal and460k grossdisbursement exposure')
check(all(a['earliest_conditional_recovery']=='2030-02-06' and a['actual_appropriation_loan_authority_receipt_or_repayment'] is None for a in adv),'Repaymentdate conditionalon receipt/futurecommondues, not actualcollectionauthority')
events=cash['events'];issued=[e for e in events if e['kind']=='bounded_local_working_advance_financial_claim_not_grant'];repaid=[e for e in events if e['kind']=='actual_receipt_conditioned_local_principal_recovery_not_revenue'];check(near(sum(Q(e['CU']) for e in issued),sum(Q(e['CU']) for e in repaid)) and all(e['date']=='2030-01-01' for e in issued) and all(e['date']=='2030-02-06' for e in repaid),'Source/repaymentmatched once, no extraannualtax/grant income or revolvingreloan')
check(all(cash['first_unfunded_date'][k] is None for k in ['L1','L2','L3','L4']) and cash['first_unfunded_date']['G']=='2030-01-01' and cash['S_no_gap_requires_all_requested_G_backing_actually_received'],'Localschedule/Spositivebalances requiremissingGsource, not paidpayroll or fundedcountry')
check(cash['first_unfunded_date']['Renewal_housing_G'] is None and all(e['date'].endswith(('-01-01','-04-01','-07-01','-10-01')) for e in events if e['kind']=='housing_renewal_quarter_start_source_before_capital_draw'),'Housingreserve fundedbeforeeachquarterdraw, no borrowedS/otherreserve')
check(near(sum(Q(r['annual_interest_sensitivity_CU']) for r in F['source_calls']['owners']),supply['annual_new_capital_interest_CU']) and near(sum(Q(r['annual_equal_principal_cash_CU']) for r in F['source_calls']['owners']),supply['annual_new_capital_principal_CU']),'Owner-specificinterest/principal identities, principal not priceproductioncost')
check(near(F['source_calls']['named_disjoint_physical_plus_goods_normal_FU'],Q('127289288.4940607353553146263')) and F['source_calls']['actual_full_national_FX_call_or_pool'] is None,'Disjointnamed127.289mFU subtotal, no fullFXdemand/sourcepool')
check(all(r['events'][0]['date']=='2029-01-01' and r['events'][2]['date']=='2029-12-31' and r['actual_mature_year_safe_acceptance'] is None for r in F['source_calls']['owners']),'Prestartcapital/stock timeline distinctfrom full2030use, no assumedacceptance')
check(near(F['source_calls']['private_goods']['full_year_unprovided_FU'],14250000),'Privategoods1mownedopening not sharedwithphysicalowners')
check(Q(U['personal']['totals']['nonolder_U'])==Q(1020096000) and Q(U['personal']['totals']['I05'])>0,'ProtectedU/basic/extraI05 remain separate, no falseallneedscompletion')
# Material counterfactuals exercise different causes, not a second copy of implementation.
def changed(**updates):
 c=deepcopy(cfg)
 for k,v in updates.items():c[k]=v
 return compute(c)['cases']['water_limited/firm_seven_extended/plural_public_backbone/A']
a=changed(local_cash_advance_mode='none');check([a['cash_required_not_paid']['first_unfunded_date'][k] for k in ['L1','L2','L3','L4']]==['2030-01-31']*4 and near(a['cash_required_not_paid']['local_working_advance_total_CU'],0),'No-advance rival keepsactualdatedcashmismatch underthesameannualgrants')
a=changed(housing_reserve_funding_timing='month_end');check(a['cash_required_not_paid']['first_unfunded_date']['Renewal_housing_G']=='2030-01-01','Month-endformation failsbeforefirstrebuild despitepositiveannualreserve')
a=changed(station_baseline_compatible_fraction_hypothesis='0');check(a['public_book']['new_workstation_quote_units']==a['public_book']['distinct_service_people_not_fungible'] and a['public_book']['new_workstation_quote_units']>book['new_workstation_quote_units'],'Unavailablebaselineequipment cannotbe silentlyreused')
c=deepcopy(cfg);c['finance']['new_capital_interest']='0';a=compute(c)['cases']['water_limited/firm_seven_extended/plural_public_backbone/A'];prior=read(R/'2026-11-country-physical-portfolio/results.json')['cases']['water_limited/firm_seven_extended'];check(near(a['supply']['power_exVAT_CU_kWh'],prior['prices']['power_exVAT_CU_kWh']) and near(a['supply']['water_exVAT_CU_m3'],prior['prices']['water_exVAT_CU_m3']) and near(a['supply']['food_chain_resource_plus_interest_CU'],prior['prices']['food_chain_cost_CU']),'Zeroassetinterest recovers127matchedresourcequotes, includingsecondarysewagecredit')
a=changed(housing_electricity_in_old_other_cost_hypothesis=False);ah=a['supply']['housing'];check(near(Q(ah['programme_total_CU'])-Q(h['programme_total_CU']),h['construction_electricity_CU']) and Q(ah['public_rebuild_reserve_draw_CU'])>Q(h['public_rebuild_reserve_draw_CU']),'Disjointhousingenergy restores bothrebuildandnonrebuild bills, not silentlydroppedothercost')
a=changed(private_wage_received_fraction='.8');check(Q(a['personal']['totals']['unpaid_wages'])>0 and Q(a['personal']['totals']['I05'])>Q(person['totals']['I05']) and Q(a['personal']['totals']['PA_assessed'])<Q(person['totals']['PA_assessed']),'Failedprivatewages preservearrears/increaseneeds/reducetax, not automaticpaidincome')
a=changed(higher_prior_units_hypothesis=True);check(near(a['personal']['prior_earned_each'],22500) and near(Q(a['personal']['totals']['insurance_gross'])-Q(person['totals']['insurance_gross']),112500000),'Largerpriorpensionunits survivecurrentrepricing; no resettofutureoneWcap')
for mutate,why in [(lambda c:c.update(future_medium={'uninterpreted':'situated'}),'Newfuture top-levelmeaning requires interpretation'),(lambda c:c['finance'].update(future_control='uninterpreted'),'Unknownnestedfinance semantics not dropped'),(lambda c:c['sources'].update(household_inputs=c['sources']['physical_inputs']),'Changedsourcepath cannot inherit review'),(lambda c:c['finance'].update(actual_accepted_lenders_equity_currency_or_terms=True),'Model cannot declare actualfinancing'),(lambda c:c.update(actual_complete_country_source_readiness_or_better_lives=True),'No actualcountrycompletion classifier'),(lambda c:c['physical_cases'].pop(),'Missingrival cannot silentlytruncatecomparison'),(lambda c:c['food_VAT_sensitivity_by_product'].update(cereals='.1'),'Knownplainfoodzerorate cannotbe silentlyredefined'),(lambda c:c.update(private_wage_received_fraction='1.2'),'Invalidreceiptfraction rejected'),(lambda c:c.update(local_cash_advance_mode='automatic_unlimited'),'No impliedunlimitedloanpower'),(lambda c:c.update(year=2031),'Differentyear needsfreshscope'),(lambda c:c['finance'].update(equal_principal_years=True),'Boolcannotbe a principalduration')]:
 bad=deepcopy(cfg);mutate(bad);check(rejects(lambda:compute(bad)),why)
reg=read(D/'country-register.json');check(len(reg['functions'])==37 and all(v['original_complete_function_sha256']==hashlib.sha256(json.dumps(next(f for f in old['functions'] if f['id']==v['id']),sort_keys=True,separators=(',',':')).encode()).hexdigest() for v in reg['functions']),'All37currentcase sidecars tracecompleteoriginalobjects')
check(all(v['actual_full_current_cost'] is None and v['actual_owned_source'] is None for v in reg['functions']),'Actualfullfunction costs/source never filledfrompartialquotes')
sources=read(D/'sources.json');check(len(sources['external_sources'])==1 and all(sha(R/a['path'])==a['sha256'] for a in sources['local_scoped_sources']),'OriginalselectedIMFdefinition scope/localdependencies pinned; not independentprojectevidence')
contract=read(D/'source-contract.json');check(all(sha(R/n)==h for n,h in contract['sha256'].items()),'Complete declaredinput/code/meaningcontract identities match')
scope=read(D/'scope-record.json');ref=inv['current_country_operating_and_source_reference'];check(all(v is None for o in [scope,ref,x] for k,v in o.items() if k.startswith('actual_')),'Evidence/selection/actualadoption/source/readiness/receivedlives remain separate')
check('Integrated design 130' in (R/'COUNTRY-DESIGN.md').read_text() and 'integrated design 130' in (R/'DESIGN-STATUS.md').read_text(),'Countryoverview/status/C06 alignon130andoneboundednext')
check(all(not re.search('[\u4e00-\u9fff]',(R/n).read_text()) for n in scope['changed_current_markdown']),'New/editedcurrentpublicMarkdown English, historicalsourceartifacts unchanged')
check((R/'status/current/04-country-operation-and-scoped-support.md').is_file() and 'retained scoped support' in (R/'DESIGN-STATUS.md').read_text(),'Statusentrance organizedwithoutdiscarding priorscopedfollowthrough')
check(sha(R/'history/03/11-design-116-onward.md')==b['sha256']['history/03/11-design-116-onward.md'],'Precedinghistory unchanged; currentdecision extendsseparateboundedhistory')
pins=read(D/'source-manifest.json')['sha256'];check(all((R/n).is_file() and sha(R/n)==h for n,h in pins.items()),'Everydeclaredcurrent/inheritedlocal pin matches')
run=subprocess.run([sys.executable,str(R.parent/'scripts/check-research-structure.py')],capture_output=True,text=True);check(run.returncode==0,'Currentstructure/150linebound/14chapters/37singleauditowners/locallinks: '+run.stdout.strip()+run.stderr.strip())
report={'edition':130,'status':'pass','bounded_check_count':len(checks),'checks':checks,'source_pin_count':len(pins),'structure':run.stdout.strip(),'scope':'Exactpreservation and authored currentreplacement/person/tax/source/title/finance/receipt/temporal identities and adversecases only. Not actualnational cost/GDP/deficit/source/independentauthority/safepaidcapacity/receivedremedy/childorpublicchoice/betterlives.'};(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
