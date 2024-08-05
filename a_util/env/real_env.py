import sys
from datetime import datetime, timedelta
import traceback

import pandas as pd
import numpy as np

sys.path.append('./')
from a_util.service.letsgrow_service import LetsgrowService

from aaaa.farm_math import sun_cal, wsm_to_molm2_day, wsm_to_molm2_day_per5min
from aaaa.cost_cal import cost_calculate, greenhouse_const
from a_util.letsgrow_const import LETGROW_FORCAST, LETSGROW_CONTROL

class GreenhouseControl:
    def __init__(self, startdate, strategies:list):
        self.strategies = strategies
        self.today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.startdate = startdate
        self.lg_service = LetsgrowService()
        self.indoor_env = self.lg_service.data_from_db_day(self.today)
        self.indoor_env_yesterday = self.lg_service.data_from_db_day(self.today-timedelta(days=1))
        self.plant_status = self.get_plant_status(self.today)
        self.forecast_data = self.get_forecast_real()

        self.green_input = GreenHouseInput(self.startdate, self.indoor_env,self.indoor_env_yesterday, self.plant_status, self.today)
        self.green_out = GreenHouseOutput(self.today)
        ## to-do
        self.density = [ 
                        90,90,90,90,90,90,90,
                        60,60,60,60,60,60,60,
                        45,45,45,45,45,45,45,
                        30,30,30,30,30,30,30,
                        22.5,22.5,22.5,22.5,22.5,22.5,
                        18,18,18,18,18,18,18,
                        15,15,15,15,15,15,15
                    ]
        self.green_cost = cost_calculate(self.green_input,self.density)




    def get_plant_status(self, start_date):
        #todo

        #self.rs_service = RealsenseService()
        #return self.rs_service.getOnedayData(start_date)

        pass

    def get_forecast_real(self):
        print("Get Forecast date from {}".format(self.today))
        self.forecast_data = self.indoor_env[LETGROW_FORCAST]
        return self.forecast_data
        
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

    def calc_strategy(self):
        for stg in self.strategies:
            try:
                self.green_out = stg(self.green_input, self.green_out)
            except:
                traceback.print_exc()
                print("error: ")

        print("strategy calulation done")
        return self.green_out.plant_model

    def calc_setpoint(self,plant_model):
        self.green_out.setting_point = plant_model
        print("setpoint calulation done")
        return self.green_out.setting_point

    def __str__(self) -> str:
        return  F"""
            green_input => {self.green_input}
            green_out  => {self.green_out} 
        """ 

        pass

class GreenHouseInput:
    def __init__(self, startdate, indoor_env, indoor_env_yesterday, plant_status, today):
        self.now = datetime.now() 
        self.today = today
        self.nthday = (self.today - startdate).days
        self.forecast = indoor_env[LETGROW_FORCAST]
        self.setpoint = indoor_env[LETSGROW_CONTROL]
        self.indoor_env = indoor_env
        self.indoor_env_yesterday = indoor_env_yesterday
        self.plant_status = plant_status
        self.rise_time, self.set_time = sun_cal(self.today, self.forecast, True)
        self.rise_time_int = self.rise_time.hour * 60 + self.rise_time.minute
        self.set_time_int = self.set_time.hour * 60 + self.set_time.minute
        self.statistics_strategy_json = "strategyDay.json"  # to-do
        self.LED_iglob_threshold = 500
        self.par_setpoint = 205
        self.LED_max = 75

     
    def get_Iglob_sum(self):
        return wsm_to_molm2_day_per5min(self.forecast["FC_radiation_5min"])  # to-do check 5min or not
    def get_temp_av(self):
        return self.forecast["FC_outside_temperature_5min"].mean()  # to-do check 5min or not
    def get_windspeed_av(self):
        return self.forecast["FC_wind_speed_5min"].mean()  # to-do check 5min or not
    def get_peakRadiationTime(self):
        result = np.convolve(np.array(self.forecast["FC_radiation_5min"]), np.ones(shape=36))  # to-do check 5min or not
        p_data = np.where(result == result.max())[0]-18
        if len(p_data) != 1:
            return 150
        else:
            return p_data[0]
    def get_temp_night_av(self):
        iglob_data = self.forecast["FC_radiation_5min"]  # to-do check 5min or not
        temp_data = self.forecast["FC_outside_temperature_5min"]  # to-do check 5min or not
        return temp_data[iglob_data==0].mean()
    def get_Iglob_sum_under_LED(self):
        iglob_data = self.forecast["FC_radiation_5min"]  # to-do check 5min or not
        return iglob_data[iglob_data>self.LED_iglob_threshold].sum()*5*60*2/1000000*0.65
    def get_LED_ON_TIME(self):
        iglob_data = self.forecast["FC_radiation_5min"]  # to-do check 5min or not
        if True in list(iglob_data > self.LED_iglob_threshold):
            LED_ON_TIME = [self.rise_time_int - 240,
                            list(iglob_data > self.LED_iglob_threshold).index(True)*5,
                            (len(iglob_data) - list(iglob_data > self.LED_iglob_threshold)[::-1].index(True)) * 5,
                            self.set_time_int + 120
                            ]
        else:
            LED_ON_TIME = [self.rise_time_int - 240,12*60,12*60,self.set_time_int + 120]

        LED_ON_TIME[3] = 20*60 if LED_ON_TIME[3] > 20*60 else LED_ON_TIME[3]
        return LED_ON_TIME


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
        Iglob_sum => {self.Iglob_sum}

        temp_av => {self.temp_av}
        windspeed_av => {self.windspeed_av}
        LED_iglob_threshold => {self.LED_iglob_threshold}
        PeakRadiationTime => {self.PeakRadiationTime}
        temp_night_av => {self.temp_night_av}
        
        Iglob_sum_under_LED => {self.Iglob_sum_under_LED}
        LED_ON_TIME => {self.LED_ON_TIME}
        """
        

class GreenHouseOutput:
    def __init__(self, today:datetime):
        self.today = today
        self.plant_model = self.plant_model_init(today)
        self.setting_point = self.plant_model
        self.global_info = {}

    def plant_model_init(self,today):
        index = pd.date_range(today, periods=288, freq='5min')
        columns = [LETSGROW_CONTROL]
        return pd.DataFrame(index=index, columns=columns)

    def __str__(self) -> str:
        return F"""
            global_info => {self.global_info}
            setting_point => 
            {self.setting_point}
        """
        
