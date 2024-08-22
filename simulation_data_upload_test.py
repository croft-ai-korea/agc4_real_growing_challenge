import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
from aaaa.farm_math import datetime_to_int, fruit_price

csv_file_path = "./a_util/reference2.csv"


df = pd.read_csv(csv_file_path)

# additional columns
# par_sensor_above, tpipe, conpipes_tsuppipe, pconpipe, lmp_elecuse,
# fruit_fresh_weight, dvs_fruit, dry_matter_fract, crop_abs, elec_price_peakhour
# red_fruits_weight, mc_pure_air

## rename
column_rename = {
    "DateTime":"time",
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
df = df.set_index('time')
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

df = df.resample('5T').interpolate(method='linear')

start_date = df.index[0]

DosingCapacity = 100
lamp_max_intensity = 100   # 질문사항
num_screens = 2

fixed_costs_accum = 0
variable_costs_accum = 0 

electric_coeff = np.array([0.2]*288)
electric_coeff[datetime_to_int(datetime(2024,1,1,7,0,0)):datetime_to_int(datetime(2024,1,1,23,0,0))] = 0.3 

coeef = 90

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

    # print("net profit : ", df.loc[filtered_index,'net_profit'][-1]*coeef, "gain : ", df.loc[filtered_index,'gains'][-1]*coeef, "total cost : ", df.loc[filtered_index,'total_cost'][-1]*coeef)
    
    net_profit_value = df.loc[filtered_index,'net_profit'][-1]*coeef - df.loc[filtered_index, 'gains'][-1]*coeef - gain_value 
    print("net profit : ", net_profit_value, "gain : ", gain_value, "total cost : ", df.loc[filtered_index,'total_cost'][-1]*coeef)
    
    
