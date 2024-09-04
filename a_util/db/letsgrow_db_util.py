import warnings
from datetime import datetime, timedelta
from typing import List, Any

import pandas as pd

warnings.simplefilter(action='ignore', category=Warning)
pd.reset_option('all')

import psycopg2
import sys

sys.path.append('./')
from a_util.letsgrow_const import COLID_MAP_NAME, COLID_MAP_NUMBER, LETSGROW_CONTROL
from aaaa.config import config
from a_util.db.db_util import db_select_one, db_insert, db_select, db_select_pandas_sql_dict_real, db_select_pandas_sql, db_insert_many, db_select_by_param, db_select_pandas_sql_dict


def db_to_csv():
    CONNECTION = "postgres://postgres:admin1234@localhost:5432/postgres"

    with psycopg2.connect(CONNECTION) as conn:
        db_cursor = conn.cursor()

    sql = """ select * from measure"""

    # Use the COPY function on the SQL we created above.
    SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(sql)

    # Set up a variable to store our file path and name.
    with open('resultsfile.csv', 'w') as f:
        db_cursor.copy_expert(SQL_for_file_output, f)


timescale_config = config['timescale']
#
# _pool = None
#
# try:
#
#     _pool = psycopg2.pool.SimpleConnectionPool(1, 20,
#                                                user=timescale_config['username'],
#                                                password=timescale_config['password'],
#                                                host=timescale_config['host'],
#                                                port=timescale_config['port'],
#                                                database=timescale_config['db']
#                                                )
# except:
#     print('timescaledb connection error')


class LetsgrowDao:

    def save_setpoint(self,setpoint: pd.DataFrame):
        """
        dataframe
        """
        list_dict = setpoint.T.to_dict()

        # print('list_dict', list_dict)

        for key in list_dict:
           
            value_dict = list_dict[key]
            dataItem = { 'time':key, **value_dict } 
            sql = self.make_insert_sql_by_dict(dataItem)
            
            #print(sql)
            #print(dataItem)
            db_insert(sql,dataItem)

    def insert_day(self, l:List[Any]):
        if len(l) < 1:
            print('no data!')
            return

    
        _datas = self.value_grouping(l)
        sql = self.make_insert_sql_by_dict(_datas[0])

        
        print('sql', sql)

        # db_insert_many(sql, _datas)

        for anItem in _datas:
            sql = self.make_insert_sql_by_dict(anItem)
            db_insert(sql, anItem)

    def insert_day_bakup(self, data):
        if ('Message' in data):
            print(data)
        else:
            dic = {}
            for key in data:
                dic = {"time": key['TimeStamp']}
                data = str(COLID_MAP_NUMBER[str(key['ColId'])])
                dic.update({data: key['Value']})
                sql = '''
                INSERT INTO measure ("time", ''' + data + ''')
                VALUES( %(time)s, %(''' + data + ''')s) 
                ON CONFLICT (time) 
                DO 
                UPDATE SET ''' + data + ''' = %(''' + data + ''')s
                '''
                # print(dic)
                # print(sql)
                db_insert(sql, dic)
                dic = {}
                # print("time = {}".format(key['TimeStamp']))

    def value_grouping(self,list):
        xlist = sorted(list, key=lambda v: v['TimeStamp'])

        result = []
        cur_tm = xlist[0]['TimeStamp']
        tmp_dict = {'time': cur_tm}

        for item in xlist:
            # print(item)
            if cur_tm != item['TimeStamp']:
                result.append(tmp_dict)
                cur_tm = item['TimeStamp']
                tmp_dict = {'time': cur_tm}

            if str(item['ColId']) in COLID_MAP_NUMBER:
                tmp_dict[COLID_MAP_NUMBER[str(item['ColId'])]] = item['Value']

        result.append(tmp_dict)

        # print('result', result)

        return result

    def getSetpointOfOneHour(self, begin_time) -> List[dict]:
        # to-do modify query
        sql = f""" 
                SELECT 
                    time,heating_temp_sp,vent_temp_sp,net_pipe_sp,lee_vent_min_sp,
                    scr_enrg_sp,scr_blck_sp,lamps_sp,co2_sp,dx_sp ,plant_density,day_of_harvest
                from measure 
                where 
                    time >= %(f)s
                    and time < %(t)s
        """

        get_db = db_select_by_param(sql , {'f':begin_time ,'t': begin_time + timedelta(hours=1)})
        # print(get_db)
        gh_list = []
        for dic in get_db:
            time = dic['time'].strftime("%Y-%m-%dT%H:%M")
            for key in dic:
                # print('### key', key)
                if (key == 'time' or dic[key] != dic[key] or dic[key] == None):
                    pass
                else:
                    if (dic[key] == None):
                        print("key = {}, value = {}, type = {}".format(key, dic[key], type(dic[key])))

                    dic_value = {
                        "colId": COLID_MAP_NAME[key],
                        "TimeStamp": time,
                        "Value": dic[key],
                        "Offset": 0
                    }
                    gh_list.append(dic_value)
        return gh_list


        pass

    def getSetpoint(self, begin_time) -> List[List[dict]]:
        # to-do modify query
        
        setpoints = ",".join(LETSGROW_CONTROL)
        
        sql = f""" 
                SELECT 
                    time,{setpoints}
                from measure 
                where 
                    time >= %(f)s
                    and time < %(t)s
        """

        get_db = db_select_by_param(sql , {'f':begin_time ,'t': begin_time + timedelta(days=1)})
        # print(get_db)
        gh_list = []
        for dic in get_db:
            time = dic['time'].strftime("%Y-%m-%dT%H:%M")
            for key in dic:
                # print('### key', key)
                if (key == 'time' or dic[key] != dic[key] or dic[key] == None): #or COLID_MAP_NAME[key] == 1593865):
                    pass
                else:
                    if (dic[key] == None):
                        print("key = {}, value = {}, type = {}".format(key, dic[key], type(dic[key])))

                    dic_value = {
                        "colId": COLID_MAP_NAME[key],
                        "TimeStamp": time,
                        "Value": dic[key],
                        "Offset": 0
                    }
                    gh_list.append(dic_value)
                    #if(key=='scr_enrg_sp' or key=='scr_blck_sp'):
                    #    print("key = {} and value = {}".format(key,dic[key]))
        return gh_list

    def latest_date(self):
        from_date_sql = '''
                select min(tm) from (
                    select max(time) as tm
                    from measure
                    where outside_temperature_5min is not null
                    union
                    select (now() at time zone 'Europe/Amsterdam') - interval '0 hour' as tm
                ) tbl
            '''
        return db_select_one(from_date_sql)

    def from_db_day(self, begin_time: datetime):
        sql = " SELECT * from measure where time >= %(f)s and time < %(t)s "
        return db_select_pandas_sql_dict(sql, {'f': begin_time, 't': begin_time + timedelta(days=1)})


    def from_db(self, begin_time: datetime, end_time: datetime):
        sql = " SELECT * from measure where time >= '" + begin_time.strftime(
            "%Y-%m-%dT%H:%M:%S") + "' and time < '" + end_time.strftime("%Y-%m-%dT%H:%M:%S") + "'"

        return db_select_pandas_sql(sql)
    
    def from_db_specific_columns(self, begin_time: datetime, end_time: datetime, columns:str):
        sql = f" SELECT \"{columns}\", \"time\" from measure where time >= '" + begin_time.strftime(
        "%Y-%m-%dT%H:%M:%S") + "' and time < '" + end_time.strftime("%Y-%m-%dT%H:%M:%S") + "'"

        return db_select_pandas_sql(sql)

    def from_db_hour(self, begin_time, end_time):
        sql = """ SELECT time_bucket('1 hour', time) AS tm
        FROM measure
        where time >= '""" + begin_time.strftime("%Y-%m-%dT%H:%M:%S") + """' and time <  '""" + end_time.strftime(
            "%Y-%m-%dT%H:%M:%S") + """'
        GROUP BY tm
        ORDER BY tm
        """
        print(sql)
        return db_select_pandas_sql(sql)

    def make_insert_sql_by_dict(self, anItem):
        colNames = ",".join([k for k in anItem])
        values = ",".join(['%(' + k + ')s' for k in anItem])
        updates = ",".join([f"{k} = %({k})s " for k in anItem][1:])

        return f"""
            INSERT INTO measure ( {colNames} )
            VALUES ( {values})
            ON CONFLICT (time) DO UPDATE SET
            {updates}
        """

if __name__ == "__main__":
    pass

