import sys
from datetime import datetime, timedelta
import traceback

import pandas as pd
import numpy as np
import yaml 

sys.path.append('./')
from a_util.service.letsgrow_service_simul import LetsgrowService

from aaaa.farm_math import sun_cal, get_DLI, datetime_to_int
from aaaa.cost_cal import cost_calculate, greenhouse_const
from a_util.letsgrow_const import LETSGROW_CONTROL

class GreenhouseControl:
    def __init__(self, config,lg_service, lg_simul_date, strategies:list, now = None):
        self.strategies = strategies
        if now is None:
            self.now = datetime.now()
        else:
            self.now = now
        self.today = self.now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.startdate = config['transplant_date']
        self.lg_service = lg_service
        # self.lg_service = LetsgrowService()
        self.indoor_env = lg_simul_date[(lg_simul_date.index >= now) & (lg_simul_date.index < now + timedelta(days=1)) ]
        self.indoor_env_yesterday = lg_simul_date[(lg_simul_date.index >= now - timedelta(days=1)) & (lg_simul_date.index < now) ]
        self.plant_status = None
        
        self.green_input = GreenHouseInput(config=config,
                                           startdate=self.startdate,
                                           indoor_env=self.indoor_env,
                                           indoor_env_yesterday=self.indoor_env_yesterday,
                                           plant_status=self.plant_status,
                                           now=self.now)
        self.green_out = GreenHouseOutput(today=self.today)
       
        # self.green_cost = cost_calculate(self.green_input,self.density)
      
    def get_greenhouse_data_to_db(self):
        """
            letsgrow to db 
        """
        print("Get Greenhouse data from db date: {}".format(self.today))
        return self.lg_service.letsgrow_to_db_day(self.today)

    def set_greenhouse_data_from_db(self):
        print("set Greenhouse data to db date: {}".format(self.today))
        return self.lg_service.data_from_db_day(self.today)

    def save_to_db(self,setpoint):
        print("Save setpoint to database")
        self.lg_service.pd_control_to_db(setpoint)
    
    def save_to_db_hour(self,setpoint):
        print("Save setpoint to database  one hour")
        self.lg_service.pd_control_to_db_hour(setpoint)

    def apply_to_greenhouse(self):
        print("Apply setpoin to greenhouse")
        self.lg_service.db_to_letsgrow(self.today)

    def apply_strategy(self):
        for stg in self.strategies:
            try:
                self.green_out = stg(self.green_input, self.green_out)
            except:
                traceback.print_exc()
                print("error: ")

        print("strategy calulation done")
        return self.green_out.plant_model

    def __str__(self) -> str:
        return  F"""
            green_input => {self.green_input}
            green_out  => {self.green_out} 
        """ 
        pass

class GreenHouseInput:
    def __init__(self, config, startdate, indoor_env, indoor_env_yesterday, plant_status, now):
        self.now = now 
        self.today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        print(self.today)
        self.nthday = (self.today - startdate).days        
        
        self.indoor_env = indoor_env
        self.indoor_env_yesterday = indoor_env_yesterday
        self.plant_status = plant_status
        
        self.rise_time, self.set_time = sun_cal(self.today, self.indoor_env, True)
        
        self.rise_time_int = datetime_to_int(self.rise_time)
        self.set_time_int = datetime_to_int(self.set_time)
        self.now_int = datetime_to_int(self.now)
                      
        self.config = config  
          
        ## pre calculate data
        self.expected_DLI = get_DLI(self.indoor_env['fc_radiation_5min'],
                                    transmittance=self.config["greenhouse_transmittance"],
                                    type="watt")
        self.current_DLI = get_DLI(self.indoor_env['outside_par_measurement_5min'],
                                   transmittance=self.config["greenhouse_transmittance"],
                                   window=[0,self.now_int],
                                   energy_screen_array=self.indoor_env['sp_energy_screen_setpoint_5min'],
                                   black_out_screen_array=self.indoor_env['sp_blackout_screen_setpoint_5min']
                                   )
        self.density = [ 56,56,56,56,56,56,56,56,56,56,56,56,56,56,
                    56,56,56,56,56,56,56,56,56,56,56,56,56,56,
                    56,56,56,42,42,42,42,42,42,42,42,42,42,42,
                    30,30,30,30,30,30,30,30,30,30,20,20,20,20,
                    20,20,20,20,20,20,20,20,20,20,20,20,20,20,
                    20,20,20,20,20,20,20,20,20,20,20,20,20,20,
                    20,20,20,20,20,20,20,20,20,20,20,20,20,20,
                    20,20,20,20,20,20,20,20,20,20,20,20,20,20,
                    20,20,20,20,20,20,20,20,20,20,20,20,20,20,
                    20,20,20,20,20,20,20,20,20,20,20,20,20,20,
                    20,20,20,20,20,20,20,20,20,20,20,20,20,20,
                    20,20,20,20,20,20,20,20,20,20,20,20,20,20,
                    20,20,20,20,20,20,20,20,20,20,20,20,20,20,                    
                    ]
          



    def __str__(self) -> str:
        return F"""
        today => {self.today}
        nthday => {self.nthday}
        forecast => {self.forecast}
        indoor_env => {self.indoor_env}
        plant_status => {self.plant_status}

        rise_time => {self.rise_time}
        rise_time_int => {self.rise_time_int}
        set_time => {self.set_time}
        set_time_int => {self.set_time_int}
        """
        

class GreenHouseOutput:
    def __init__(self, today:datetime):
        self.today = today
        self.plant_model = self.plant_model_init(today)
        self.setting_point = self.plant_model
        self.global_info = {}

    def plant_model_init(self,today):
        index = pd.date_range(today, periods=288, freq='5min')
        columns = LETSGROW_CONTROL
        return pd.DataFrame(index=index, columns=columns)

    def __str__(self) -> str:
        return F"""
            global_info => {self.global_info}
            setting_point => 
            {self.setting_point}
        """
        
