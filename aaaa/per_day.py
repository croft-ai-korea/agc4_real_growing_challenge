import sys
from datetime import datetime, timedelta
import json
import yaml
import traceback
import time

sys.path.append('./')

from a_util.service.letsgrow_service import LetsgrowService
from a_util.env.real_env import GreenhouseControl
from aaaa.strategy.strategy import base_strategy
# from aaaa.strategy.strategy import temp_strategy, enrg_screen_strategy, radiation_strategy, co2_strategy, \
#     humidity_strategy, base_strategy,statistics_temp_strategy_perday,\
#     statistics_ventilation_strategy_perday,statistics_radiation_strategy_perday,statistics_co2_strategy_perday,statistics_HD_strategy_perday,netPipeMin_strategy,\
#     leeVentMin_strategy,blk_screen_strategy, density_strategy, harvest_strategy

def per_day():
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        lg_service = LetsgrowService()
        lg_service.jsonbak_to_letsgrow(begin_time=today,
                                       json_path='a_util/rest_api/save_control.json')
    except Exception as e:
        print("error: ", e)
        traceback.print_exc()

    config_path = "./a_util/env/config.yaml"
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
                
    # now = datetime(2024,8,26,0,0,0)    # 특정 날자 세팅
    now = None   # 만약 오늘을 집어넣고 싶으면 today는 None으로 설정
        
    greenhouse = GreenhouseControl(      
        config=config,  
        strategies = [
                base_strategy,
                # temp_strategy,
                # radiation_strategy,
                # co2_strategy,
                # humidity_strategy,
                # radiation_strategy,
                # statistics_temp_strategy_perday,
                # statistics_ventilation_strategy_perday,
                # statistics_radiation_strategy_perday,
                # statistics_co2_strategy_perday,
                # statistics_HD_strategy_perday,
                # enrg_screen_strategy,
                # netPipeMin_strategy,
                # leeVentMin_strategy,
                # blk_screen_strategy,
                # density_strategy,
                # harvest_strategy
            ],
        now = now
    )

    setpoint = greenhouse.apply_strategy()
        
    # #print(greenhouse)
    greenhouse.save_to_db(setpoint)
    greenhouse.apply_to_greenhouse()
       
if __name__ == "__main__":
    s =  per_day()


