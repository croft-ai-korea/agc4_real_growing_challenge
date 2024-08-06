from datetime import datetime, timedelta

from typing import List
import os
import sys
import requests
import json
import pandas as pd
import numpy


sys.path.append('./')
from a_util.rest_api.letsgrow import LetGrow
from a_util.db.letsgrow_db_util import LetsgrowDao
from a_util.db.db_util import db_select_pandas_sql, db_select_pandas_sql_dict, db_select_one, db_insert,db_select_by_param
from a_util.letsgrow_const import GREENHOUSE_MODULE_ID, WEATHER_MODULE_ID, FORCAST_MODULE_ID
from aaaa.config import config


class LetsgrowService:
    def __init__(self):
        self.letgrow_id = config['letsgrow']['username']
        self.letgrows_pwd = config['letsgrow']['password']
        # self.letsgrow = LetGrow(self.letgrow_id, self.letgrows_pwd)
        self.letsgrow = None
        self.letsgrow_Dao = LetsgrowDao()

    def db_insert_day(self, list):
        print('-----------------', len(list))
        self.letsgrow_Dao.insert_day(list)

    def connect_letsgrow(self):
        if self.letsgrow == None:
            self.letsgrow = LetGrow(self.letgrow_id, self.letgrows_pwd)

    def GH_data_read(self, begin_time):
        rslt = self.letsgrow.read_all_values_oneday(GREENHOUSE_MODULE_ID, begin_time)
        return rslt

    def EXT_data_read(self, begin_time):
        return self.letsgrow.read_all_values_oneday(GREENHOUSE_MODULE_ID, begin_time)

    def FC_data_read(self, begin_time):
        return self.letsgrow.read_all_values_oneday(FORCAST_MODULE_ID, begin_time)

    def OUT_data_read(self, begin_time):
        return self.letsgrow.read_all_values_oneday(WEATHER_MODULE_ID, begin_time)

    def letsgrow_to_db_day(self, begin_time):
        self.connect_letsgrow()

        self.db_insert_day(self.GH_data_read(begin_time))
        # self.db_insert_day(self.EXT_data_read(begin_time))
        self.db_insert_day(self.FC_data_read(begin_time))
        self.db_insert_day(self.OUT_data_read(begin_time))

    def jsonbak_to_letsgrow(self, begin_time):
        with open('a_util/rest_api/save_control.json') as json_file:
            json_data = json.load(json_file)

        for data in json_data:
            data['TimeStamp'] = datetime.strptime(data['TimeStamp'],"%Y-%m-%dT%H:%M").replace(year=begin_time.year,month=begin_time.month,day=begin_time.day).strftime("%Y-%m-%dT%H:%M")
  
        self.connect_letsgrow()
        self.letsgrow.write_values(GREENHOUSE_MODULE_ID, json_data)
        
        with open('a_util/rest_api/save_control.json', 'w') as json_file:
            json.dump(json_data,json_file)

    def db_to_letsgrow(self, begin_time):
        self.connect_letsgrow()

        gh_values = self.letsgrow_Dao.getSetpoint(begin_time)
        # gh_values = self.letsgrow_Dao.getSetpointOfOneHour(begin_time)
        self.letsgrow.write_values(GREENHOUSE_MODULE_ID, gh_values)

    def pd_control_to_db(self, setpoint: pd.DataFrame):
        self.letsgrow_Dao.save_setpoint(setpoint)        
        # db_insert_pandas(control)

    def pd_control_to_db_hour(self, setpoint: pd.DataFrame):
        n = datetime.now()
        n2 = n + timedelta(hours=1)

        f_time = n.strftime("%H:00")
        t_time = n2.strftime("%H:00")

        setpoint = setpoint.between_time(f_time ,  t_time)
        print('------------------------')
        print(setpoint)


        self.letsgrow_Dao.save_setpoint(setpoint)
        # db_insert_pandas(control)

    def get_latest_date(self):
        return self.letsgrow_Dao.latest_date()
        

    def data_from_db_day(self, begin_time:datetime):
        return self.letsgrow_Dao.from_db_day(begin_time)

    def data_from_db(self, begin_time, end_time):
        return self.letsgrow_Dao.from_db(begin_time, end_time)

    def data_from_db_hour(self, begin_time, end_time):
        return self.letsgrow_Dao.from_db_hour(begin_time, end_time)



if __name__ == "__main__":

    lg = LetsgrowService()

    # from_date = lg.get_latest_date()
    # print('from_date', from_date)
    lg.letsgrow_to_db_day(datetime(2022,1,21))
    # lg.letsgrow_to_db_day(from_date)

    # data = lg.data_from_db_day(from_date)
