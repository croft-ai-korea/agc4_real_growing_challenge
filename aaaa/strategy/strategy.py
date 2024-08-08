import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
from a_util.env.real_env import GreenHouseInput, GreenHouseOutput
from aaaa.farm_math import sun_cal
import json
import os
import sys

sys.path.append('./')

def base_strategy(_in: GreenHouseInput, _out: GreenHouseOutput) -> GreenHouseOutput:
    """
    _in : 상수의 느낌
    _out:
        setpoint :
        global_info : 다른 strategy 함수와 공유하는 변수
    """
    """
    led/screen setting
    - Daily light sum
      - minimal 10
      - no max yet 18
      - max capacity 500
    - eletricity price
      - peak 7:00-23:00: 0.3 euro per kwh
      - low 23:00-7:00: 0.2 euro per kwh
    """
    """
    heating/venting temp
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
    _out.setting_point['sp_leeside_minvent_position_setpoint_5min'] = [5]*288
    _out.setting_point['sp_net_pipe_minimum_setpoint_5min'] = [0]*288
    _out.setting_point['sp_value_to_isii_1_5min'] = [0]*288
    _out.setting_point['sp_energy_screen_setpoint_5min'] = [50]*288
    _out.setting_point['sp_blackout_screen_setpoint_5min'] = [0]*288
    _out.setting_point['sp_co2_setpoint_ppm_5min'] = [500]*288
    _out.setting_point['sp_humidity_deficit_setpoint_5min'] = [4]*288
    _out.setting_point['sp_irrigation_interval_time_setpoint_min_5min'] = [30]*288
    _out.setting_point['sp_plantdensity'] = [56]*288
    _out.setting_point['sp_day_of_harvest_day_number'] = [351]*288   
    
    return _out