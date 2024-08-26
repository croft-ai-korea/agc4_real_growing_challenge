import sys
from datetime import datetime, timedelta
import traceback
import pytz

import pandas as pd
import numpy as np
import yaml 

sys.path.append('./')
from a_util.service.letsgrow_service import LetsgrowService

from aaaa.farm_math import sun_cal, get_DLI, datetime_to_int
from aaaa.cost_cal import cost_calculate, greenhouse_const
from a_util.letsgrow_const import LETSGROW_CONTROL, LETSGROW_CONTROL_WITH_EXTRA_PARAM
from a_util.simulator.simulator import generate_density_from_string

class GreenhouseControl:
    def __init__(self, config, strategies:list, now = None):
        self.config = config
        self.strategies = strategies
        if now is None:
            self.now = datetime.now(pytz.timezone('Europe/Amsterdam')).replace(tzinfo=None)
        else:
            self.now = now
        self.today = self.now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.startdate = config['start_date']
        self.lg_service = LetsgrowService()        
        self.indoor_env = self.get_data_5min(self.today)
        self.indoor_env_yesterday = self.get_data_5min(self.today-timedelta(days=1))

        # 어제의 적산온도를 반영
        if self.indoor_env_yesterday['accumulate_temperature'][-1] is None:
            self.indoor_env['accumulate_temperature'] = 0
        else:
            temp_average = sum(self.indoor_env_yesterday['temperature_greenhouse_5min'])/len(self.indoor_env_yesterday['temperature_greenhouse_5min'])
            self.indoor_env['accumulate_temperature'] = self.indoor_env_yesterday['accumulate_temperature'][-1] + temp_average
        """
        - 1st stage : 4 Sep ~ 18 Sep
        - 2nd stage : 18 Sep ~ 22 Sep
        - 3rd stage : 22 Sep ~ 29 Sep
        - 4th stage : 29 Sep - 9 Oct
        - 5th stage : 9 October - 9 November

        irrigation setting
        => sh
        1. everyday when light on, trigger
        2. stage 1: every 1 mol light accumulate 5ml 
        3. stage 2-3: every 1 mol accumulate 8.3ml
        
        EC 기준
            1) stage 1: 2
            2) stage 2-3: 3
            3) stage 4: 5
        4. ave daily ec is lower - next day every 1 mol light accumulate -1ml
        5. ave daily ec is higher or no drain - next day every 1 mol light accumulate +1ml
        => move to per_hour stategy
    
        every 20ml trigger
        
        reset light sum value to 0 at midnight
        """

        # EC에 따른 물 공급 반영 wooram
        try:
            if self.today < datetime(2024,9,19):
                if self.indoor_env_yesterday['irrigation_ml'][-1] is None:
                    self.indoor_env['irrigation_ml'] = 5
                else:
                    yesterday_ml = self.indoor_env_yesterday['irrigation_ml'][-1]
                    yesterday_ec = sum(self.indoor_env_yesterday['drain_ec_5min'])/len(self.indoor_env_yesterday['drain_ec_5min'])
                    if yesterday_ec < 1.8:
                        target_ml = yesterday_ml - 1 
                        if target_ml < 1:
                            target_ml = 1                    
                    elif yesterday_ec > 2.2:
                        target_ml = yesterday_ml + 1
                        if target_ml > 10:
                            target_ml = 10
                    else:
                        target_ml = yesterday_ml
                    self.indoor_env['irrigation_ml'] = target_ml     
            elif self.today < datetime(2024,9,29):
                if self.today == datetime(2024,9,19):
                    self.indoor_env['irrigation_ml'] = 8.3
                else:
                    yesterday_ml = self.indoor_env_yesterday['irrigation_ml'][-1]
                    yesterday_ec = sum(self.indoor_env_yesterday['drain_ec_5min'])/len(self.indoor_env_yesterday['drain_ec_5min'])
                    if yesterday_ec < 2.8:
                        target_ml = yesterday_ml - 1 
                        if target_ml < 1:
                            target_ml = 1                    
                    elif yesterday_ec > 3.2:
                        target_ml = yesterday_ml + 1
                        if target_ml > 16:
                            target_ml = 16
                    else:
                        target_ml = yesterday_ml
                    self.indoor_env['irrigation_ml'] = target_ml
            else:
                if self.today == datetime(2024,9,29):
                    self.indoor_env['irrigation_ml'] = 8.3
                else:
                    yesterday_ml = self.indoor_env_yesterday['irrigation_ml'][-1]
                    yesterday_ec = sum(self.indoor_env_yesterday['drain_ec_5min'])/len(self.indoor_env_yesterday['drain_ec_5min'])
                    if yesterday_ec < 4.8:
                        target_ml = yesterday_ml - 1 
                        if target_ml < 1:
                            target_ml = 1                    
                    elif yesterday_ec > 5.2:
                        target_ml = yesterday_ml + 1
                        if target_ml > 16:
                            target_ml = 16
                    else:
                        target_ml = yesterday_ml
                    self.indoor_env['irrigation_ml'] = target_ml
        except:
            print("ec smart control algorithm error")
            if self.today < datetime(2024,9,19):
                self.indoor_env['irrigation_ml'] = 5
            else:
                self.indoor_env['irrigation_ml'] = 8.3

        
        # shot number 초기화

        self.plant_status = None
        
        self.green_input = GreenHouseInput(config=self.config,
                                           startdate=self.startdate,
                                           indoor_env=self.indoor_env,
                                           indoor_env_yesterday=self.indoor_env_yesterday,
                                           plant_status=self.plant_status,
                                           now=self.now)
        self.green_out = GreenHouseOutput(today=self.today)
       
        # self.green_cost = cost_calculate(self.green_input,self.density)
    
    def get_data_5min(self, date : datetime):
        df = self.lg_service.data_from_db_day(date)

        # 시작과 끝 시간을 가져옴
        start_time = df.index[0]
        end_time = df.index[-1]

        # 인덱스를 5분 간격으로 다시 생성
        new_index = pd.date_range(start=start_time, end=end_time.replace(hour=23, minute=55), freq='5T')

        # 기존 데이터프레임을 새로운 인덱스에 맞춰 리샘플링 및 보간
        df_resampled = df.reindex(new_index)
        df_resampled = df_resampled.interpolate(method='linear')

        # NaN값을 기존 데이터인 None으로 변경
        df_resampled = df_resampled.applymap(lambda x: None if pd.isna(x) else x)
        return df_resampled
      
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
        return self.green_out.setting_point

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
        self.config = config   

        self.indoor_env = indoor_env
        self.indoor_env_yesterday = indoor_env_yesterday
        self.plant_status = plant_status

        self.setpoint = self.indoor_env[LETSGROW_CONTROL]
        
        self.rise_time, self.set_time = sun_cal(self.today, self.indoor_env, True)
        
        self.rise_time_int = datetime_to_int(self.rise_time)
        self.set_time_int = datetime_to_int(self.set_time)
        self.now_int = datetime_to_int(self.now)
            
        # self.expected_DLI = get_DLI(self.indoor_env['fc_radiation_5min'],
        #                             transmittance=self.config["greenhouse_transmittance"],
        #                             type="watt")
        
        # self.current_DLI = get_DLI(self.indoor_env['outside_par_measurement_5min'],
        #                             transmittance=self.config["greenhouse_transmittance"],
        #                             window=[0,self.now_int],
        #                             energy_screen_array=self.indoor_env['sp_energy_screen_setpoint_5min'],
        #                             black_out_screen_array=self.indoor_env['sp_blackout_screen_setpoint_5min']
        #                             )
        
        self.density = generate_density_from_string(config['plant_density'], 200)
        
        # self.density = [ 56,56,56,56,56,56,56,56,56,56,56,56,56,56,
        #             56,56,56,56,56,56,56,56,56,56,56,56,56,56,
        #             56,56,56,42,42,42,42,42,42,42,42,42,42,42,
        #             30,30,30,30,30,30,30,30,30,30,20,20,20,20,
        #             20,20,20,20,20,20,20,20,20,20,20,20,20,20,
        #             20,20,20,20,20,20,20,20,20,20,20,20,20,20,
        #             20,20,20,20,20,20,20,20,20,20,20,20,20,20]
          
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
        self.setting_point = self.plant_model_init(today)
        self.global_info = {}

    def plant_model_init(self,today):
        index = pd.date_range(today, periods=288, freq='5min')
        columns = LETSGROW_CONTROL_WITH_EXTRA_PARAM
        return pd.DataFrame(index=index, columns=columns)

    def __str__(self) -> str:
        return F"""
            global_info => {self.global_info}
            setting_point => 
            {self.setting_point}
        """
        
