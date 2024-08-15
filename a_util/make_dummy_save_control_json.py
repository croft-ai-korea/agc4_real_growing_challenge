import json 
from datetime import datetime, timedelta
import sys
sys.path.append('./')

from a_util.letsgrow_const import COLID_MAP_NAME, COLID_MAP_NUMBER
from a_util.letsgrow_const import LETGROW_FORCAST, LETSGROW_CONTROL
from a_util.letsgrow_const import LETSGROW_MOD_COLS_MAP

def make_dummy_save_control_json(date:datetime = datetime(2024,7,15,0,0)):
    default_timestamp = date
    formatted_timestamp = default_timestamp.isoformat(timespec='minutes')

    save_control = []

    for i in range(288):
        now = default_timestamp+timedelta(minutes=i*5)
        formatted_timestamp = now.isoformat(timespec='minutes')
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_plantdensity'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 56.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_day_of_harvest_day_number'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 90.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_heating_temp_setpoint_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 18.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_vent_ilation_temp_setpoint_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 20.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_leeside_minvent_position_setpoint_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 5.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_net_pipe_minimum_setpoint_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 0.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_Value_to_iSii_1_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 0.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_energy_screen_setpoint_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 50.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_blackout_screen_setpoint_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 0.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_CO2_setpoint_ppm_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 500.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_humidity_deficit_setpoint_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 4.0,
                'Offset' : 0
            }              
        )
        save_control.append(
            {
                'colId' : COLID_MAP_NAME['sp_irrigation_interval_time_setpoint_min_5min'],
                'TimeStamp' : formatted_timestamp,
                'Value' : 20.0,
                'Offset' : 0
            }              
        )

    # 저장할 파일 경로
    file_path = "./a_util/rest_api/save_control.json"

    # JSON 파일로 저장
    with open(file_path, 'w') as file:
        json.dump(save_control, file, indent=4)
        
if __name__ == "__main__":
    date = datetime(2024,7,15,0,0)
    make_dummy_save_control_json(date = date)
          
# COLID_MAP_NAME = {
#     'tair':1593811,
#     'rh':1593815,
#     'co2':1593819,
#     'dx':1593823,
#     'vent_lee':1593827,
#     'vent_wind':1593831,
#     't_rail':1593835,
#     'par':1593839,
#     'lamps':1593843,
#     'scr_enrg':1593845,
#     'scr_blck':1593849,
#     'co2_reg':1593853,
#     'heating_temp_vip':1593857,
#     'heating_temp_sp':1593775,
#     'vent_templee_vip':1593861,
#     'vent_tempwind_vip':1593865,
#     'vent_temp_sp':1593779,
#     'lee_wind_min_vip':1593869,
#     'lee_vent_min_sp':1593783,
#     'net_pipe_vip':1593873,
#     'net_pipe_sp':1593787,
#     'scr_enrg_vip':1593877,
#     'scr_enrg_sp':1593791,
#     'scr_blck_vip':1593881,
#     'scr_blck_sp':1593795,
#     'lamps_vip':1608458,
#     'lamps_sp':1608460,
#     'co2_vip':1593889,
#     'co2_sp':1593803,
#     'dx_vip':1593893,
#     'dx_sp':1593807,
#     'sigrow_par':1593485,
#     'sigrow_tair':1593489,
#     'sigrow_rh':1593493,
#     'sigrow_stomata':1593497,
#     'ridder_netrad':1593501,
#     'ridder_transp':1593503,
#     'ridder_leaftem':1593505,
#     'plant_density':1602309,
#     'day_of_harvest':1602310,
#     'fc_tout':611680,
#     'fc_rhout':611682,
#     'fc_iglob':611684 ,
#     'fc_radsum':611686,
#     'fc_windsp':611688,
#     'fc_cloud':611690,
#     'out_tout':611644,
#     'out_rhout':611648,  
#     'out_iglob':611656,  
#     'out_windsp':611660,  
#     'out_radsum':611658,  
#     'out_winddir':611664,  
#     'out_rain':611668,  
#     'out_parout':611672,  
#     'out_pyrgeo':611676,  
#     'out_abshumout':611640
# }

# COLID_MAP_NUMBER = inv_map = {str(v): k for k, v in COLID_MAP_NAME.items()} 

# file_path = "./temp/save_control.json"

# with open(file_path, 'r') as file:
#     colID_data = json.load(file)

# colID_list = []
# for data in colID_data:
#     if data['colId'] not in colID_list:
#         colID_list.append(data['colId'])
#     print(data)  

# for ci in colID_list:
#     print(COLID_MAP_NUMBER[str(ci)])
# print("ok")

