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
    _out.setting_point['sp_heating_temp_setpoint_5min'] = [19]*288
    
    return _out