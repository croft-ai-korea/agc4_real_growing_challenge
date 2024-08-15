import math
from typing import Any, List
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def sun_cal(date, forecast, wur_cal=True):
    if (wur_cal == False):
        par_sum = 0
        par_trig = True
        for key, value in enumerate(forecast['fc_radiation_5min']):
            # glass transmission
            par_sum = par_sum + wsm_to_umolm2(value)
            if (par_sum > 50 and par_trig):
                # par_sum이 50 이상이면 해가 떴다고 간주
                date_Rise = date.replace(hour=int(key / 12))
                par_trig = False
            elif (wsm_to_umolm2(value) == 0 and par_trig == False):
                # 해가 뜬 이후 예보 결과가 0이면 해가 졌다고 간주
                date_Set = date.replace(hour=int(key / 12))
                break
    else:
        # dayOfYear = 31 , 2 * math.pi / 365 = 0.01721420632103996
        dayOfYear = (date - date.replace(month=1, day=1)).days
        latitude = 52
        Year_angle = (dayOfYear - 80) * 2 * math.pi / 365
        ellipseCorrection = -7.127 * math.cos(Year_angle) - 1.84 * math.sin(Year_angle) - 0.688 * math.cos(
            2 * Year_angle) + 9.92 * math.sin(2 * Year_angle)
        declination = 0.38 - 0.77 * math.cos(Year_angle) + 23.27 * math.sin(Year_angle) + 0.37 * math.cos(
            2 * Year_angle) - 0.109 * math.sin(2 * Year_angle) - 0.1665 * math.sin(3 * Year_angle)
        Day_length = math.acos(
            -math.tan(declination * 2 * math.pi / 360) * math.tan(latitude * 2 * math.pi / 360)) * 24 / math.pi

        Rise = 12.6 - ellipseCorrection / 60 - 0.5 * Day_length
        Set = 12.6 - ellipseCorrection / 60 + 0.5 * Day_length
        # print("Rise",Rise)
        # print("Set",Set)
        date_Rise = date.replace(hour=math.floor(Rise), minute=math.floor(Rise % math.floor(Rise) * 60))
        date_Set = date.replace(hour=math.floor(Set), minute=math.floor(Set % math.floor(Set) * 60))
        # print("sun_rise = {} and sun_set = {}".format(date_Rise, date_Set))
    return date_Rise, date_Set

def wsm_to_jcm2_day(rad_array: Any):
    return rad_array.sum() * 0.0001 * 60 * 60

def jcm2_to_molm2_day(jcm_var):
    return jcm_var * 0.0215

def get_DLI(light_array:Any, 
            interval:int = 5, 
            transmittance:float = 1.0, 
            type:str="umol", 
            window:List = None,
            energy_screen_array = None,
            black_out_screen_array = None,            
            ):
    """
        interval : min
        type : "umol", "watt"
        window : [start_time_int, end_time_int]  
                 if interval is not 5, then must need correspond value
    """
    if window is None:
        window = [0, 287]
    if energy_screen_array is None:
        energy_screen_array = np.array([0]*288)
    if black_out_screen_array is None:
        black_out_screen_array = np.array([0]*288)
    
    energy_screen_effect = ((100-energy_screen_array)+0.7*energy_screen_array)/100
    blackout_screen_effect = (100-black_out_screen_array)/100
    
    light_array_with_screen_effect = light_array*energy_screen_effect*blackout_screen_effect
        
    if type == "umol":
        return sum(light_array_with_screen_effect[window[0]:window[1]])*transmittance*interval*60*1e-6
    elif type == "watt":
        return 2.1*sum(light_array_with_screen_effect[window[0]:window[1]])*transmittance*interval*60*1e-6

def fruit_price(weight):
    """
       weight for red tomato 
    """
    if weight < 50:
        return -0.75
    elif weight < 80:
        return 1.8*(weight-80)/(80-50)+1.8-0.75
    elif weight <150:
        return (2-1.8)*(weight-150)/(150-80)+2-0.75
    else:
        return 2-0.75
    

def get_peakTime(array):
    result = np.convolve(np.array(array), np.ones(shape=36))  # to-do check 5min or not
    p_data = np.where(result == result.max())[0]-18
    if len(p_data) != 1:
        return 150
    else:
        return p_data[0]

def datetime_to_int(input:datetime):
    return (input.hour*60+input.minute)//5

# 4.6 μmole.m2/s = 1 W/m2
# 2.1 μmole.m2/s = 1 W/m2 (305 - 2800nm)
# glass transmission
def watt_to_umolm2(rad_array):
    return rad_array * 2.1

def wsm_to_molm2_day(rad_array):
    return sum(rad_array) * 2.1 * 60 * 60 * 1e-6

def VPD_cal(green_temp,green_humidity,plant_Temp):
    VPsat = (610.7*10**((7.5*plant_Temp)/(237.3+plant_Temp)))/1000
    VPair = (610.7*10**((7.5*green_temp)/(237.3+green_temp)))/1000 * green_humidity/100
    VPD = VPsat-VPair
