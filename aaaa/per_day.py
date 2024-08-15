import sys
from datetime import datetime
import json
import traceback

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
        lg_service.jsonbak_to_letsgrow(today)
    except Exception as e:
        print("error: ", e)
        traceback.print_exc()

    greenhouse = GreenhouseControl(
        startdate=datetime(2024,7,15), 
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
            ]
    )

    plant_model_output = greenhouse.calc_strategy()
    setpoint = greenhouse.calc_setpoint(plant_model_output)
    
    print("ok")
    
    # #print(greenhouse)
    greenhouse.save_to_db(setpoint)
    greenhouse.apply_to_greenhouse()
   
if __name__ == "__main__":
    s =  per_day()


