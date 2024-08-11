import pandas as pd
import os
import copy
import sys
import psycopg2
from random import random
from datetime import datetime
from psycopg2.extras import execute_values

from temp.manual_parameter import heatingTemp, hours_light, max_iglob, ventOffset
from a_util.simulator.greenhouse import Greenhouse, get_day_data
from a_util.simulator.simulator import send_server, json_parsing, sim_greenhouse, get_endDate_from_output
from a_util.simulator.simulator import modify_temperature, modify_intensity, modify_hours_light
from a_util.simulator.simulator import modify_temperature_random, modify_intensity_random, modify_hours_light_random
from a_util.simulator.simulator import convert_key_from_start_date, get_realtime_data, get_reference_table
from a_util.simulator.simulator import action_table_to_server_format
from a_util.db.db_util import create_table_if_not_exists, db_drop_table_if_exists, db_simulation_data_insert
from a_util.db.schema import create_simulation_table_query


def simulation_test():
    sys.path.append('./')
    control_json_path = "temp/Par_Out_23_12.54.89_control.json"
    Par_Out_reference = "temp/Par_Out_23_12.54.89.json"

    db_drop_table_if_exists(table_name = 'simulation')
    create_table_if_not_exists(table_name = 'simulation', query=create_simulation_table_query)

    reference_csv_path = "temp/reference.csv"
    df = pd.read_csv(reference_csv_path)
    df.rename(columns={"DateTime":"time"}, inplace=True)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    
    # env_keys = ['comp1.Air.T', 'comp1.Air.RH', 'comp1.Air.ppm', 'common.Iglob.Value',
    #    'common.Tout.Value', 'common.RHout.Value', 'common.Windsp.Value',
    #    'comp1.PARsensor.Above', 'comp1.TPipe1.Value',
    #    'comp1.ConPipes.TSupPipe1', 'comp1.PConPipe1.Value',
    #    'comp1.ConWin.WinLee', 'comp1.ConWin.WinWnd', 'comp1.Setpoints.SpHeat',
    #    'comp1.Setpoints.SpVent', 'comp1.Scr1.Pos', 'comp1.Scr2.Pos',
    #    'comp1.Lmp1.ElecUse', 'comp1.McPureAir.Value', 'comp1.Setpoints.SpCO2',
    #    'comp1.Growth.FruitFreshweight', 'comp1.Growth.DVSfruit',
    #    'comp1.Growth.DryMatterFract', 'comp1.Growth.CropAbs',
    #    'comp1.Growth.PlantDensity', 'common.ElecPrice.PeakHour',
    #    'comp1.Growth.WaterUsePerPot', 'comp1.Growth.RedFruitsWeight']
    
    env_keys = ['comp1.Air.T', 'comp1.Air.RH', 'comp1.Air.ppm', 'common.Iglob.Value',
       'common.Tout.Value', 'common.RHout.Value', 'common.Windsp.Value',
       'comp1.PARsensor.Above', 'comp1.TPipe1.Value',
       'comp1.ConPipes.TSupPipe1', 'comp1.PConPipe1.Value',
       'comp1.ConWin.WinLee', 'comp1.ConWin.WinWnd', 'comp1.Setpoints.SpHeat',
       'comp1.Setpoints.SpVent', 'comp1.Scr1.Pos', 'comp1.Scr2.Pos',
       'comp1.Lmp1.ElecUse', 'comp1.McPureAir.Value', 'comp1.Setpoints.SpCO2',
       'comp1.Growth.FruitFreshweight', 'comp1.Growth.DVSfruit',
       'comp1.Growth.DryMatterFract', 'comp1.Growth.CropAbs',
       'comp1.Growth.PlantDensity', 'common.ElecPrice.PeakHour',
       'comp1.Growth.WaterUsePerPot', 'comp1.Growth.RedFruitsWeight']

    ### Initialize and set up the greenhouse
    greenhouse_control = Greenhouse(logging_enabled=False)
    greenhouse_control.initialize_devices(control_json_path = control_json_path)

    save_folder = "./temp/"
    episode = str(datetime.now().strftime("%d_%H.%M.%f")[:11])
    response_csv_path = os.path.join(save_folder, f"Par_Out_{episode}.csv")


    ### modify setting point
    greenhouse_control.endDate = '31-12-2023'
    startDate = '05-09-2023'
    greenhouse_control.startDate = startDate
    print(greenhouse_control.plantDensity)
    greenhouse_control.plantDensity = "1 56; 32 42; 42 30; 52 20"

    ### set weather data and analysis 
    reference = json_parsing(response_json_path = Par_Out_reference)
    greenhouse_control.load_weather_data_and_analysis(reference)

    greenhouse_control.device_illumination['lmp1'].intensity = 250

    greenhouse_control.device_setpoints['setpoints'].temp.heatingTemp = convert_key_from_start_date(heatingTemp, startDate)
    greenhouse_control.device_setpoints['setpoints'].temp.ventOffset = convert_key_from_start_date(ventOffset, startDate)
    # heatingTemp = copy.deepcopy(greenhouse_control.device_setpoints['setpoints'].temp.heatingTemp)
    # intensity = copy.deepcopy(greenhouse_control.device_illumination['lmp1'].intensity)
    # max_iglob = copy.deepcopy(greenhouse_control.device_illumination['lmp1'].max_iglob)
    # hours_light = copy.deepcopy(greenhouse_control.device_illumination['lmp1'].hours_light)

    ### reference data
    parameters = greenhouse_control.export_all_devices(set_start_date = True)
    reference_json_path = "ref.json"
    result_json = send_server(parameters=parameters,response_json_save_path=reference_json_path)
    result_pandas = json_parsing(response_json_path=reference_json_path, response_csv_path = response_csv_path)
    result_pandas.index.rename('time', inplace=True)



    db_simulation_data_insert(df=df)


if __name__ == "__main__":
    ## do simulator
    simulation_test()
    
