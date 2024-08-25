import datetime
from typing  import List
import requests
import json
import re
import pandas as pd
from pandas import DataFrame
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
# import plotly.express as px
from datetime import timedelta, datetime
from random import random
import numpy as np
import copy

def parse_simulation_data(simulation_data):
    simulation_days = []
    plant_densities = []
    
    # 데이터를 세미콜론으로 분할
    entries = simulation_data.split(';')
    
    for entry in entries:
        day, density = entry.strip().split()
        simulation_days.append(int(day))
        plant_densities.append(int(density))
    
    return simulation_days, plant_densities

def generate_density_from_string(simulation_data, total_days):
    simulation_days, plant_densities = parse_simulation_data(simulation_data)
    
    density = []
    
    # 시작 시점과 끝 시점을 만들어, 각각의 기간에 해당하는 density값을 추가
    for i in range(len(simulation_days) - 1):
        start_day = simulation_days[i]
        end_day = simulation_days[i + 1]
        density.extend([plant_densities[i]] * (end_day - start_day))
    
    # 마지막 density값을 나머지 일자에 대해 채움
    density.extend([plant_densities[-1]] * (total_days - simulation_days[-1] + 1))
    
    return density

def generate_simulation_string(density_list):
    simulation_data = []
    current_density = density_list[0]
    start_day = 1

    for i in range(1, len(density_list)):
        if density_list[i] != current_density:
            simulation_data.append(f"{start_day} {current_density}")
            current_density = density_list[i]
            start_day = i + 1

    # 마지막 density값을 추가
    simulation_data.append(f"{start_day} {current_density}")

    return "; ".join(simulation_data)

def convert_key_from_start_date(setting_point, start_date):
    setting_point_to_server = {}
    start_date_time = datetime.strptime(start_date, "%d-%m-%Y")
    for key, value in setting_point.items():
        today = start_date_time + timedelta(days=key)
        setting_point_to_server[today.strftime("%d-%m")] = value
    return setting_point_to_server

# random search
def modify_temperature(heatingTemp:dict, temp_diff:list = None):
    if temp_diff is not None and len(temp_diff) == len(heatingTemp):
        for key, val in heatingTemp.items():
            val['0'] += temp_diff[key][0]
            val['r-2'] += temp_diff[key][1]
            val['r'] += temp_diff[key][2]
            val['13'] += temp_diff[key][3]
            val['s'] += temp_diff[key][4]
            val['s+2'] += temp_diff[key][5]
            val['23'] += temp_diff[key][6]
    else:
        print("wrong size of temp_diff")

def modify_intensity(intensity:float, intensity_diff:float = 15.0):
    return intensity * intensity_diff

def modify_hours_light(hours_light:dict, hour_diff:list = None):
    if hour_diff is not None and len(hour_diff) == len(hours_light):
        for key, val in hours_light.items():
            hours_light[key] += hour_diff[key]            
            if hours_light[key] > 20:
                hours_light[key] = 20

# random search
def modify_temperature_random(heatingTemp:dict, night_range = 1, day_range = 2):
    night_temp_diff = (1-random()*2)*night_range
    day_temp_diff = (1-random()*2)*day_range
    for key, val in heatingTemp.items():
        val['0'] += night_temp_diff
        val['r-2'] += night_temp_diff
        val['r'] += day_temp_diff
        val['13'] += day_temp_diff
        val['s'] += day_temp_diff
        val['s+2'] += night_temp_diff
        val['23'] += night_temp_diff

def modify_intensity_random(intensity:float, intensity_range:float = 15):
    return intensity + (1-random()*2)*intensity_range

def modify_hours_light_random(hours_light:dict, hour_range = 2):
    hours_light_diff_s1 = (1-random()*2)*hour_range
    hours_light_diff_s2 = (1-random()*2)*hour_range
    hours_light_diff_s3 = (1-random()*2)*hour_range
    hours_light_diff_s4 = (1-random()*2)*hour_range
    hours_light_diff_s5 = (1-random()*2)*hour_range
    hours_light_diff_s6 = (1-random()*2)*hour_range

    hours_light['05-09'] += hours_light_diff_s1
    hours_light['19-09'] += hours_light_diff_s2
    hours_light['03-10'] += hours_light_diff_s3
    hours_light['17-10'] += hours_light_diff_s4
    hours_light['31-10'] += hours_light_diff_s5
    hours_light['14-11'] += hours_light_diff_s6

    for key, val in hours_light.items():
        if val > 20:
            hours_light[key] = 20
    
def ole2date(x):
    OLE_TIME_ZERO = datetime(1899, 12, 30, 0, 0, 0)
    return OLE_TIME_ZERO + timedelta(days=float(x))

def send_server(parameters:dict, 
                response_json_save_path:str = None):
    '''
    그린하우스 서버에 json 파일을 전달하고 피드백을 받습니다.
    :param parameterFile: 서버로 보낼 json 파일 (to_json2 함수를 거친 후 보내준다)
    :param episode: 날짜, 숫자 정보 (파일 저장할 때 사용)
    :return: 서버로 부터 받은 json 파일을 판다스로 변환 후 반환 합니다.
    '''
    key = 'AgriFusion-A-uaw1-lnd9'  # simulator A key
    # key = 'AgriFusion-B-uaw1-lnd9'  # simuklator B key

    url = 'https://www.digigreenhouse.wur.nl/AGC2024/model/kaspro'

    parameters = {"key": key, "parameters": parameters}

    response = requests.post(url, data=parameters, timeout=300)
    output_json = response.json()

    if response_json_save_path is not None:
        with open(response_json_save_path, 'w') as file:
            json.dump(output_json, file, indent=4)

    return output_json

def json_parsing(response_json_path:str, response_csv_path:str = None):
    '''
    json 파일 -> Pandas
    :param episode: 날짜, 숫자 정보 (파일 저장할 때 사용)
    :return:  json 파일을 판다스로 변환하여 반환 합니다. 이때 변경된 파일은 csv 파일로도 저장이 됩니다.
    '''
    with open(response_json_path, 'r') as f:
       json_data = json.load(f)
    df = pd.json_normalize(json_data)
    output_data = pd.DataFrame(df['data.DateTime.data'].tolist()).T

    for key in df:
        if (key.split(".")[-1] == "data"):
            output_data[re.sub("data.|.data", "", key)] = pd.DataFrame(df[key].tolist()).T
        elif (key.split(".")[0] == "stats"):
            output_data[re.sub("stats.", "", key)] = pd.DataFrame(df[key].tolist()).T

    output_data = output_data.drop(0, axis=1)
    output_data['DateTime'] = output_data['DateTime'].apply(lambda x: ole2date(x))
    output_data.set_index("DateTime", inplace=True)
    output_data = round_up_minutes(output_data)

    if response_csv_path is not None:
        output_data.to_csv(response_csv_path)

    return output_data
    #return output_data['comp1.Air.T'].median(), output_data['comp1.TPipe1.Value'].median(), output_data['comp1.Setpoints.SpHeat'].median(), output_data['economics.gains.objects.product'][0]
    #return output_data['common.Iglob.Value'].median(), output_data['comp1.PARsensor.Above'].median(), output_data['comp1.Lmp1.ElecUse'].median(), output_data['economics.gains.objects.product'][0]
    #return output_data['comp1.ConWin.WinLee'].median(), output_data['comp1.ConWin.WinWnd'].median(), output_data['comp1.Setpoints.SpVent'].median(), output_data['economics.balance'][0]
    #return output_data['comp1.Air.ppm'].median(), output_data['comp1.McPureAir.Value'].median(), output_data['comp1.Plant.headFW'].median(), output_data['economics.balance'][0]


def round_up_minutes(df):
    """ Rounds up all the minutes in the DataFrame's DatetimeIndex """
    # Function to round up the minute of a single datetime
    def round_up_minute(dt):
        # Check if already rounded (i.e., seconds and microseconds are zero)
        if dt.minute < 30:
            return dt.replace(minute=0, second=0, microsecond=0)
        else:
            # Add one minute and zero out the seconds and microseconds
            return dt.replace(minute=0, second=0, microsecond=0) + pd.DateOffset(hours=1)

    # Check if the index is a DatetimeIndex
    if isinstance(df.index, pd.DatetimeIndex):
        # Apply the rounding function to each datetime in the index
        df.index = df.index.map(round_up_minute)
    else:
        raise ValueError("DataFrame index is not a DatetimeIndex.")
    return df

class sim_greenhouse:
    def __init__(self, greenhouse_data, control_json_path = None):
        self.greenhouse_data = greenhouse_data
        if control_json_path is not None:
            with open(control_json_path, 'r') as f:
                self.control_data = json.load(f)       

        self.endDate = get_endDate_from_output(self.greenhouse_data, convert_str=False)       
        self.greenhouse_data_crop = self.greenhouse_data[self.greenhouse_data.index <= self.endDate]

    def get_Date(self,number_date = 1) -> datetime:
        """ Returns the datetime entry in the DataFrame's index. """
        return pd.Timestamp(self.greenhouse_data.index[(number_date-1)*24]).to_pydatetime()

    def get_Date_str(self,number_date = 1) -> str:
        """ Returns the date as a string from the index, adjusted by number_date. """
        datetime_obj = pd.Timestamp(self.greenhouse_data.index[(number_date-1)*24]).to_pydatetime()
        format_str = '%Y-%m-%d'
        return datetime_obj.strftime(format_str)

    def get_data_by_date(self, dates) -> pd.DataFrame:
        """
        Filters the DataFrame for the given date(s).

        Args:
        dates (str or list): A single date string or a list of date strings.

        Returns:
        pd.DataFrame: A DataFrame containing data for the specified dates.
        """
        # Ensure the index is a datetime index
        self.greenhouse_data.index = pd.to_datetime(self.greenhouse_data.index)

        if isinstance(dates, list):
            # Filter for multiple dates
            return self.greenhouse_data[self.greenhouse_data.index.normalize().isin(pd.to_datetime(dates).normalize())]
        else:
            # Filter for a single date
            return self.greenhouse_data.loc[self.greenhouse_data.index.normalize() == pd.to_datetime(dates).normalize()]

    def get_weather_by_date(self, dates) -> pd.DataFrame:
        """
        Extracts specific weather-related columns for given date(s).

        Args:
        dates (str or list): A single date or a list of dates.

        Returns:
        pd.DataFrame: A DataFrame with selected columns for the specified date(s).
        """
        weather_col = ['common.Iglob.Value', 'common.Tout.Value', 'common.RHout.Value', 'common.Windsp.Value', 'comp1.PARsensor.Above']
        data_by_date = self.get_data_by_date(dates)
        return data_by_date[weather_col]

    def get_fixed_cost(self):
        fixed_cost_col = ['economics.fixedCosts.objects.comp1.Lmp1', 'economics.fixedCosts.objects.comp1.Scr1', 'economics.fixedCosts.objects.comp1.Scr2', 'economics.fixedCosts.objects.comp1.ConCO2', 'economics.fixedCosts.objects.spacingSystem','economics.fixedCosts.total']
        return self.greenhouse_data[fixed_cost_col].iloc[0]

    def get_variable_cost(self):
        variable_cost_col = ['economics.variableCosts.objects.gas', 'economics.variableCosts.objects.elec', 'economics.variableCosts.objects.CO2', 'economics.variableCosts.objects.plants', 'economics.variableCosts.total']
        return self.greenhouse_data[variable_cost_col].iloc[0]

    def get_profit(self):
        profit_col = ['economics.gains.objects.product', 'economics.gains.total', 'economics.balance']
        return self.greenhouse_data[profit_col].iloc[0]

    def report_profit(self):
        report_col = ['economics.fixedCosts.total','economics.variableCosts.total','economics.gains.total']
        report_pd = self.greenhouse_data[report_col].iloc[0]

        print("Gain: {} - Fixedcost: {} - VariableCost: {} = balance: {}".format(report_pd[2],report_pd[0],report_pd[1],(report_pd[2]-report_pd[0]-report_pd[1]).round(3)))
    
    def compare_par(self,p2,p_list):
        '''
        파라미터 비교 함수 (compare_par('10_02.30',c_p)
        :param p2: 비교 원하는 날짜
        :param p_list: 비교 원하는 파라미터 ex. c_p=['comp1.Air.T','comp1.TPipe1.Value','economics.balance']
        :return: 결과는 print 로 출력 된다
        '''
        print("----Compare two datas----")
        pandas_1 = self.greenhouse_data
        pandas_2 = json_parsing(p2)

        dic_var =dict.fromkeys(p_list, None)
        for i, val in enumerate(p_list):
            dic_var[list(dic_var.keys())[i]] = pandas_1[p_list[i]].median() - pandas_2[p_list[i]].median()
            if(pandas_1[p_list[i]].median() - pandas_2[p_list[i]].median()) > 0:
                bigger_result = "My data result"
            else:
                bigger_result = p2
            print("{} is bigger! ,{} - mean of different is {}".format(bigger_result,p_list[i],pandas_1[p_list[i]].median() - pandas_2[p_list[i]].median()))

    def mean_par(self,p_list):
        '''
        파라미터 값 확인 (mean_par("11_07.11.11',c_p)
        :param p1: 확인 원하는 날짜
        :param p_list: 비교 원하는 파라미터 ex. c_p= ['comp1.Air.T','comp1.TPipe1.Value','economics.balance']
        :return: 결과는 print 로 출력 된다
        '''
        print("----Mean Parameters----")
        dic_var =dict.fromkeys(p_list, None)
        for i, val in enumerate(p_list):
            dic_var[list(dic_var.keys())[i]] = self.greenhouse_data[p_list[i]].median()

            if(p_list[i] == 'economics.variableCosts.objects.comp1.Pipe1' or p_list[i] == 'economics.gains.objects.product'):
                print("{} - mean of value is {}".format(p_list[i], self.greenhouse_data[p_list[i]][0]))
            elif(p_list[i]=='comp1.Plant.shootDryMatterContent'):
                print("{} - value is {}".format(p_list[i], self.greenhouse_data[p_list[i]][-1]))
            elif(p_list[i]=='comp1.Growth.FruitFreshweight'):
                print("{} - max value is {}".format(p_list[i], self.greenhouse_data[p_list[i]][-1]))
            else:
                print("{} - mean of value is {}".format(p_list[i],self.greenhouse_data[p_list[i]].median()))

    def graph1(self):
        after_pandas = self.greenhouse_data

        # Calculate daily medians and store in a DataFrame
        daily_data = pd.DataFrame(index=after_pandas.index.strftime("%Y-%m-%d").drop_duplicates())
        daily_data['T_means'] = after_pandas['comp1.Air.T'].groupby(after_pandas.index.strftime("%Y-%m-%d")).median()
        daily_data['C_means'] = after_pandas['comp1.Air.ppm'].groupby(after_pandas.index.strftime("%Y-%m-%d")).median()
        daily_data['L_means'] = (after_pandas['comp1.PARsensor.Above'].groupby(
            after_pandas.index.strftime("%Y-%m-%d")).median() * 24 * 3600 / 1000000)
        daily_data['headFW'] = after_pandas['comp1.Growth.FruitFreshweight'].groupby(
            after_pandas.index.strftime("%Y-%m-%d")).median()

        # Calculating overall means for each column
        overall_means = daily_data.mean()

        # Creating a bar graph of the overall means using Plotly
        fig = go.Figure([go.Bar(x=['T_means', 'C_means', 'L_means', 'headFW'], y=overall_means,
                                marker_color=['blue', 'green', 'red', 'purple'])])
        fig.update_layout(title='Overall Mean Values of Different Measurements',
                          xaxis_title='Measurement Type',
                          yaxis_title='Mean Value')
        fig.show()

        # Plotting multiple lines on a single graph with labels and a legend using Plotly
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=after_pandas['common.Tout.Value'].index, y=after_pandas['comp1.Setpoints.SpHeat'], mode='lines',
                       name='SpHeat', line=dict(color='red')))
        fig.add_trace(
            go.Scatter(x=after_pandas['common.Tout.Value'].index, y=after_pandas['comp1.Setpoints.SpVent'], mode='lines',
                       name='SpVent', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=after_pandas['common.Tout.Value'].index, y=(after_pandas['comp1.PARsensor.Above'] / 10),
                                 mode='lines', name='PARsensor Above', line=dict(color='blue')))
        fig.update_layout(title='Setpoints and PARsensor Readings Over Time',
                          xaxis_title='Date',
                          yaxis_title='Values',
                          legend_title='Variable')
        fig.show()

    def temp_sorting2(self,temp_set,max_par,bco2):
        '''
        온도 제어 알고리즘
        :param temp_set: 설정 원하는 온도
        :param max_par: 설정 온도 대비 max_par 값 결정 (높을 수록 온도를 더 잘 맞추지만 비용이 올라갑니다. 40~60 정도가 괜챃습니다.)
        :param bco2: co2 조건값
        :return: 온도 정보, Max 온도 정보 추후 control 판다스에 넣어주면 됩니다.
        '''
        '''
        현재 로직 - 
        1) 각 날짜 별 평균 온도를 구함
        2) temp_diff(ex. 2도) 온도차를 기준 으로 그룹 묶음
        3) 그룹내 시간대별 온도 평균 구함
        4) 난방기 온도 = 각 시간대별 온도 평균 + temp_set (ex. 22도를 만들기 위해서 난방은 29도 설정)
        5) 이때 temp_var(ex. 9도) 이상 온도는 히터를 끈다 (전기세 위하여)
        '''

        #평균온도 9도 이하에서만 히터를 튼다
        temp_var = 9
        #22도 - 평균 온도 만큼 설정한다
        temp_set = temp_set+1
        # 온도 차이에 따라 분류한다
        temp_diff = 1.5

        # Co2 차이로 분류한다
        iglob_diff = 1

        #booster CO2
        #bco2 = 100

        iglob_means = pd.DataFrame(columns=['means'], index=self.greenhouse_data.index.strftime("%Y-%m-%d").drop_duplicates())

        # A) 각 날짜 별 평균 태양열 값을 구함
        for key in self.greenhouse_data.index.strftime("%Y-%m-%d").drop_duplicates():
            iglob_means.loc[key] = self.greenhouse_data['common.Iglob.Value'][key].median()

        #exit()

        list22_val = []

        list_val2 = []
        list22_val2 = []
        old_val2 = 0

        trig_c2 = True

        # B) iglob_diff 태양열 차이를 기준으로 그룹 묶음
        for key, value in iglob_means['means'].iteritems():
            if(trig_c2 == True):
                old_key2 = key
                trig_c2 = False
                old_val2 = value
            if(abs(old_val2 - value) > abs(iglob_diff)):
                trig_c2 = True
                list22_val.append(self.greenhouse_data[old_key2:key]['common.Tout.Value'])
                list_val2.append(old_key2[-2:] + '-' + key[-5:-3])
                list22_val2.append(self.greenhouse_data[old_key2:key]['common.Iglob.Value'])
            #print("key = {}, value = {}, old_key = {}, old_val = {}".format(key,value,old_key2,old_val2))

        dic_var2 = dict.fromkeys(list_val2, None)
        dic_var_max2 = dict.fromkeys(list_val2, None)
        dic_var_co2 = dict.fromkeys(list_val2, None)

        FGFG2  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        FGFG2_temp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        FGFG2_max = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        FGFG2_co2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        #print(list22_val2)
        # 3) 그룹내 시간대별 iglob_diff 평균 구한 후
        for i, val in enumerate(list22_val2):
            for j, j_val in enumerate(list22_val2[i]):
                #print("j_val = {},  list22_val = {}".format(j_val,list22_val))
                c = divmod(j, 24)[1]
                FGFG2[c] = FGFG2[c] + j_val
                FGFG2_temp[c] = FGFG2_temp[c] = list22_val[i][j]
                # print("FGFG = {}, j_val = {}".format(FGFG[c],j_val))

            # print(list(dic_var.keys())[i])

            for j, j_val in enumerate(FGFG2):
                # print(FGFG[j] / (len(list22_val[i])/24))
                if ((FGFG2[j] / (len(list22_val2[i]) / 24)) > bco2*2):
                    FGFG2[j] = 25#30
                    FGFG2_max[j] = 75
                    if((datetime.strptime(list(dic_var2.keys())[i], "%d-%m") - datetime.strptime("04-03","%d-%m")).days<14):
                        FGFG2_co2[j] = 350
                    else:
                        FGFG2_co2[j] = 1050
                    FGFG2_co2[j] = 1050
                elif((FGFG2[j] / (len(list22_val2[i]) / 24)) > bco2):
                    FGFG2[j] = 24 #28
                    FGFG2_max[j] = 75
                    if((datetime.strptime(list(dic_var2.keys())[i], "%d-%m") - datetime.strptime("04-03","%d-%m")).days<14):
                        FGFG2_co2[j] = 350
                    else:
                        FGFG2_co2[j] = 1000
                    FGFG2_co2[j] = 950
                else:
                    # print("FGFG[{}] = {}, len(list22_val[i] = {}, total = {}".format(j,FGFG[j],FGFG[j]/(len(list22_val[i])/24),temp_set -FGFG[j]/(len(list22_val[i])/24)))
                    FGFG2[j] = temp_set - round(FGFG2_temp[j] / (len(list22_val[i]) / 24), 2)
                    FGFG2_max[j] = FGFG2[j] + max_par
                    if((datetime.strptime(list(dic_var2.keys())[i], "%d-%m") - datetime.strptime("04-03","%d-%m")).days<14):
                        FGFG2_co2[j] = 350
                    else:
                        FGFG2_co2[j] = 850
                    FGFG2_co2[j] = 850

            dic_var2[list(dic_var2.keys())[i]] = {"1": FGFG2[0], "2": FGFG2[1], "3": FGFG2[2], "4": FGFG2[3], "5": FGFG2[4],"6": FGFG2[5], "7": FGFG2[6], "8": FGFG2[7], "9": FGFG2[8],"10": FGFG2[9], "11": FGFG2[10], "12": FGFG2[11], "13": FGFG2[12],"14": FGFG2[13], "15": FGFG2[14], "16": FGFG2[15], "17": FGFG2[16],"18": FGFG2[17], "19": FGFG2[18], "20": FGFG2[19], "21": FGFG2[20],"22": FGFG2[21], "23": FGFG2[22]}
            dic_var_max2[list(dic_var2.keys())[i]] = {"1": FGFG2_max[0], "2": FGFG2_max[1], "3": FGFG2_max[2],"4": FGFG2_max[3], "5": FGFG2_max[4], "6": FGFG2_max[5],"7": FGFG2_max[6], "8": FGFG2_max[7], "9": FGFG2_max[8],"10": FGFG2_max[9], "11": FGFG2_max[10], "12": FGFG2_max[11],"13": FGFG2_max[12], "14": FGFG2_max[13], "15": FGFG2_max[14],"16": FGFG2_max[15], "17": FGFG2_max[16], "18": FGFG2_max[17],"19": FGFG2_max[18], "20": FGFG2_max[19], "21": FGFG2_max[20],"22": FGFG2_max[21], "23": FGFG2_max[22]}
            dic_var_co2[list(dic_var2.keys())[i]] = {"1": FGFG2_co2[0], "2": FGFG2_co2[1], "3": FGFG2_co2[2],"4": FGFG2_co2[3], "5": FGFG2_co2[4], "6": FGFG2_co2[5],"7": FGFG2_co2[6], "8": FGFG2_co2[7], "9": FGFG2_co2[8],"10": FGFG2_co2[9], "11": FGFG2_co2[10], "12": FGFG2_co2[11],"13": FGFG2_co2[12], "14": FGFG2_co2[13], "15": FGFG2_co2[14],"16": FGFG2_co2[15], "17": FGFG2_co2[16], "18": FGFG2_co2[17],"19": FGFG2_co2[18], "20": FGFG2_co2[19], "21": FGFG2_co2[20],"22": FGFG2_co2[21], "23": FGFG2_co2[22]}
            FGFG2 = [0]*24
            FGFG2_max = [0]*24
            FGFG2_co2 = [0]*24

        #exit()
        return [dic_var2 , dic_var_max2, dic_var_co2]
    
    def get_analysis_data(self, spacing_change, screen_num): 
        datetime_index = self.greenhouse_data_crop.index
        filtered_index = datetime_index[datetime_index.hour == 15]
        endDate = filtered_index[-1]
        total_days = (filtered_index[-1] - filtered_index[0]).days+1
        filtered_data = self.greenhouse_data_crop.loc[filtered_index]
        freshWeightList = filtered_data['comp1.Growth.FruitFreshweight']        
        dryMatterPercentage = filtered_data['comp1.Growth.DryMatterFract'].iloc[-1]      
        densityList = filtered_data['comp1.Growth.PlantDensity']
        AveragePotPerM2 = (total_days) / sum( 1/densityList ) 
        fractionOfYear = total_days / 365   
        price_per_head = self.get_price_per_head(freshWeightList.iloc[-1], dryMatterPercentage)
        total_gain_estimate = AveragePotPerM2 * price_per_head
        
        # if dryMatterPercentage>0.08:
        #     total_gain_estimate = AveragePotPerM2 * 1.9
        # elif dryMatterPercentage < 0.07:
        #     total_gain_estimate = AveragePotPerM2 * 1.7
        # else:
        #     total_gain_estimate = AveragePotPerM2 * (1.7 + 20*(dryMatterPercentage-0.07))  
        lamp_fixed_costs = {
            'lmp_LED23' : 0.04, 'lmp_LED27' : 0.07, 'lmp_LED29' : 0.09, 'lmp_LED30' : 0.12, 'lmp_LED32' : 0.14
        }

        # print(f"final fresh weight : {freshWeightList.iloc[-1]}  total days : {total_days} start_date : {filtered_index[0]}")
        
        PlantCosts_per_head = 0.90
        yearly_greenhouse_cost = 40.0
        Electric_cost_onpeak = 0.15
        Electric_cost_offpeak = 0.10
        
        # PlantCosts_per_head = 1.00
        # yearly_greenhouse_cost = 30.0
        # Electric_cost_onpeak = 0.15
        # Electric_cost_offpeak = 0.10
        
        # PlantCosts_per_head = 0.75
        # yearly_greenhouse_cost = 15.0
        # Electric_cost_onpeak = 0.30
        # Electric_cost_offpeak = 0.20
        
        greenHouseCosts = fractionOfYear * yearly_greenhouse_cost
        PlantCosts = PlantCosts_per_head*AveragePotPerM2
        FixedCO2Costs = self.control_data['common']['CO2dosing']['@pureCO2cap']*0.015*fractionOfYear        
        FixedLampCosts = self.control_data['comp1']['illumination']['lmp1']['@intensity']*lamp_fixed_costs[self.control_data['comp1']['illumination']['lmp1']['@type']]*fractionOfYear       
        FixedScreenCosts = screen_num*1.00* fractionOfYear
        SpacingCosts = spacing_change * 1.50 * fractionOfYear
        try:
            OnPeakElec = sum(self.greenhouse_data_crop['comp1.Lmp1.ElecUse'] * (self.greenhouse_data_crop['common.ElecPrice.PeakHour']>0.5))/1000 
            OffPeakElec = sum(self.greenhouse_data_crop['comp1.Lmp1.ElecUse'] * (self.greenhouse_data_crop['common.ElecPrice.PeakHour']<=0.5))/1000
            ElectricityCosts = (OnPeakElec * Electric_cost_onpeak + OffPeakElec * Electric_cost_offpeak)
        except:
            ElectricityCosts = 0
        HeatingCosts = sum(self.greenhouse_data_crop['comp1.PConPipe1.Value'])/1000*0.09
        try:
            CO2Costs = sum(self.greenhouse_data_crop['comp1.McPureAir.Value'])*3600*0.30
        except:
            CO2Costs = 0                  
        Balance = total_gain_estimate - FixedCO2Costs - FixedLampCosts - FixedScreenCosts \
            - SpacingCosts - ElectricityCosts - HeatingCosts - CO2Costs - PlantCosts - greenHouseCosts
        TotalCost = FixedCO2Costs + FixedLampCosts + FixedScreenCosts + SpacingCosts \
              + ElectricityCosts + HeatingCosts + CO2Costs + PlantCosts + greenHouseCosts
        
        # print("end_data : ", endDate)data_cro
        # print("gain_total : ",  greenhouse_data_crop['economics.gains.total'].iloc[0], total_gain_estimate)
        # print("average_density : ", greenhouse_data_crop['economics.info.averageDensity'].iloc[0],  AveragePotPerM2)
        # print("PlantCosts : ", greenhouse_data_crop['economics.variableCosts.objects.plants'].iloc[0],  PlantCosts)
        # print("fractionOfYear : ", greenhouse_data_crop['economics.info.fractionOfYear'].iloc[0],  fractionOfYear)
        # print("greenhouseOccupation : ", greenhouse_data_crop['economics.fixedCosts.objects.comp1.Greenhouse'].iloc[0],  greenhouseOccupation)
        # print("FixedCO2Costs : ", greenhouse_data_crop['economics.fixedCosts.objects.comp1.ConCO2'].iloc[0], FixedCO2Costs)
        # print("FixedLampCosts : ", greenhouse_data_crop['economics.fixedCosts.objects.comp1.Lmp1'].iloc[0], FixedLampCosts)
        # print("FixedScreenCosts : ", greenhouse_data_crop['economics.fixedCosts.objects.comp1.Scr1'].iloc[0]*2, FixedScreenCosts)
        # print("SpacingCosts : ", greenhouse_data_crop['economics.fixedCosts.objects.spacingSystem'].iloc[0], SpacingCosts)
        # print("ElectricityCosts : ", greenhouse_data_crop['economics.variableCosts.objects.elec'].iloc[0], ElectricityCosts)
        # print("HeatingCosts : ", greenhouse_data_crop['economics.variableCosts.objects.gas'].iloc[0], HeatingCosts)
        # print("CO2Costs : ", greenhouse_data_crop['economics.variableCosts.objects.CO2'].iloc[0], CO2Costs)
        # print("greenHouseCosts : ", greenhouse_data_crop['economics.fixedCosts.objects.comp1.Greenhouse'].iloc[0], greenHouseCosts)
        # print("Balance : ", greenhouse_data_crop['economics.balance'].iloc[0], Balance)        
        
        first_freshweight_date = freshWeightList[freshWeightList>0].index[0]
        
        return_value = {
            'Balance' : Balance,
            'total_gain_estimate' : total_gain_estimate,
            'TotalCost' : TotalCost,
            'total_days' : total_days,
            'first_freshweight_date' : first_freshweight_date,
            'gain' : total_gain_estimate,
            'fixedCosts' : FixedCO2Costs + FixedLampCosts + FixedScreenCosts + SpacingCosts + greenHouseCosts,
            'FixedCO2Costs' : FixedCO2Costs,
            'FixedLampCosts': FixedLampCosts,
            'FixedScreenCosts': FixedScreenCosts,
            'SpacingCosts': SpacingCosts,
            'greenHouseCosts': greenHouseCosts,
            'variableCosts' : ElectricityCosts + HeatingCosts + CO2Costs + PlantCosts,
            'gas cost' : HeatingCosts,
            'electric cost' : ElectricityCosts,
            'co2 cost' : CO2Costs,
            'plant cost' : PlantCosts,
            'fractionOfYear' : fractionOfYear,
            'AveragePotPerM2' : AveragePotPerM2
            
        }
        
        return return_value
    
    def get_price_per_head(self, freshWeight, dryMatter):
        if dryMatter > 0.08:
            dryMatter_lim = 0.08
        elif dryMatter < 0.07:
            dryMatter_lim = 0.07
        else:
            dryMatter_lim = dryMatter
                
        if freshWeight < 350:
            return 0
        elif freshWeight < 400:
            return (1.5+ 20*(dryMatter_lim-0.07))/50 * freshWeight - (1.5+ 20*(dryMatter_lim-0.07)) * 7
        elif freshWeight < 450:
            return 0.2/50 * freshWeight -0.1 + 20*(dryMatter_lim - 0.07)
        else:
            return (1.7 + 20*(dryMatter_lim-0.07))          

def get_endDate_from_output(result_pandas:DataFrame, convert_str:bool = True):
    filtered_data  = result_pandas[result_pandas['comp1.Growth.FruitFreshweight'] >= 450]
    if len(filtered_data) > 0:
        final_date = filtered_data.index[0]
        if convert_str:
            final_date += timedelta(days=1)
            return final_date.strftime("%d-%m-%Y")
        else:
            final_date += timedelta(days=1)
            final_date.normalize()
            return final_date
    else:
        if convert_str:
            return result_pandas.index[-1].strftime("%d-%m-%Y")
        else:
            return result_pandas.index[-1].normalize()
        
def get_temperature_setting(df_days:DataFrame):
    
    df_index = df_days['common.Tout.Value'].index
    
    values = {}
    key = df_index[0].strftime("%d-%m")
        
    for time_row in df_index:
        value = df_days['common.Tout.Value'].loc[time_row]
        if value < 14:
            value = 14
            
        if value > 25:
            value = 25
        
        values[str(int(time_row.strftime("%H")))] = value
    
    return key, values

def get_reference_table(result_pandas_path:str,
                        plant_density:str,
                        value_table:DataFrame = None,
                        action_table:dict = None,
                        extra_days = 50):
    
    pd_list =  [a[:-1] for a in plant_density.split()[1::2]]

    df = pd.read_csv(result_pandas_path)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.set_index('DateTime', inplace=True)    
    
    heat_setting = df['comp1.Setpoints.SpHeat']
    vent_setting = df['comp1.Setpoints.SpVent']-df['comp1.Setpoints.SpHeat']
    
    ## new_end_date 로 확장하기
    end_date = heat_setting.index[-1]
    end_date_1 = end_date - timedelta(days=1)
    temp_last_setting = heat_setting[(heat_setting.index >= end_date_1) & (heat_setting.index < end_date)]
    vent_last_setting = vent_setting[(vent_setting.index >= end_date_1) & (vent_setting.index < end_date)]
    
    for i in range(1,50):
        for t_index in temp_last_setting.index:
            # print(t_index, temp_last_setting.loc[t_index])
            heat_setting.loc[t_index+timedelta(days=i)] = temp_last_setting.loc[t_index]

    for i in range(1,50):
        for t_index in vent_last_setting.index:
            # print(t_index, temp_last_setting.loc[t_index])
            vent_setting.loc[t_index+timedelta(days=i)] = vent_last_setting.loc[t_index]    

    index = np.arange(1, 451, 0.5)
    ## freshWeight Increment list
    freshWeight = df['comp1.Growth.FruitFreshweight']
    freshWeight = freshWeight[freshWeight.index.hour == 15]
    
    plantdensity = df['comp1.Growth.PlantDensity']
    plantdensity = plantdensity[plantdensity.index.hour == 15]

    if value_table is None:
        value_table_new = pd.DataFrame(np.nan, index=index, columns=pd_list)
    else:
        value_table_new = copy.deepcopy(value_table)

    good_action_date = []
    for i in range(len(freshWeight)-1):
        current_plantDensity = plantdensity.iloc[i]
                
        if freshWeight.iloc[i] >= 1:
            increase = freshWeight.iloc[i+1] / freshWeight.iloc[i]
            current_freshWeight_round = round(freshWeight.iloc[i] * 2) / 2
            
            # print(freshWeight.iloc[i], current_freshWeight_round, increase, current_plantDensity)

            for pd_num in pd_list: 
                if current_plantDensity != int(pd_num):
                    continue 
                value_table_new.at[current_freshWeight_round,pd_num] = increase
                if value_table is not None and increase > value_table.at[current_freshWeight_round,pd_num]:
                    good_action_date.append(freshWeight.index[i])
                
    fill_value_table(value_table_new, pd_list)

    if action_table is None:
        action_table = {pd_list[0]:{}, pd_list[1]:{}}
               
    for idx in freshWeight.index[1:]:
        df_daily = df[(df.index<idx)&(df.index>=idx-timedelta(days=1))]
        FreshWeight = freshWeight.loc[idx-timedelta(days=1)]
        FreshWeight_grow = freshWeight.loc[idx]
        fw_increase = np.nan if ((FreshWeight == 0) or (FreshWeight_grow == 0)) else FreshWeight_grow/FreshWeight
        
        PD = str(int(df_daily['comp1.Growth.PlantDensity'].iloc[-1]))
        fw_index = round(FreshWeight*2)/2   
        if fw_index < 1:
            continue
        target_fw_increase = value_table_new.at[fw_index,PD]     
        score = fw_increase/target_fw_increase*100 if target_fw_increase != 0 else np.nan
                
        if idx not in action_table[PD].keys():
            action_table[PD][idx] = {'heat_setting' : df_daily['comp1.Setpoints.SpHeat'],
                    'fw' : FreshWeight,
                    'fw_increase' : fw_increase,
                    'pd' : PD,
                    'score' : score
                    }              
        else:
            # score recalculation                
            fw_increase_ref = action_table[PD][idx]['fw_increase'] 
            fw_index_ref = round(action_table[PD][idx]['fw']*2)/2
            target_fw_increase_ref = value_table_new.at[fw_index,action_table[PD][idx]['pd']]     
            score_ref =  fw_increase_ref/target_fw_increase_ref*100 if target_fw_increase_ref != 0 else np.nan
            if score > score_ref:
                action_table[PD][idx] = {'heat_setting' : df_daily['comp1.Setpoints.SpHeat'],
                        'fw' : FreshWeight,
                        'fw_increase' : fw_increase,
                        'pd' : PD,
                        'score' : score
                        }   
                
    # df_action =  df[['comp1.Setpoints.SpHeat', 'comp1.Setpoints.SpVent', 'comp1.Growth.PlantDensity']]
    df_action =  df[['comp1.Setpoints.SpHeat', 'comp1.Setpoints.SpVent', 'comp1.Growth.PlantDensity']]
    
    ## df_action correction
    for PD in action_table.keys():
        for timestamp in action_table[PD].keys():
            heat_setting = action_table[PD][timestamp]['heat_setting']            
            for hour_idx in heat_setting.index:
                df_action.at[hour_idx, 'comp1.Setpoints.SpHeat'] = heat_setting.loc[hour_idx]
            
    return value_table_new, action_table, df_action



def fill_value_table(df:DataFrame, column_names:List[str]):
    for column_name in column_names:
        # 마지막 행부터 첫 번째 행까지 반복
        max_value = 0
        for idx in reversed(df.index):
            value = df.at[idx, column_name]
            if np.isnan(value) or value < max_value:
                # NaN이거나 현재의 최대값보다 작은 경우 최대값으로 대체
                df.at[idx, column_name] = max_value
            else:
                # 현재 값이 최대값보다 크거나 같은 경우 최대값 업데이트
                max_value = value

    return df

def action_table_to_server_format(action_table:DataFrame):

    start_date = action_table.index[0].normalize()
    end_date = action_table.index[-1].normalize()

    today = start_date

    heating_setting = {}
    vent_setting = {}

    while today < end_date:
        action_table_one_day = action_table[(action_table.index>=today) & (action_table.index < (today+timedelta(days=1)))]
        key = action_table_one_day.index[0].strftime("%d-%m")
        values_heat = {}
        values_vent = {}
        for idx in action_table_one_day.index:
            value_heat = action_table_one_day.at[idx,'comp1.Setpoints.SpHeat']
            value_vent = action_table_one_day.at[idx,'comp1.Setpoints.SpVent']
            hour = str(int(idx.strftime("%H")))
            values_heat[hour] = value_heat
            values_vent[hour] = value_vent - value_heat
        heating_setting[key] = values_heat
        vent_setting[key] = values_vent
        today = today+timedelta(days=1)

    return heating_setting, vent_setting
    

def get_realtime_data(result_pandas_path:str, start_date:str, end_data:str):
    df = pd.read_csv(result_pandas_path)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.set_index('DateTime', inplace=True)

    startDate = datetime.strptime(start_date, '%d-%m-%Y')
    endDate = datetime.strptime(end_data, '%d-%m-%Y')
    
    heatingTemp = {}      
    
    today =  startDate        
    while today < endDate:
        df_filtered = df[(df.index>=today) & (df.index<today+timedelta(days=1))]
        key, values = get_temperature_setting(df_filtered)
        heatingTemp[key] = values
        today = today + timedelta(days=1)
        
    return heatingTemp
    
    
        
    
    
    

