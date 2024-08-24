import sys
sys.path.append('./')

from datetime import timedelta, datetime
import pandas as pd
import numpy as np
from a_util.env.real_env import GreenHouseInput, GreenHouseOutput
from aaaa.farm_math import sun_cal, get_DLI, datetime_to_int, get_peakTime, calc_irrigation_time_with_DLI
import json
import os

def base_strategy(_in: GreenHouseInput, _out: GreenHouseOutput):
    """  
    _in : 상수의 느낌
    _out:
        setpoint :
        global_info : 다른 strategy 함수와 공유하는 변수
    """
    """
    heating/venting temp setting
    - with light max 30 degree 
    - setting
      - veg 
        - light : heat 19, vent 20
        - no light : heat 18, vent 19
      - generative
        - light : heat 21, vent 22
        - no light : heat 17, vent 18  
    """

    _out.setting_point['sp_heating_temp_setpoint_5min'] = [18]*288
    _out.setting_point['sp_heating_temp_setpoint_5min'][_in.rise_time_int:_in.set_time_int] = 19
    _out.setting_point['sp_vent_ilation_temp_setpoint_5min'] = _out.setting_point['sp_heating_temp_setpoint_5min']+1

    """
    energy screen 
      [october 10/10]
        use below 100W/m2 radiation - 90%
        above 500W/m2 radiation - 75%
      [november 11/2]
        use below 200W/m2 radiation - 90%
        above 400W/m2 radiation - 75%
    """
    
    # if (_in.now > datetime(2024,10,10,0,0,0)) and (_in.now < datetime(2024,11,2,0,0,0)):
    if _in.now < datetime(2024,11,2,0,0,0):         ## 임시 테스트용
        _out.setting_point['sp_energy_screen_setpoint_5min'] = [0]*288
        _out.setting_point['sp_energy_screen_setpoint_5min'][_in.indoor_env['fc_radiation_5min']<100] = 90
        _out.setting_point['sp_energy_screen_setpoint_5min'][_in.indoor_env['fc_radiation_5min']>500] = 75
    if _in.now >= datetime(2024,11,2,0,0,0):
        _out.setting_point['sp_energy_screen_setpoint_5min'] = [0]*288
        _out.setting_point['sp_energy_screen_setpoint_5min'][_in.indoor_env['fc_radiation_5min']<200] = 90
        _out.setting_point['sp_energy_screen_setpoint_5min'][_in.indoor_env['fc_radiation_5min']>400] = 75        
    
    """
    led setting
    - Daily light sum
      - minimal 10
      - no max yet 18
      - max capacity 500
    - eletricity price
      - peak 7:00-23:00: 0.3 euro per kwh
      - low 23:00-7:00: 0.2 euro per kwh
      
      6 hour rest
      18 photo period
      
    
    set : 100umol
    set DLI = 15
      
    """
    _out.setting_point['sp_value_to_isii_1_5min'] = [0]*288
    DLI_need = _in.config['base_target_DLI'] - _in.expected_DLI
    if DLI_need > 0:
        LED_time_per_5min = ((DLI_need * 1e6) / (_in.config['base_LED_umol']*60))//5
        
        filtered_by_threshold = _in.indoor_env['fc_radiation_5min'][_in.indoor_env['fc_radiation_5min']>_in.config['base_target_DLI']]
        if len(filtered_by_threshold) > 0:
            led_end_time_int = datetime_to_int(filtered_by_threshold.index[0])
            led_start_time_int = int(led_end_time_int-LED_time_per_5min)          
        else:
            led_center_time_int = get_peakTime(_in.indoor_env['fc_radiation_5min'])  
            led_start_time_int = led_center_time_int - LED_time_per_5min//2
            led_end_time_int = led_center_time_int + LED_time_per_5min//2
            
        if led_start_time_int < datetime_to_int(datetime(2000,1,1,2,0,0)):
            led_start_time_int = datetime_to_int(datetime(2000,1,1,2,0,0))  
        if led_end_time_int > datetime_to_int(datetime(2000,1,1,11,0,0)):
            led_end_time_int = datetime_to_int(datetime(2000,1,1,11,0,0))
        
        _out.setting_point['sp_value_to_isii_1_5min'][led_start_time_int:led_end_time_int] = _in.config['base_LED_umol']            
     
    """
    screen setting
    at night, if led is on, then use blackout screen
    
    """
    _out.setting_point['sp_blackout_screen_setpoint_5min'] = [0]*288
    
    _out.setting_point['sp_blackout_screen_setpoint_5min'][_out.setting_point['sp_value_to_isii_1_5min']>0] = 95
    _out.setting_point['sp_blackout_screen_setpoint_5min'][_in.rise_time_int:_in.set_time_int] = 0


    """
    min_vent_position setting
    
    
    """

    _out.setting_point['sp_leeside_minvent_position_setpoint_5min'] = [5]*288


    """
    net_pipe_minimum setting
      night : temp ok not use
      get rid of humidity -> start heating -> maintain min temp some value
      small capacity..
      if humidity is to high:
          during september
                      
    """   
    _out.setting_point['sp_net_pipe_minimum_setpoint_5min'] = [0]*288

    """
    co2 setting
        - 1st stage : 550,  4 Sep ~ 18 Sep, 12 days after transplanting (48/m2) - just leaves
        - 2nd stage : 550,  18 Sep ~ 22 Sep, 16 days (36/m2) - first flowering
        - 3rd stage : 800,  22 Sep ~ 29 Sep, 23 days (25/m2) - first fruiting, generative growth
        - 4th stage : 800,  29 Sep - 9 Oct (lost days…)
        - 5th stage : 800,  9 October - 9 November, 33 days (20/m2)
      after fruit stage :  more than 1000 correlation vent
      
      
    """
    _out.setting_point['sp_co2_setpoint_ppm_5min']  = 300
    if _in.today <= datetime(2023,9,22):
      _out.setting_point['sp_co2_setpoint_ppm_5min'][_in.set_time_int-3*12:_in.set_time_int+2*12] = 550
    else:
      _out.setting_point['sp_co2_setpoint_ppm_5min'][_in.set_time_int-3*12:_in.set_time_int+2*12] = 800         

    """
    hd setting
    """    
    _out.setting_point['sp_humidity_deficit_setpoint_5min'] = [2]*288


    """ 
    irrigation setting
        => sh
        1. everyday when light on, trigger
        2. stage 1: every 1 mol light accumulate 5ml 
        3. stage 2-3: every 1 mol accumulate 8.3ml
        
            1) stage 1: 2
            2) stage 2-3: 3
            3) stage 4: 5
        4. ave daily ec is lower - next day every 1 mol light accumulate -1ml
        5. ave daily ec is higher or no drain - next day every 1 mol light accumulate +1ml
        => move to per_hour stategy
    
    every 20ml trigger
    
    reset light sum value to 0 at midnight
    
    """
    _out.setting_point['sp_irrigation_interval_time_setpoint_min_5min'] = [1440]*288
    if 'led_start_time_int' in locals() or 'led_start_time_int' in globals():
        _out.setting_point['sp_irrigation_interval_time_setpoint_min_5min'][led_start_time_int] = 4
    else:
        _out.setting_point['sp_irrigation_interval_time_setpoint_min_5min'][_in.set_time_int] = 4
    
    ## to-do 
    # 4 mol light -> one shot    
    # time_to_irrigation = calc_irrigation_time_with_DLI(_in.indoor_env['fc_radiation_5min'], criterion = 4)
               

    """
    plantdensity setting
      additonal sensors
    - TRH sensor in the bush for plant density 
       humidity rule.. 
       depth image -> height sensing 
       using given date 
          
    """    
    _out.setting_point['sp_plantdensity'] = [_in.density[_in.nthday]]*288

    """
    harvest setting
    """ 
    _out.setting_point['sp_day_of_harvest_day_number'] = [351]*288   
    
    """
    additional sensor
    image sensor + TRH sensoer(inside the bush)
    
    """

    return _out