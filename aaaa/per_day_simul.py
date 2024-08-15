import sys
from datetime import datetime, timedelta
import json
import traceback
import time
import yaml 
import pandas as pd

sys.path.append('./')

from a_util.service.letsgrow_service_simul import LetsgrowService
from a_util.env.sim_env import GreenhouseControl
from aaaa.strategy.strategy import base_strategy
# from aaaa.strategy.strategy import temp_strategy, enrg_screen_strategy, radiation_strategy, co2_strategy, \
#     humidity_strategy, base_strategy,statistics_temp_strategy_perday,\
#     statistics_ventilation_strategy_perday,statistics_radiation_strategy_perday,statistics_co2_strategy_perday,statistics_HD_strategy_perday,netPipeMin_strategy,\
#     leeVentMin_strategy,blk_screen_strategy, density_strategy, harvest_strategy

def per_day(config = None):
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        lg_service = LetsgrowService()
        lg_service.jsonbak_to_letsgrow(begin_time=today,
                                json_path='a_util/rest_api/save_control_simul.json')
    except Exception as e:
        print("error: ", e)
        traceback.print_exc()
    
    if config is None:
        config_path = "./a_util/env/config.yaml"
        
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
    setpoint_list = []
                
    now = config['start_date']   
    
    # def data_from_db(self, begin_time, end_time):
    #     return self.letsgrow_Dao.from_db(begin_time, end_time)  
    
    lg_service = LetsgrowService()
    lg_simul_data = lg_service.data_from_db(config['start_date']-timedelta(days=1), config['end_date'])
    
    while now < config['end_date']:        
        greenhouse = GreenhouseControl(            
            config=config, 
            lg_service = lg_service,
            lg_simul_date=lg_simul_data,
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
            now = now,       
            
        )

        setpoint = greenhouse.apply_strategy()
        
        setpoint_list.append(setpoint)     
        
        now += timedelta(days=1)
    
    setpoints = pd.concat(setpoint_list)
    setpoints.sort_index(inplace=True)
    
    # #print(greenhouse)
    greenhouse.save_to_db(setpoints)
    greenhouse.apply_to_greenhouse()
       
if __name__ == "__main__":
    s =  per_day()


