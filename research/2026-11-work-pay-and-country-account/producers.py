"""A bounded ordinary-goods recipe, not complete private demand or delivered prices."""
import math


def ordinary_goods(c,H):
    P=c['population'];D=c['dwellings'];gar=P*c['garments_person_year'];hyg=P*c['hygiene_kg_person_year']
    devices=c['device_stock']/c['device_life'];apstock=D*c['appliances_dwelling'];apps=apstock/c['appliance_life']
    goods=[dict(id='garments',quantity=gar,unit='item',border_invoice_CU=gar*c['garment_border_CU'],tonnes=gar*c['garment_kg']/1000),
           dict(id='hygiene',quantity=hyg,unit='kg',border_invoice_CU=hyg*c['hygiene_border_CU_kg'],tonnes=hyg/1000),
           dict(id='devices',quantity=devices,unit='replacement device',border_invoice_CU=devices*c['device_border_CU'],tonnes=devices*c['device_kg']/1000),
           dict(id='appliances',quantity=apps,unit='replacement appliance',border_invoice_CU=apps*c['appliance_border_CU'],tonnes=apps*c['appliance_kg']/1000)]
    mass=sum(x['tonnes'] for x in goods);border=sum(x['border_invoice_CU'] for x in goods)
    tx=gar+hyg/c['hygiene_pack_kg']+devices+apps
    shoptasks=tx*c['retail_activities_item']+mass*4+c['retail_outlets']*365+c['retail_outlets']*2*52
    shopcov=c['retail_outlets']*c['retail_people']*c['retail_daily_hours']*c['retail_days']
    haulkm=mass*c['goods_haul_km']/c['truck_load_tonnes']*(1+c['truck_empty_return_fraction'])
    haulh=haulkm/c['truck_speed_km_h']+mass/c['truck_load_tonnes']*c['truck_handling_hours_trip']
    ppkm=P*c['bus_passenger_km_person'];service=ppkm/c['bus_average_passengers'];dead=service*c['bus_deadhead_fraction'];buskm=service+dead
    fleet=math.ceil(buskm/c['bus_km_year']);drive=(service/c['bus_service_speed']+dead/c['bus_deadhead_speed'])*(1+c['bus_preparation_fraction'])
    roles=[]
    def role(prod,id,kind,tasks,coverage=0):
        h=max(tasks,coverage);n=math.ceil(h/H)
        roles.append(dict(producer=prod,id=id,role=kind,task_hours=tasks,coverage_hours=coverage,required_hours=h,annual_post_bound=n,payroll_CU=n*c[kind+'_annual_pay_CU'],actual_employment_offer_or_assignment=None))
    role('shops','retail','ordinary',shoptasks,shopcov);role('goods_haul','border_to_shop','ordinary',haulh)
    role('communications','help','ordinary',P*2*.25);role('communications','field','professional',75000*.2*2)
    role('communications','core','professional',6000,8760);role('communications','independent_assessment','professional',1000)
    role('durable_repair','repair','ordinary',10000+45000*2)
    role('grooming','contact_and_preparation','ordinary',P*6*.5*1.25);role('professional_service','contact_and_admin','professional',100000*1.25)
    role('bus','drivers','ordinary',drive);role('bus','mechanics','ordinary',fleet*400)
    role('bus','dispatch','ordinary',2*16*365);role('bus','access_booking','ordinary',20000*.25);role('bus','planning','professional',3000)
    assets=[]
    def asset(prod,id,q,p,life):assets.append(dict(producer=prod,id=id,quantity=q,unit_quote_CU=p,life_years=life,gross_replacement_quote_CU=q*p,CFC_quote_CU=q*p/life,owner_and_vintage=None,included_predecessor_component=None,new_purchase_source=None))
    asset('shops','buildings',4000,1500,30);asset('shops','fitout',40,25000,10);asset('shops','terminals',80,1000,5)
    asset('goods_haul','trucks',3,100000,10)
    for id,q,p,L in [('terminals',75000,100,8),('drops',75000,150,30),('duct_m',750000,30,30),('aggregation',30,100000,10),('cores',2,500000,8),('premises_m2',500,1500,30),('field_vans',30,25000,10)]:asset('communications',id,q,p,L)
    asset('durable_repair','workshops_m2',2000,1500,30);asset('durable_repair','tools',20,25000,10);asset('durable_repair','vans',20,25000,10)
    asset('grooming','buildings_m2',4000,1500,30);asset('grooming','equipment',40,10000,5)
    asset('professional_service','buildings_m2',2000,1500,30);asset('professional_service','equipment',20,20000,5)
    asset('bus','fleet',fleet,250000,12);asset('bus','depot_m2',12400,1000,30);asset('bus','tools',1,1000000,10);asset('bus','shelters',100,10000,20)
    E=dict(shops=2,goods_haul=0,communications=4,durable_repair=1,grooming=1,professional_service=1,bus=1)
    # These are current purchases separate from listed work and periodic asset renewal.
    O=dict(shops=4160*3+40*1000,goods_haul=haulkm*.3*c['diesel_border_CU_litre']+3*3000,
           communications=75000*100*12*.01+452500+100000+450000*.08*c['diesel_border_CU_litre']+30*2000,
           durable_repair=10000*20+45000*30+300000*.08*c['diesel_border_CU_litre']+20*2000,
           grooming=600000*.05*5+2000*5,professional_service=100000*.5,
           bus=buskm*c['bus_fuel_litres_km']*c['diesel_border_CU_litre']+fleet*10000+fleet*3000)
    producers=[]
    for prod in E:
        pay=sum(x['payroll_CU'] for x in roles if x['producer']==prod);cap=sum(x['gross_replacement_quote_CU'] for x in assets if x['producer']==prod);cfc=sum(x['CFC_quote_CU'] for x in assets if x['producer']==prod)
        power=E[prod]*1e6*c['reference_electricity_CU_kWh']
        producers.append(dict(id=prod,named_payroll_CU=pay,other_current_quotes_CU=O[prod],electricity_GWh=E[prod],electricity_reference_cost_CU=power,operator_asset_quote_CU=cap,CFC_reference_CU=cfc,
                              named_annual_cost_subtotal_CU=pay+O[prod]+power+cfc,land_finance_insurance_and_supplier_tail=None,complete_delivered_price=None,actual_funded_capacity=None))
    return dict(final_goods=goods,producer_recipes=producers,role_requirements=roles,operator_assets=assets,
                annual_final_goods_border_quote_CU=border,inbound_tonnes=mass,retail_transactions=tx,retail_task_hours=shoptasks,retail_coverage_hours=shopcov,
                normal_annual_posts=sum(x['annual_post_bound'] for x in roles),named_annual_payroll_CU=sum(x['payroll_CU'] for x in roles),
                operator_gross_asset_quote_CU=sum(x['gross_replacement_quote_CU'] for x in assets),operator_CFC_quote_CU=sum(x['CFC_quote_CU'] for x in assets),
                household_device_appliance_stock_quote_CU=c['device_stock']*c['device_border_CU']+apstock*c['appliance_border_CU'],household_stock_is_operator_capital=False,
                inventory_working_asset_CU=border*c['inventory_days']/365,inventory_tonnes=mass*c['inventory_days']/365,
                household_shopping_hours=tx*c['household_shopping_hours_transaction'],household_shopping_passenger_km=tx*c['household_shopping_return_km'],household_trips_are_subset_of_bus_km=True,
                bus_passenger_km=ppkm,bus_vehicle_km=buskm,bus_fleet=fleet,goods_haul_vehicle_km=haulkm,
                electricity_GWh=sum(E.values()),electricity_provisionally_replaces_PS_private10GWh=True,
                public_building60_bus_depot_overlap_resolved=False,
                final_goods_plus_named_service_subtotal_CU=border+sum(x['named_annual_cost_subtotal_CU'] for x in producers),
                actual_basket_adequacy_or_price_index=None,actual_job_cohort_matches=None,actual_cash_or_foreign_source=None,
                unresolved=['Household choice/additional needs and discretionary goods','Land/title/vintage/finance/insurance','Full electricity and upstream supplier prices/capacity','Actual route, peak, home delivery and unpaid household time','Matched ownership/subsidy and old/new bus scope','Other initial/specialist suppliers and actual product quality'])
