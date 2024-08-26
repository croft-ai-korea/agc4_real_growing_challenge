import sys
from datetime import datetime, timedelta
import json
import yaml
import traceback
import time
import pytz

sys.path.append('./')

from a_util.service.letsgrow_service import LetsgrowService
from a_util.env.real_env import GreenhouseControl
from aaaa.strategy.strategy import base_strategy, clone_setpoint_strategy, irrigation_control_strategy
# from aaaa.strategy.strategy import temp_strategy, enrg_screen_strategy, radiation_strategy, co2_strategy, \
#     humidity_strategy, base_strategy,statistics_temp_strategy_perday,\
#     statistics_ventilation_strategy_perday,statistics_radiation_strategy_perday,statistics_co2_strategy_perday,statistics_HD_strategy_perday,netPipeMin_strategy,\
#     leeVentMin_strategy,blk_screen_strategy, density_strategy, harvest_strategy

def per_30min():
    config_path = "./a_util/env/config.yaml"
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    now = datetime(2024,8,26,0,0,0)  
    now = datetime.now(pytz.timezone('Europe/Amsterdam')).replace(tzinfo=None)

    greenhouse = GreenhouseControl(
        config=config, 
        strategies = [
            clone_setpoint_strategy,
            irrigation_control_strategy
            ],
        now = now
    )

    setpoint = greenhouse.apply_strategy()
    greenhouse.save_to_db(setpoint)
    greenhouse.apply_to_greenhouse()

if __name__ == "__main__":
    s =  per_30min()