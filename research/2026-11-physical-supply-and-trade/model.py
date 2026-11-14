"""Joined authored quantities, work, power and named FX; no national GDP closure."""
from pathlib import Path
import json,math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def posts(hours,H,pay=30000):
    n=math.ceil(hours/H)
    return dict(task_or_coverage_hours=hours,annual_post_bound=n,ordinary_payroll_CU=n*pay,actual_qualified_shift=None)


def food_case(c,pop,H,kind):
    if kind not in ['resource_fit_mixed','import_heavy','irrigated_mixed']:raise ValueError('Unsupported food path')
    if not 0<c['packing_yield']<=1 or not 0<c['distribution_yield']<=1:raise ValueError('Missing/invalid food yield')
    fy=c['packing_yield'];dy=c['distribution_yield'];rows=[]
    recipes=c['irrigated_rival'] if kind=='irrigated_mixed' else c['crop_recipes']
    field=area=work=netwater=dompacked=border=received=side=foodFX=lost_importFX=reserve=reserveFX=0
    for a in c['commodities']:
        share=a['import_heavy_domestic_share'] if kind=='import_heavy' else a['mixed_domestic_share']
        if not 0<=share<=1 or a['received_kg_person_year']<0:raise ValueError('Invalid commodity share/quantity')
        rec=pop*a['received_kg_person_year']/1000;dom=rec*share;imp=(rec-dom)/dy
        packed=dom/dy;gross=packed/fy if dom else 0
        land=hours=water=0
        if dom:
            if a['id'] not in recipes:raise ValueError('Unsupported domestic commodity recipe: '+a['id'])
            p=recipes[a['id']]
            if p['yield_t_ha']<=0:raise ValueError('Nonpositive crop yield')
            land=gross/p['yield_t_ha'];hours=land*p['work_hours_ha'];water=land*p['net_irrigation_m3_ha']
        stock=rec/dy*c['reserve_days']/365 if a['id'] in c['reserve_goods'] else 0
        quote=a['border_quote_CU_tonne']
        rows.append(dict(id=a['id'],received_t=rec,domestic_received_t=dom,border_import_t=imp,
                         packed_domestic_t=packed,gross_domestic_t=gross,cropped_ha=land,
                         field_hours=hours,net_irrigation_m3=water,reserve_t=stock))
        received+=rec;dompacked+=packed;field+=gross;border+=imp;area+=land;work+=hours;netwater+=water
        side+=gross-packed;foodFX+=imp*quote;lost_importFX+=dom*c['harvest_loss_fraction']/dy*quote
        reserve+=stock;reserveFX+=stock*quote
    holding=area/(1-c['rotation_land_fraction']);cover=holding-area;work+=cover*c['cover_hours_ha']
    bulk=dompacked+border
    tonnekm=dompacked*c['domestic_tonne_km']+border*c['import_tonne_km']+bulk*c['final_tonne_km']
    vehiclekm=tonnekm/c['truck_carried_tonnes']*(1+c['empty_return_km_fraction']);trips=2*bulk/c['truck_carried_tonnes']
    driving=vehiclekm/c['truck_speed_km_h']+trips*c['driver_handling_hours_trip']
    meals=c['school_meals']+c['care_hospital_meals']+c['custody_bed_days']*c['custody_meals_day']
    public=meals*c['meal_ingredient_kg']/1000
    if public>received:raise ValueError('Public ingredients cannot exceed national receipt')
    roles=dict(field_and_cover=posts(work,H),processing_packing=posts(field*c['processing_hours_gross_tonne'],H),
               bulk_handling=posts(bulk*c['bulk_handling_hours_tonne'],H),freight=posts(driving,H),
               retail_coverage=posts(c['retail_outlets']*c['retail_daily_hours']*365*c['retail_simultaneous_people'],H))
    farmwater=netwater/c['field_irrigation_efficiency']
    # Very favorable harvest bound: no scheduled leave/learning during peak.
    peak_person_hours=c['harvest_scheduled_weeks']*(32-2.5)*.9
    return dict(kind=kind,commodities=rows,received_t=received,domestic_received_t=dompacked*dy,
                border_import_t=border,gross_crop_t=field,packed_domestic_t=dompacked,packing_side_stream_t=side,
                bulk_food_t=bulk,distribution_loss_t=bulk-received,cropped_ha=area,holding_ha=holding,
                net_irrigation_m3=netwater,farm_customer_water_m3=farmwater,field_cover_hours=work,
                roles=roles,named_ordinary_payroll_CU=sum(x['ordinary_payroll_CU'] for x in roles.values()),
                public_ingredient_t=public,other_received_t=received-public,public_meals_are_subset=True,
                household_preparation_time=None,vehicle_km=vehiclekm,diesel_litres=vehiclekm*c['diesel_litres_vehicle_km'],
                food_border_bill_CU=foodFX,diesel_import_quote_CU=vehiclekm*c['diesel_litres_vehicle_km']*c['diesel_landed_CU_litre'],
                reserve_opening_t=reserve,reserve_opening_import_quote_CU=reserveFX,
                reserve_annual_spoil_t=reserve*c['reserve_spoil_fraction'],reserve_annual_spoil_import_CU=reserveFX*c['reserve_spoil_fraction'],
                normal_rotation_is_not_extra_food=True,seasonal_storage_additional_requirement=None,
                harvest_loss_received_t=dompacked*dy*c['harvest_loss_fraction'],
                harvest_loss_additional_border_t=dompacked*c['harvest_loss_fraction'],harvest_loss_extra_import_CU=lost_importFX,
                harvest_favorable_peak_people_bound=math.ceil(work*c['harvest_work_fraction']/peak_person_hours),
                harvest_normal32_no_overtime=True,
                harvest_40total_paid_overtime_people_bound=math.ceil(work*c['harvest_work_fraction']/(c['harvest_scheduled_weeks']*(40-2.5)*.9)),
                actual_peak_premiums_or_qualification=None,
                food_electricity_GWh=(field*c['processing_MWh_gross_tonne']+bulk*c['cold_chain_MWh_bulk_tonne'])/1000+farmwater*c['irrigation_kWh_m3']/1e6,
                nutritional_or_geographic_adequacy=None,actual_labor_or_source=None)


def water_case(c,pop,farm,H,mode):
    if mode not in ['desal','bulk']:raise ValueError('Unsupported water source')
    if not 0<c['catchment_to_header_product_yield_hypothesis']<=1 or not 0<=c['repaired_network_loss']<1:raise ValueError('Invalid source yield/loss')
    other=pop*c['household_litres_person_day']*365/1000+c['public_m3_year']+c['authored_nonfarm_commercial_m3_year']
    D=other+farm;sewer=other*c['other_return']+farm*c['farm_return'];recovered=sewer*c['treatment_recovery']
    reuse=min(c['reuse_target_m3_year'],recovered,min(c['reuse_farm_max_m3_year'],farm)+c['reuse_industry_max_m3_year'])
    fresh=D-reuse;header=fresh/(1-c['repaired_network_loss']);networkloss=header-fresh
    raw_available=c['raw_catchment_m3_year']-c['ecological_m3_year']-c['annual_standby_flow_exclusion_m3']
    catch=raw_available*c['catchment_to_header_product_yield_hypothesis'];gap=max(0,header-catch)
    normalcap=c['desal_trains']*c['desal_each_m3_day']*365*c['desal_available_fraction']
    oneoutcap=(c['desal_trains']-1)*c['desal_each_m3_day']*c['desal_available_fraction']
    sourcecapvol=normalcap if mode=='desal' else c['bulk_suppliers']*c['bulk_each_m3_day']*365*c['bulk_available_fraction']
    source_oneout_day=oneoutcap if mode=='desal' else (c['bulk_suppliers']-1)*c['bulk_each_m3_day']*c['bulk_available_fraction']
    usable=c['potable_tanks']*c['tank_each_gross_m3']*c['tank_usable_fraction'];one_tank=(c['potable_tanks']-1)*c['tank_each_gross_m3']*c['tank_usable_fraction']
    newsource_outage=gap/365*c['outage_days'];allsource_outage=header/365*c['outage_days']
    additional_energy=gap*(c['desal_kWh_product_m3'] if mode=='desal' else c['bulk_unloading_kWh_m3'])
    power=(header*c['fresh_pump_kWh_header_m3']+sewer*c['secondary_kWh_sewer_m3']+reuse*c['reuse_kWh_reused_m3']+additional_energy)/1e6
    commoncap=c['reuse_annual_capacity_m3']*c['reuse_capital_CU_annual_m3']+c['leak_project_capital_CU']+c['potable_tanks']*c['tank_each_gross_m3']*c['tank_capital_CU_m3']
    sourcecap=c['desal_trains']*c['desal_each_m3_day']*365*c['desal_capital_CU_annual_m3'] if mode=='desal' else c['bulk_terminal_capital_CU']
    roles=dict(reuse_process=posts(8760,H,60000),reuse_lab=posts(2000,H,60000),reuse_mechanical=posts(2000,H),independent_review=posts(800,H,60000))
    if mode=='desal':
        roles.update(source_process=posts(c['desal_trains']*8760,H,60000),source_lab=posts(1500,H,60000),source_mechanical=posts(4500,H))
    else:roles.update(source_process=posts(8760,H,60000),source_lab=posts(1500,H,60000),source_mechanical=posts(1000,H))
    parts=reuse*c['reuse_parts_CU_m3']+c['potable_tanks']*c['tank_each_gross_m3']*c['tank_maintenance_CU_gross_m3']+c['meter_testing_CU']
    directFX=gap*(c['desal_parts_CU_product_m3'] if mode=='desal' else c['bulk_landed_CU_m3'])
    importcap=commoncap*c['common_capital_import_fraction']+sourcecap*(c['desal_capital_import_fraction'] if mode=='desal' else c['bulk_terminal_import_fraction'])
    return dict(mode=mode,delivered_customer_m3=D,nonfarm_customer_m3=other,farm_customer_m3=farm,sewer_received_m3=sewer,
                recovered_m3=recovered,reused_m3=reuse,final_discharge_m3=recovered-reuse,treatment_loss_m3=sewer-recovered,
                customer_consumption_m3=D-sewer,fresh_delivered_m3=fresh,fresh_header_m3=header,network_loss_m3=networkloss,
                protected_catchment_available_m3=catch,raw_after_exclusions_m3=raw_available,
                modeled_additional_catchment_treatment_loss_m3=raw_available-catch,actual_catchment_quality_or_treatment=None,additional_source_required_m3=gap,normal_desal_capacity_m3=normalcap,
                normal_desal_volume_bound_pass=(gap<=normalcap),normal_source_capacity_m3=sourcecapvol,
                normal_source_volume_bound_pass=(gap<=sourcecapvol),one_source_out_daily_deficit_m3=max(0,gap/365-source_oneout_day),
                one_train_out_daily_deficit_m3=max(0,gap/365-oneoutcap),
                tank_usable_m3=usable,one_area_tank_lost_usable_m3=one_tank,
                potable_initial_fill_m3=c['potable_tanks']*c['tank_each_gross_m3'],
                additional_initial_fill_process_GWh=c['potable_tanks']*c['tank_each_gross_m3']*(c['desal_kWh_product_m3'] if mode=='desal' else c['bulk_unloading_kWh_m3'])/1e6,
                reuse_buffer_usable_m3=c['reuse_buffer_nominal_m3']*c['reuse_buffer_usable_fraction'],
                reuse_buffer_days=(c['reuse_buffer_nominal_m3']*c['reuse_buffer_usable_fraction']/(reuse/365) if reuse else None),
                seawater_intake_m3=(gap/c['desal_recovery_fraction'] if mode=='desal' else None),
                brine_m3=(gap/c['desal_recovery_fraction']-gap if mode=='desal' else None),new_source_14day_interruption_m3=newsource_outage,
                new_source_stock_volume_bound_pass=(usable>=newsource_outage),one_tank_lost_stock_pass=(one_tank>=newsource_outage),
                all_fresh_source_14day_requirement_m3=allsource_outage,all_source_stock_pass=(usable>=allsource_outage),
                drought20_additional_source_m3=max(0,header-(.8*c['raw_catchment_m3_year']-c['ecological_m3_year']-c['annual_standby_flow_exclusion_m3'])*c['catchment_to_header_product_yield_hypothesis']),
                electricity_GWh=power,named_new_asset_quote_CU=commoncap+sourcecap,named_asset_import_quote_CU=importcap,
                common_current_parts_quote_CU=parts,source_direct_import_quote_CU=directFX,
                bulk_retainer_quote_CU=(c['bulk_suppliers']*c['bulk_each_m3_day']*365*c['bulk_retainer_CU_annual_nameplate_m3'] if mode=='bulk' else 0),new_roles=roles,
                new_ordinary_payroll_CU=sum(x['ordinary_payroll_CU'] for x in roles.values()),
                actual_quality_seasons_location_fuel_or_source=None,full_source_qualification=False)


def outage(c,extra,wind,links_lost):
    demand=c['stress_bus_demand_MW'];local=sum(c['firm_units_net_MW'])+(c['third_firm_net_MW'] if extra else 0)
    imports=sum(c['import_links_net_MW'][links_lost:]);available=local+imports+wind
    deficit=max(0,demand-available);battery_power=min(deficit,c['battery_MW']);duration=c['stress_duration_h']
    battery_energy=min(battery_power*duration,c['battery_usable_AC_MWh'])
    return dict(extra_firm=extra,wind_MW=wind,import_links_lost=links_lost,available_net_bus_MW=available,
                deficit_before_storage_MW=deficit,immediate_unserved_MW=max(0,deficit-c['battery_MW']),
                battery_duration_h=(c['battery_usable_AC_MWh']/battery_power if battery_power else None),
                ideal_unserved_MWh=deficit*duration-battery_energy,static_without_storage_pass=(deficit==0),
                fast_response_or_frequency_qualified=False)


def power_case(c,pop,food,water,export_GWh=0):
    H=c['energized_reference_dwellings']*c['home_MWh_dwelling_year']/1000+pop*c['space_comfort_MWh_person_year']/1000
    end=H+c['retained_public_building_GWh']+c['small_private_sites_GWh']+food['food_electricity_GWh']+water['electricity_GWh']+export_GWh
    battery_discharge=c['battery_usable_AC_MWh']*c['battery_annual_full_cycles']/1000
    battery_charge=battery_discharge/c['battery_round_trip_efficiency'];battery_loss=battery_charge-battery_discharge
    bus=end/(1-c['distribution_loss']);supply=bus+battery_loss
    local=c['solar_available_GWh']+c['wind_available_GWh']+c['domestic_firm_scheduled_GWh']
    imports=max(0,supply-local);fuel=c['domestic_firm_scheduled_GWh']/c['domestic_fuel_efficiency']
    return dict(home_electricity_GWh=H,named_end_use_GWh=end,named_bus_use_GWh=bus,battery_discharge_GWh=battery_discharge,
                battery_charge_GWh=battery_charge,battery_loss_GWh=battery_loss,named_supply_needed_GWh=supply,
                local_annual_hypothesis_GWh=local,annual_import_required_GWh=imports,annual_import_offer_GWh=c['annual_import_offer_GWh'],
                annual_import_volume_bound_pass=(imports<=c['annual_import_offer_GWh']),renewable_surplus_not_assumed_export_GWh=max(0,local-supply),
                electricity_import_quote_CU=imports*1000*c['import_quote_CU_MWh'],domestic_generation_imported_fuel_GWh_thermal=fuel,
                generation_fuel_import_quote_CU=fuel*1000*c['fuel_landed_CU_MWh_thermal'],generation_direct_CO2_t=fuel*1000*c['authored_fuel_tonnes_CO2_MWh_thermal'],
                manufacturing_mobility_and_other_load_GWh=None,actual_hourly_grid_or_fuel_qualification=None,full_national_energy_total=None,
                initial_power_assets_and_land_CU=None,annual_capacity_and_complete_operating_cost_CU=None,
                third_firm_named_capital_quote_CU=c['extra_firm_capital_CU'],third_firm_named_nonfuel_quote_CU=c['extra_firm_annual_nonfuel_CU'],
                stress=[outage(c,e,w,k) for e in [False,True] for w in c['stress_wind_MW'] for k in [1,2]],
                annual_energy_implies_adequacy=False,additional_instant_response_needed_beyond_battery_MW=c['fast_other_response_required_MW'])


def calculate(c=None):
    c=c or json.loads((HERE/'inputs.json').read_text());tw=json.loads((ROOT/c['tw_results']).read_text());H=tw['cases'][0]['calendar']['deployable_task_hours']
    cases=[]
    for kind in ['resource_fit_mixed','import_heavy','irrigated_mixed']:
        food=food_case(c['food'],c['population'],H,kind)
        for mode in ['desal','bulk']:
            water=water_case(c['water'],c['population'],food['farm_customer_water_m3'],H,mode)
            power=power_case(c['power'],c['population'],food,water)
            minimum=food['food_border_bill_CU']+food['reserve_annual_spoil_import_CU']+food['diesel_import_quote_CU']+water['source_direct_import_quote_CU']+water['bulk_retainer_quote_CU']+power['electricity_import_quote_CU']+power['generation_fuel_import_quote_CU']
            cases.append(dict(id=kind+'/'+mode,food=food,water=water,power=power,named_recurring_FX_quote_CU=minimum,
                              named_first_asset_and_food_stock_FX_CU=water['named_asset_import_quote_CU']+food['reserve_opening_import_quote_CU'],
                              other_operating_and_initial_import_need=None,actual_export_receipts=None,credited_verified_export_source_CU=0,
                              named_imports_not_funded=True))
    o=c['export_order'];work=o['billable_hours']/o['billable_fraction'];n=math.ceil(work/H);gross=o['billable_hours']*o['unit_price_CU_hour']
    export=dict(status=o['status'],gross_conditional_receipt_CU=gross,actual_received_FX=None,credited_actual_source_CU=0,
                total_human_task_hours=work,annual_professional_post_bound=n,ordinary_payroll_CU=n*o['professional_annual_pay_CU'],
                extra_annual_import_quote_CU=o['recurring_imported_services_CU'],named_domestic_premises_CU=o['named_domestic_premises_CU'],
                extra_electricity_GWh=o['electricity_MWh']/1000,payment_delay_days=o['payment_delay_days'],
                pre_receipt_working_capital_and_qualification=None,publicly_available_share_of_returns=None)
    return dict(edition=92,status='Joined authored essential supply subsets; no whole-country physical, fiscal, FX or adequacy pass',
                task_hours_per_post=H,cases=cases,conditional_export_order=export,actual=c['excluded_actuals'])


if __name__=='__main__':(HERE/'results.json').write_text(json.dumps(calculate(),indent=2)+'\n')
