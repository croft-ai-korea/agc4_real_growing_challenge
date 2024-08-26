import sys
sys.path.append('./')

import pandas as pd
import numpy as np
import os
import copy
import json
import yaml 
import psycopg2
from random import random
from datetime import datetime, timedelta
from psycopg2.extras import execute_values
from aaaa.farm_math import datetime_to_int, fruit_price, get_simulation_setpoint , get_simulation_setpoint_light_time
from a_util.manual_parameter import heatingTemp, hours_light, max_iglob, ventOffset, endTime, intensity
from a_util.simulator.greenhouse import Greenhouse, get_day_data
from a_util.simulator.simulator import send_server, json_parsing, sim_greenhouse, get_endDate_from_output
from a_util.simulator.simulator import modify_temperature, modify_intensity, modify_hours_light
from a_util.simulator.simulator import modify_temperature_random, modify_intensity_random, modify_hours_light_random
from a_util.simulator.simulator import convert_key_from_start_date, get_realtime_data, get_reference_table
from a_util.simulator.simulator import action_table_to_server_format, generate_density_from_string
from a_util.db.db_util import create_table_if_not_exists, db_drop_table_if_exists, db_data_insert
from a_util.db.schema import create_simulation_table_query, simulation_result_columns_to_insert
from a_util.db.schema import simulation_result_insert_query, simulation_forcast_insert_query
from aaaa.per_day_simul import per_day 
from a_util.service.letsgrow_service_simul import LetsgrowService


USE_NEW_TABLE = True

def run_simulator():    
    control_json_path = "a_util/Par_Out_reference_control.json"
    Par_Out_reference = "a_util/Par_Out_reference.json"
    
    ## make strategy
    config_path = "./a_util/env/config.yaml"

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        
    start_datetime = config['start_date']
    end_datetime = config['end_date']    
    
    if USE_NEW_TABLE:
        db_drop_table_if_exists(table_name = 'simulation')
        create_table_if_not_exists(table_name = 'simulation', query=create_simulation_table_query)
                
        reference_csv_path = "./a_util/reference.csv"        
        df = pd.read_csv(reference_csv_path)
        column_rename = {
            "DateTime" : "time",
            "common.Iglob.Value":"fc_radiation_5min",
            "common.Tout.Value":"fc_temperature_5min",
            "common.RHout.Value":"fc_rh_5min",
            "common.Windsp.Value":"fc_wind_speed_5min",
        }         
        df.rename(columns=column_rename, inplace=True)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        df = df.resample('5T').interpolate(method='linear')
        df.reset_index(inplace=True)
        df = df[(df['time']>=start_datetime) & (df['time'] <= end_datetime)]
        df = df[["time","fc_radiation_5min","fc_temperature_5min","fc_rh_5min","fc_wind_speed_5min"]]
        
        db_data_insert(df=df, query=simulation_forcast_insert_query)
        
    per_day(config=config)    

    lg_service = LetsgrowService()
    lg_simul_data = lg_service.data_from_db(config['start_date'], config['end_date'])
                
    ### Initialize and set up the greenhouse
    greenhouse_control = Greenhouse(logging_enabled=False)
    greenhouse_control.initialize_devices(control_json_path = control_json_path)

    save_folder = "./temp/"
    episode = str(datetime.now().strftime("%d_%H.%M.%f")[:11])
    response_csv_path = os.path.join(save_folder, f"Par_Out_{episode}.csv")


    ### modify setting point
    greenhouse_control.endDate = end_datetime.strftime("%d-%m-%Y")
    # greenhouse_control.endDate = "31-12-2023"
    startDate = start_datetime.strftime("%d-%m-%Y")
    
    greenhouse_control.startDate = startDate
    greenhouse_control.plantDensity = config['plant_density']

    ### set weather data and analysis 
    reference = json_parsing(response_json_path = Par_Out_reference)
    greenhouse_control.load_weather_data_and_analysis(reference)

    # greenhouse_control.device_illumination['lmp1'].intensity = 250
    
    heating_setpoint = get_simulation_setpoint(lg_simul_data['sp_heating_temp_setpoint_5min'],config['start_date'])
    greenhouse_control.device_setpoints['setpoints'].temp.heatingTemp = convert_key_from_start_date(heating_setpoint, startDate)
    
    vent_offset = get_simulation_setpoint(lg_simul_data['sp_vent_ilation_temp_setpoint_5min']-lg_simul_data['sp_heating_temp_setpoint_5min'],config['start_date'])
    greenhouse_control.device_setpoints['setpoints'].temp.ventOffset = convert_key_from_start_date(vent_offset, startDate)
    
    greenhouse_control.device_illumination['lmp1'].intensity = config['base_LED_umol']
    hours_light_temp, end_time = get_simulation_setpoint_light_time(lg_simul_data['sp_value_to_isii_1_5min'])
    
    greenhouse_control.device_illumination['lmp1'].end_time = end_time
    # greenhouse_control.device_illumination['lmp1'].hours_light = convert_key_from_start_date(hours_light, startDate)
    greenhouse_control.device_illumination['lmp1'].hours_light = hours_light_temp
    
    # greenhouse_control.device_illumination['lmp1'].intensity = convert_key_from_start_date(heating_setpoint, startDate)
    # heatingTemp = copy.deepcopy(greenhouse_control.device_setpoints['setpoints'].temp.heatingTemp)
    # intensity = copy.deepcopy(greenhouse_control.device_illumination['lmp1'].intensity)
    # max_iglob = copy.deepcopy(greenhouse_control.device_illumination['lmp1'].max_iglob)
    # hours_light = copy.deepcopy(greenhouse_control.device_illumination['lmp1'].hours_light)

    ### reference data
    parameters = greenhouse_control.export_all_devices(set_start_date = True)
    reference_json_path = "ref.json"
    result_json = send_server(parameters=parameters,response_json_save_path=reference_json_path)
    df = json_parsing(response_json_path=reference_json_path, response_csv_path = response_csv_path)
    
    df.index.name = "time"
    column_rename = {
        "comp1.Air.T":"temperature_greenhouse_5min",
        "comp1.Air.RH":"rh_greenhouse_5min",
        "comp1.Air.ppm":"co2_greenhouse_ppm_5min",
        "common.Iglob.Value":"outside_radiation_5min",
        "common.Tout.Value":"outside_temperature_5min",
        "common.RHout.Value":"outside_rh_5min",
        "common.Windsp.Value":"outside_wind_speed_5min",
        "comp1.PARsensor.Above":"par_sensor_above",
        "comp1.TPipe1.Value": "tpipe", 
        "comp1.ConPipes.TSupPipe1": "conpipes_tsuppipe",
        "comp1.PConPipe1.Value": "pconpipe",
        "comp1.ConWin.WinLee": "vent_lee_5min",
        "comp1.ConWin.WinWnd": "vent_wind_5min",
        "comp1.Setpoints.SpHeat": "sp_heating_temp_setpoint_5min",
        "comp1.Setpoints.SpVent": "sp_vent_ilation_temp_setpoint_5min",
        "comp1.Scr1.Pos": "energy_curtain_5min",
        "comp1.Scr2.Pos": "blackout_curtain_5min",
        "comp1.Lmp1.ElecUse": "lmp_elecuse",
        "comp1.McPureAir.Value": "mc_pure_air",
        "comp1.Setpoints.SpCO2": "sp_co2_setpoint_ppm_5min",
        "comp1.Growth.FruitFreshweight": "fruit_fresh_weight",
        "comp1.Growth.DVSfruit": "dvs_fruit",
        "comp1.Growth.DryMatterFract": "dry_matter_fract",
        "comp1.Growth.CropAbs": "crop_abs",
        "comp1.Growth.PlantDensity": "sp_plantdensity",
        "common.ElecPrice.PeakHour": "elec_price_peakhour",
        "comp1.Growth.WaterUsePerPot": "water_supply_minutes_5min", 
        "comp1.Growth.RedFruitsWeight": "red_fruits_weight"
    }

    df.rename(columns=column_rename, inplace=True)
    df.index = pd.to_datetime(df.index)
    df.loc[df.index[0]-timedelta(hours=1)] = np.array(df.iloc[0])
    df = df.sort_index()

    df['fixed_costs'] = np.nan
    df['fixed_costs_accumulation'] = np.nan
    df['fixed_greenhouse_costs'] = np.nan
    df['fixed_co2_costs'] = np.nan
    df['fixed_lamp_costs'] = np.nan
    df['fixed_screen_costs'] = np.nan
    # df['fixed_spacing_system_costs'] = np.nan
    df['variable_costs_day_sum'] = np.nan
    df['variable_costs_accumulation'] = np.nan
    df['variable_electricity_costs'] = np.nan
    df['variable_electricity_costs_day_sum'] = np.nan
    df['variable_heating_costs'] = np.nan
    df['variable_heating_costs_day_sum'] = np.nan
    df['variable_co2_costs'] = np.nan
    df['variable_co2_costs_day_sum'] = np.nan
    df['gains'] = np.nan
    df['net_profit'] = np.nan
    df['total_cost'] = np.nan
    
    df['net_profit_per_year'] = np.nan

    df = df.resample('5T').interpolate(method='linear')

    start_date = df.index[0]

    DosingCapacity = 100
    lamp_max_intensity = 100   # 질문사항
    num_screens = 2

    fixed_costs_accum = 0
    variable_costs_accum = 0 

    electric_coeff = np.array([0.2]*288)
    electric_coeff[datetime_to_int(datetime(2024,1,1,7,0,0)):datetime_to_int(datetime(2024,1,1,23,0,0))] = 0.3 

    coeef = 365

    while True:
        filtered_index = (df.index>=start_date)&(df.index<start_date+timedelta(days=1))
        filtered_index_from_transplanting = (df.index<start_date+timedelta(days=1))&(df.index.hour==23)&(df.index.minute==55)
        df_today = df[filtered_index]
        if len(df_today) < 288:
            break
        
        df.loc[filtered_index,'fixed_greenhouse_costs'] = 15.0/365
        df.loc[filtered_index,'fixed_co2_costs'] = DosingCapacity*0.015/365
        df.loc[filtered_index,'fixed_lamp_costs'] = lamp_max_intensity*0.07/365
        df.loc[filtered_index,'fixed_screen_costs'] = num_screens*1/365
        df.loc[filtered_index,'fixed_costs'] = df.loc[filtered_index,'fixed_greenhouse_costs'] + \
                                            df.loc[filtered_index,'fixed_co2_costs'] + \
                                            df.loc[filtered_index,'fixed_lamp_costs'] + \
                                            df.loc[filtered_index,'fixed_screen_costs']
        
        fixed_costs_accum += df.loc[filtered_index,'fixed_costs'][-1]    
        df.loc[filtered_index,'fixed_costs_accumulation'] = fixed_costs_accum
        
        # electricity cost
        # full capacity one hour -> 0.0625 
        # full capacity 5 min -> 0.00521
        # "lmp_elecuse" will convert to "sp_value_to_isii_1_5min"
        df.loc[filtered_index, 'variable_electricity_costs'] = 0.00521*(df.loc[filtered_index,'lmp_elecuse']/100)*electric_coeff
        df.loc[filtered_index, 'variable_electricity_costs_day_sum'] = df.loc[filtered_index, 'variable_electricity_costs'].cumsum()
            
        # heating cost
        # 0.09 per kWH    
        # 0.0075 per 5min
        Ppiperail = (df.loc[filtered_index, 'tpipe'] - df.loc[filtered_index, 'temperature_greenhouse_5min'])*2
        Ppiperail[Ppiperail<0] = 0
        df.loc[filtered_index, 'variable_heating_costs'] = (Ppiperail/1000)*0.0075
        df.loc[filtered_index, 'variable_heating_costs_day_sum'] = df.loc[filtered_index, 'variable_heating_costs'].cumsum()
        
        # co2 cost
        # 0.3 per kg
        df.loc[filtered_index, 'variable_co2_costs'] = df.loc[filtered_index, 'mc_pure_air']*5*60*0.3
        df.loc[filtered_index, 'variable_co2_costs_day_sum'] = df.loc[filtered_index, 'variable_co2_costs'].cumsum()
        
        df.loc[filtered_index, 'variable_costs_day_sum'] = df.loc[filtered_index, 'variable_electricity_costs_day_sum'] + \
                                    df.loc[filtered_index, 'variable_heating_costs_day_sum'] + \
                                    df.loc[filtered_index, 'variable_co2_costs_day_sum']
                                    
                                    
        df.loc[filtered_index, 'variable_costs_accumulation'] = df.loc[filtered_index, 'variable_costs_day_sum'] + variable_costs_accum
        
        variable_costs_accum = df.loc[filtered_index, 'variable_costs_accumulation'][-1]
        
        # total_cost
        plant_density_inverse = 1/df.loc[filtered_index_from_transplanting, 'sp_plantdensity']
        variable_cost = df.loc[filtered_index_from_transplanting, 'variable_costs_day_sum']
        fixed_cost = df.loc[filtered_index_from_transplanting, 'fixed_costs']
        D = len(plant_density_inverse)
        df.loc[filtered_index,'total_cost'] =  sum((variable_cost+fixed_cost)*plant_density_inverse)/sum(plant_density_inverse)
            
        start_date += timedelta(days=1)
        
        # total_gain
        Pd = fruit_price(df.loc[filtered_index,'red_fruits_weight'][-1])    
        df.loc[filtered_index,'gains'] = Pd / sum(plant_density_inverse)
        
            # 추가
        gain_value = df.loc[filtered_index, 'gains'][-1] * coeef
        if gain_value < 0:
            gain_value = 0

        # net profit
        df.loc[filtered_index,'net_profit'] = df.loc[filtered_index,'gains'] - df.loc[filtered_index,'total_cost']
        df.loc[filtered_index,'net_profit_per_year'] = df.loc[filtered_index,'net_profit'] * 365       

        # print("net profit : ", df.loc[filtered_index,'net_profit'][-1]*coeef, "gain : ", df.loc[filtered_index,'gains'][-1]*coeef, "total cost : ", df.loc[filtered_index,'total_cost'][-1]*coeef)
        
        net_profit_value = df.loc[filtered_index,'net_profit'][-1]*coeef - df.loc[filtered_index, 'gains'][-1]*coeef - gain_value 
        print("net profit : ", net_profit_value, "gain : ", gain_value, "total cost : ", df.loc[filtered_index,'total_cost'][-1]*coeef)
    

    df.reset_index(inplace=True)
    db_data_insert(df=df[simulation_result_columns_to_insert], query=simulation_result_insert_query)


if __name__ == "__main__":
    ## do simulator
    run_simulator()
    
