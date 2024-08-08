import pandas as pd
import os
import copy
import sys
import psycopg2
from random import random
from datetime import datetime
from psycopg2.extras import execute_values

sys.path.append('./')

from temp.manual_parameter import heatingTemp, hours_light, max_iglob, ventOffset
from a_util.simulator.greenhouse import Greenhouse, get_day_data
from a_util.simulator.simulator import send_server, json_parsing, sim_greenhouse, get_endDate_from_output
from a_util.simulator.simulator import modify_temperature, modify_intensity, modify_hours_light
from a_util.simulator.simulator import modify_temperature_random, modify_intensity_random, modify_hours_light_random
from a_util.simulator.simulator import convert_key_from_start_date, get_realtime_data, get_reference_table
from a_util.simulator.simulator import action_table_to_server_format
from a_util.db.db_util import create_table_if_not_exists, db_drop_table_if_exists, db_simulation_data_insert
from a_util.db.schema import create_simulation_table_query

control_json_path = "temp/Par_Out_23_12.54.89_control.json"
Par_Out_reference = "temp/Par_Out_23_12.54.89.json"

### Initialize and set up the greenhouse
greenhouse_control = Greenhouse(logging_enabled=False)
greenhouse_control.initialize_devices(control_json_path = control_json_path)

save_folder = "./temp/"
episode = str(datetime.now().strftime("%d_%H.%M.%f")[:11])
response_csv_path = os.path.join(save_folder, f"Par_Out_{episode}.csv")


### modify setting point
greenhouse_control.endDate = '31-10-2023'
startDate = '05-09-2023'
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
parameters = greenhouse_control.export_all_devices()
reference_json_path = "ref.json"
result_json = send_server(parameters=parameters,response_json_save_path=reference_json_path)
result_pandas = json_parsing(response_json_path=reference_json_path, response_csv_path = response_csv_path)
result_pandas.index.rename('time', inplace=True)

db_drop_table_if_exists(table_name = 'simulation')
create_table_if_not_exists(table_name = 'simulation', query=create_simulation_table_query)

# # 데이터 삽입 쿼리
# insert_query = """
# INSERT INTO simulation (
#     time, comp1_air_t, comp1_air_rh, comp1_air_ppm, common_iglob_value, common_tout_value,
#     common_rhout_value, common_windsp_value, comp1_parsensor_above, comp1_tpipe1_value,
#     comp1_conpipes_tsupipe1, comp1_pconpipe1_value, comp1_conwin_winlee, comp1_conwin_winwnd,
#     comp1_setpoints_spheat, comp1_setpoints_spvent, comp1_scr1_pos, comp1_scr2_pos,
#     comp1_lmp1_elecuse, comp1_mcpureair_value, comp1_setpoints_spco2, comp1_growth_fruitfreshweight,
#     comp1_growth_dvsfruit, comp1_growth_drymatterfract, comp1_growth_cropabs, comp1_growth_plantdensity,
#     common_elecprice_peakhour, comp1_growth_wateruseperpot, comp1_growth_redfruitsweight
# ) VALUES %s
# """

df = pd.read_csv(response_csv_path)

db_simulation_data_insert(df=df)


# # 데이터 프레임이 이미 있는 경우
# data_tuples = [tuple(x) for x in df.to_numpy()]

# # PostgreSQL 연결 정보
# conn = psycopg2.connect(
#     host="localhost",
#     port="5432",
#     database="postgres",
#     user="postgres",
#     password="admin1234"
# )

# cur = conn.cursor()


# # # 테이블 생성 쿼리 실행 (필요 시)
# # cur.execute(create_table_query)
# # conn.commit()

# # # 테이블을 비우는 쿼리 실행
# # cur.execute(delete_query)
# # conn.commit()

# # execute_values를 사용하여 데이터 삽입
# execute_values(cur, insert_query, data_tuples)

# conn.commit()
# cur.close()
# conn.close()

# print("ok")

