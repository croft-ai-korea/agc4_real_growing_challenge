import sys
from a_util.simulator.devices import Device, CO2dosing, heatingpipes, screens, illumination, setpoints
import json
from a_util.simulator.factory import DeviceFactory
from typing import Dict, List
import pandas as pd
import os
from pandas import DataFrame
from datetime import datetime, timedelta
from random import random, randint, choice
sys.path.append('./')

def get_day_data(df:DataFrame, start_date:str=None, end_date:str=None):
    # 입력된 날짜가 없는 경우, df의 인덱스에서 최소 및 최대 날짜를 자동으로 결정
    if start_date is None:
        start_date = df.index.min().normalize()
    else:
        start_date = pd.to_datetime(start_date).normalize()
    
    if end_date is None:
        end_date = df.index.max().normalize()
    else:
        end_date = pd.to_datetime(end_date).normalize()
    
    # 시작 날짜부터 종료 날짜까지 하루씩 증가시키며 데이터를 추출
    current_date = start_date
    while current_date <= end_date:
        # 다음 날짜 계산
        next_date = current_date + pd.Timedelta(days=1)
        
        # 현재 날짜의 데이터만 선택
        day_data = df[(df.index >= current_date) & (df.index < next_date)]
        
        # 현재 날짜를 다음 날짜로 업데이트
        current_date = next_date
        
        # 선택된 데이터 반환
        yield day_data


class Greenhouse:
    """
    Manages the collection of devices within a greenhouse environment. This class provides
    functionality to add, remove, and manipulate devices such as CO2 dosing systems, heating pipes,
    screens, and illumination devices.

    Attributes:
        devices (dict): A dictionary storing device instances, keyed by device name.
        logging_enabled (bool): If True, actions within the greenhouse will be logged.
    """

    def __init__(self, 
                 logging_enabled: bool = True,
                 startDate: str = "05-09-2023",
                 endDate: str ="31-12-2023"
                 ) -> None:
        """
        Initializes a new Greenhouse instance.

        Parameters:
            logging_enabled (bool, optional): Whether action logging is enabled. Defaults to True.
        """
        self.device_co2: Dict[str, CO2dosing] = {}
        self.device_heatingpipes: Dict[str, heatingpipes] = {}
        self.device_screens: Dict[str, screens] = {}
        self.device_illumination: Dict[str, illumination] = {}
        self.device_setpoints: Dict[str, setpoints] = {}

        self.logging_enabled = logging_enabled  # Controls whether logging is enabled
        self.endDate = endDate
        self.startDate = startDate
        
        os.makedirs("data", exist_ok=True)
        
        # with open(server_response_file, 'r') as file:
        #     self.output_data = json.load(file)


    def initialize_devices_with_randomWalk(self, control_json_path:str = None):
        with open(control_json_path, 'r') as file:
            control_data = json.load(file)
        
        ## Date
        random_days = 34
        self.startDate_datetime = (datetime(2023,9,5)+timedelta(days=randint(0,random_days)))
        self.startDate = self.startDate_datetime.strftime("%d-%m-%Y")
        self.endDate_datetime = datetime(2023,12,31)
        self.endDate = self.endDate_datetime.strftime("%d-%m-%Y")
        total_days = (self.endDate_datetime-self.startDate_datetime).days
        
        # pland_density
        base_density = 14      
        random_diff_density = [21, 21, 21]
        plant_density = [base_density+randint(0,random_diff_density[0])]
        for diff in random_diff_density[1:]:
            plant_density.append(plant_density[-1]+randint(0,diff))
        self.plantDensity = f"1 56; {plant_density[0]} 42; {plant_density[1]} 30; {plant_density[2]} 20"
        
        # self.plantDensity = "1 20"
        
        ## heating Temp
        heatingTemp = {}
        baseline = 15
        heating_diff = {"0":2,"2":2,"4":3,"6":3,"8":4,"10":7,
                        "12":7,"14":7,"16":4,"18":2,"20":2,"22":2}
        for i in range(total_days):
            today = self.startDate_datetime + timedelta(days=i)
            today_str = today.strftime("%d-%m")  
            today_temp = {}   
            before_temp = 15   
            for key, val in heating_diff.items():
                today_temp[key] = round((before_temp + (baseline+random()*val))/2*100)/100
                before_temp = today_temp[key]
            heatingTemp[today_str] = today_temp
                
        ## radiation Influence
        radiation_influence_list = [2,3,4]
        radiationInfluence = '100 400 '+str(choice(radiation_influence_list)) 
        
        ## ventOffset
        ventOffset = {}
        baseline = 2
        ventOffset_diff = {"0":0,"2":0,"4":0,"6":2,"8":2,"10":4,
                      "12":4,"14":4,"16":2,"18":2,"20":0,"22":0}
        for i in range(total_days):
            today = self.startDate_datetime + timedelta(days=i)
            today_str = today.strftime("%d-%m")  
            today_vent = {}  
            for key, val in ventOffset_diff.items():
                today_vent[key] = round( (baseline+random()*val)*100  )/100
            ventOffset[today_str] = today_vent
            
        ## PbandVent
        baseline = [6, 18, 20, 4]
        PbandVant_diff = [4, 2]
        baseline[1] += randint(-PbandVant_diff[0],PbandVant_diff[0])
        baseline[3] += randint(-PbandVant_diff[1],PbandVant_diff[1])
        PbandVent = f"{baseline[0]} {baseline[1]};{baseline[2]} {baseline[3]}"

        ## illumination led type
        led_type = choice(['lmp_LED23','lmp_LED27', 'lmp_LED29', 'lmp_LED30', 'lmp_LED32'])
        
        ## intensity
        # intensity = 100 + randint(0,150)
        intensity = 0 + randint(0,100)
        
        ## hours_light
        hours_light = {}
        baseline = 12
        hours_diff = 4
        # baseline = 0
        # hours_diff = 0        
        for i in range(total_days):
            today = self.startDate_datetime + timedelta(days=i)
            today_str = today.strftime("%d-%m")
            hours_light[today_str] = round((baseline+random()*hours_diff)*100)/100

        ## end_time
        end_time = 18 - randint(0, 2)
        
        ## max_iglob
        # max_iglob = 100 + randint(0,150)
        max_iglob = 0 + randint(0,100)
        
        ## close_above
        close_above =  f"{350+randint(0,1000)} {50+randint(0,50)}"

        ## co2_settings
        co2_rand1 = 400+randint(0,400)
        co2_rand2 = 800+randint(0,200)
        co2_setpoint = {
            "01-01" : {"r-3":400, "r-2":co2_rand1, "r":co2_rand2, "s":co2_rand2, "s+2":co2_rand1, "s+3": 400}
            }
        
        temp_settings = {
            'heatingTemp': heatingTemp,
            'radiationInfluence': radiationInfluence,
            'ventOffset': ventOffset,
            'PbandVent': PbandVent,
        }
        co2_settings = {
            'setpoint': co2_setpoint,
            'setpIfLamps': control_data['comp1']['setpoints']['CO2']['@setpIfLamps'],
            'doseCapacity': control_data['comp1']['setpoints']['CO2']['@doseCapacity']
        }
        ventilation_settings = {
            'winLeeMin': control_data['comp1']['setpoints']['ventilation']['@winLeeMin'],
            'winLeeMax': control_data['comp1']['setpoints']['ventilation']['@winLeeMax'],
            'winWndMin': control_data['comp1']['setpoints']['ventilation']['@winWndMin'],
            'winWndMax': control_data['comp1']['setpoints']['ventilation']['@winWndMax'],
            'startWnd': control_data['comp1']['setpoints']['ventilation']['@startWnd']
        }

        # Create and add Setpoints
        setpoints = DeviceFactory.create_device('setpoints', 'setpoints', temp=temp_settings,
                                                CO2=co2_settings, ventilation=ventilation_settings)
        self.add_device(setpoints)  

        # Create and add devices
        devices = [
            ('CO2dosing', 'co2', 
                {'capacity': control_data['common']['CO2dosing']['@pureCO2cap']}),
            ('heatingpipes', 'pipe1', 
                {'max_temp': control_data['comp1']['heatingpipes']['pipe1']['@maxTemp'], 
                'min_temp': control_data['comp1']['heatingpipes']['pipe1']['@minTemp'], 
                'radiation_influence': control_data['comp1']['heatingpipes']['pipe1']['@radiationInfluence']}),
            ('screens', 'scr1',
                {'enabled': control_data['comp1']['screens']['scr1']['@enabled'],
                'material': control_data['comp1']['screens']['scr1']['@material'],
                'close_below': control_data['comp1']['screens']['scr1']['@closeBelow'],
                'close_above': close_above,
                'tout_max': control_data['comp1']['screens']['scr1']['@ToutMax'],
                'light_pollution_prevention': control_data['comp1']['screens']['scr1']['@lightPollutionPrevention']}),
            ('screens', 'scr2',
                {'enabled': control_data['comp1']['screens']['scr2']['@enabled'],
                'material': control_data['comp1']['screens']['scr2']['@material'],
                'close_below': control_data['comp1']['screens']['scr2']['@closeBelow'],
                'close_above': control_data['comp1']['screens']['scr2']['@closeAbove'],
                'tout_max': control_data['comp1']['screens']['scr2']['@ToutMax'],
                'light_pollution_prevention': control_data['comp1']['screens']['scr2']['@lightPollutionPrevention']}),
            ('illumination', 'lmp1',
                {'type': led_type,
                'intensity': intensity, 
                'hours_light': hours_light, 
                'end_time': end_time,
                'max_iglob': max_iglob, 
                'max_par_sum': control_data['comp1']['illumination']['lmp1']['@maxPARsum']})
        ]

        self.pureCO2cap = control_data['common']['CO2dosing']['@pureCO2cap']

        for device_type, name, kwargs in devices:
            device = DeviceFactory.create_device(device_type, name, **kwargs)
            self.add_device(device)

    def calculate_DLI(self, day_df:DataFrame):
        return (day_df['comp1.PARsensor.Above']*60*60).sum()/1e6

    def calculate_Joules_Iglob(self, day_df:DataFrame):
        return (day_df['common.Iglob.Value']*60*60).sum()/1e4
    
    def calculate_Joules_above(self, day_df:DataFrame):
        return (day_df['comp1.PARsensor.Above']/2.15*60*60).sum()/1e4
    
    def find_sunrise_sunset(self, day_df:DataFrame):
        # 'common.Iglob.Value' 열의 값이 0 이상인 데이터 포인트들의 인덱스를 찾음
        positive_values = day_df['common.Iglob.Value'] > 0
        
        # 첫 번째와 마지막 True 인덱스를 찾아 일출과 일몰 시간 결정
        try:
            sunrise_index = positive_values.idxmax()  # 첫 번째 True 값의 인덱스
            sunset_index = day_df[positive_values].index[-1]  # 마지막 True 값의 인덱스
        except IndexError:
            sunrise_index = None
            sunset_index = None
        
        return sunrise_index, sunset_index

    def load_weather_data_and_analysis(self, parameters:DataFrame, save_csv_path:str = None):
        self.weather_data = parameters

        self.parameter_analysis = pd.DataFrame(
            columns=['dli', 'joule_iglob', 'joule_above','sunrise','sunset']
            )
        self.parameter_analysis.index = pd.to_datetime(self.parameter_analysis.index)  # 인덱스를 datetime으로 설정

        for day_df in get_day_data(self.weather_data):

            current_date = day_df.index[0].date()
            dli = self.calculate_DLI(day_df)
            joule_iglob = self.calculate_Joules_Iglob(day_df)
            joule_above = self.calculate_Joules_above(day_df)
            sunrise, sunset = self.find_sunrise_sunset(day_df)

            self.parameter_analysis.loc[current_date] = [dli,
                                                     joule_iglob,
                                                     joule_above,
                                                     sunrise,
                                                     sunset]
            
        if save_csv_path is not None:
            self.parameter_analysis.to_csv(save_csv_path, index=False) 

    def get_co2dosing(self, name='co2') -> CO2dosing:
        device = self.devices.get(name)
        if not isinstance(device, CO2dosing):
            raise TypeError(f"Device with name {name} is not a CO2dosing system.")
        return device

    def get_heatingpipes(self, name='pipe1') -> heatingpipes:
        device = self.devices.get(name)
        if not isinstance(device, heatingpipes):
            raise TypeError(f"Device with name {name} is not a HeatingPipes system.")
        return device

    def get_screens(self, name) -> screens:
        device = self.devices.get(name)
        if not isinstance(device, screens):
            raise TypeError(f"Device with name {name} is not a Screens system.")
        return device

    def get_illumination(self, name='lmp1') -> illumination:
        device = self.devices.get(name)
        if not isinstance(device, illumination):
            raise TypeError(f"Device with name {name} is not an Illumination system.")
        return device

    def get_setpoints(self, name) -> setpoints:
        device = self.devices.get(name)
        if not isinstance(device, setpoints):
            raise TypeError(f"Device with name {name} is not a Setpoints system.")
        return device

    def initialize_devices(self, control_json_path:str = None):
        """
        Initializes and adds devices to the greenhouse, including setpoints for temperature, CO2, and ventilation.
        This method should be explicitly called when device setup is required.
        """
                        
        if control_json_path is None : 
            # Define Setpoints for temperature, CO2, and ventilation
            temp_settings = {
                'heatingTemp': {
                "05-09": { "0": "15", "r-2": "15", "r-1": "15", "r" : "15",
                        "r+1" : 17.97, "r+2" : 17.97, "12" : 17.97,
                        "14" : 17.97,  "s-2": 17.97, "s-1": 17.97,
                        "s" : "15", "s+1" : "15", "s+2" : "15", "23": "15"},
                "15-10": { "0": "15", "r-2": "15", "r-1": "15", "r" : "15",
                        "r+1" : 16.06, "r+2" : 16.06, "12" : 16.06,
                        "14" : 16.06, "s-2": 16.06, "s-1": 16.06,
                        "s" : "15", "s+1" : "15", "s+2" : "15",  "23": "15"},
                },
                'radiationInfluence': "100 400 2",
                'ventOffset': {
                    "01-04": {"00:00": 2.398}
                },
                'PbandVent': "6 18;20 4"
            }
            
            co2_settings = {
                'setpoint': {
                    "01-01": {"r+0.5": 400, "r+1": 800, "s-1.5": 800, "s": 400}
                },
                'setpIfLamps': {
                    "15-09": "500",
                    "25-09": "700"
                },
                'doseCapacity': {
                    "01-09": "100",
                    "01-10": "20 100; 40 50; 70 25"
                }
            }
            ventilation_settings = {
                'winLeeMin': {"01-01": {"00:00": 0}},
                'winLeeMax': {"01-01": {"00:00": 100}},
                'winWndMin': {"01-01": {"00:00": 0}},
                'winWndMax': {"01-01": {"00:00": 100}},
                'startWnd': {"01-01": {"00:00": 50}}
            }

            # Create and add Setpoints
            setpoints = DeviceFactory.create_device('setpoints', 'setpoints', temp=temp_settings,
                                                    CO2=co2_settings, ventilation=ventilation_settings)
            self.add_device(setpoints)

            # Create and add devices
            max_temp_periods = {
                "15-09": {"r-1": 60, "r+1": 70, "r+2": 70, "r+3": 60},
                "15-10": {"0": 80}
            }
            min_temp_periods = {
                "15-09": {"0": 0},
                "15-10": {"r-1": 40, "r+1": 50, "s-2": 50, "s": 40}
            }

            hours_light_periods = {
                "05-09": 0,
                "07-09": 19.208242
            }
            tout_max_periods = {
                "01-09": 25,
                "19-09": 18
            }
            devices = [
                ('CO2dosing', 'co2', {'capacity': 130.0}),
                ('heatingpipes', 'pipe1',
                {'max_temp': max_temp_periods, 'min_temp': min_temp_periods, 'radiation_influence': "100 300"}),
                ('screens', 'scr1',
                {'enabled': True,'material': "scr_Transparent", 'close_below': "5 255; 10 50; 15.0 5; 15.2 0", 'close_above': "450 75",
                'tout_max': 9, 'light_pollution_prevention': False}),
                ('screens', 'scr2',
                {'enabled': True,'material': "scr_Blackout", 'close_below': "5 10", 'close_above': "1200 80", 'tout_max': tout_max_periods,
                'gapOnTempExc': "1 0;4 20", 'light_pollution_prevention': True}),
                ('illumination', 'lmp1',
                {'type': 'lmp_LED27', 'intensity': 142.942512, 'hours_light': hours_light_periods, 'end_time': 20,
                'max_iglob': 163.381332, 'max_par_sum': 40})
            ]

            self.pureCO2cap = 100
            self.plantDensity = "1 56; 40 42; 50 30; 60 20"

        else:
            with open(control_json_path, 'r') as file:
                control_data = json.load(file)

            temp_settings = {
                'heatingTemp': control_data['comp1']['setpoints']['temp']['@heatingTemp'],
                'radiationInfluence': control_data['comp1']['setpoints']['temp']['@radiationInfluence'],
                'ventOffset': control_data['comp1']['setpoints']['temp']['@ventOffset'],
                'PbandVent': control_data['comp1']['setpoints']['temp']['@PbandVent']
            }
            co2_settings = {
                'setpoint': control_data['comp1']['setpoints']['CO2']['@setpoint'],
                'setpIfLamps': control_data['comp1']['setpoints']['CO2']['@setpIfLamps'],
                'doseCapacity': control_data['comp1']['setpoints']['CO2']['@doseCapacity']
            }
            ventilation_settings = {
                'winLeeMin': control_data['comp1']['setpoints']['ventilation']['@winLeeMin'],
                'winLeeMax': control_data['comp1']['setpoints']['ventilation']['@winLeeMax'],
                'winWndMin': control_data['comp1']['setpoints']['ventilation']['@winWndMin'],
                'winWndMax': control_data['comp1']['setpoints']['ventilation']['@winWndMax'],
                'startWnd': control_data['comp1']['setpoints']['ventilation']['@startWnd']
            }

            # Create and add Setpoints
            setpoints = DeviceFactory.create_device('setpoints', 'setpoints', temp=temp_settings,
                                                    CO2=co2_settings, ventilation=ventilation_settings)
            self.add_device(setpoints)  

            # Create and add devices
            devices = [
                ('CO2dosing', 'co2', 
                 {'capacity': control_data['common']['CO2dosing']['@pureCO2cap']}),
                ('heatingpipes', 'pipe1', 
                 {'max_temp': control_data['comp1']['heatingpipes']['pipe1']['@maxTemp'], 
                  'min_temp': control_data['comp1']['heatingpipes']['pipe1']['@minTemp'], 
                  'radiation_influence': control_data['comp1']['heatingpipes']['pipe1']['@radiationInfluence']}),
                ('screens', 'scr1',
                 {'enabled': control_data['comp1']['screens']['scr1']['@enabled'],
                  'material': control_data['comp1']['screens']['scr1']['@material'],
                  'close_below': control_data['comp1']['screens']['scr1']['@closeBelow'],
                  'close_above': control_data['comp1']['screens']['scr1']['@closeAbove'],
                  'tout_max': control_data['comp1']['screens']['scr1']['@ToutMax'],
                  'light_pollution_prevention': control_data['comp1']['screens']['scr1']['@lightPollutionPrevention']}),
                ('screens', 'scr2',
                 {'enabled': control_data['comp1']['screens']['scr2']['@enabled'],
                  'material': control_data['comp1']['screens']['scr2']['@material'],
                  'close_below': control_data['comp1']['screens']['scr2']['@closeBelow'],
                  'close_above': control_data['comp1']['screens']['scr2']['@closeAbove'],
                  'tout_max': control_data['comp1']['screens']['scr2']['@ToutMax'],
                  'light_pollution_prevention': control_data['comp1']['screens']['scr2']['@lightPollutionPrevention']}),
                ('illumination', 'lmp1',
                 {'type': control_data['comp1']['illumination']['lmp1']['@type'],
                  'intensity': control_data['comp1']['illumination']['lmp1']['@intensity'], 
                  'hours_light': control_data['comp1']['illumination']['lmp1']['@hoursLight'], 
                  'end_time': control_data['comp1']['illumination']['lmp1']['@endTime'],
                  'max_iglob': control_data['comp1']['illumination']['lmp1']['@maxIglob'], 
                  'max_par_sum': control_data['comp1']['illumination']['lmp1']['@maxPARsum']})
            ]

            self.plantDensity = control_data['crp_dwarftomato']['cropModel']['@plantDensity']
            self.pureCO2cap = control_data['common']['CO2dosing']['@pureCO2cap']
            self.startDate = control_data['simset'].get('@startDate', "05-09-2023")
            self.endDate = control_data['simset']['@endDate']
            self.meteodata = "Bleiswijk"

        for device_type, name, kwargs in devices:
            device = DeviceFactory.create_device(device_type, name, **kwargs)
            self.add_device(device)

    def log(self, message):
        """
        Logs a message to the console, provided that logging is enabled.

        Parameters:
            message (str): The message to log.
        """
        if self.logging_enabled:
            print(message)

    def add_device(self, device):
        """
        Adds a device to the greenhouse.

        Parameters:
            device (Device): The device instance to add.

        Logs the action if logging is enabled.
        """
        if isinstance(device, CO2dosing):
            self.device_co2[device.name] = device
        elif isinstance(device, heatingpipes):
            self.device_heatingpipes[device.name] = device
        elif isinstance(device, screens):
            self.device_screens[device.name] = device
        elif isinstance(device, illumination):
            self.device_illumination[device.name] = device
        elif isinstance(device, setpoints):
            self.device_setpoints[device.name] = device
        else:
            raise ValueError("Unknown device type")
        if self.logging_enabled:
            print(f"Device '{device.name}' added.")

    def remove_device(self, name):
        """
        Removes a device from the greenhouse by name.

        Parameters:
            name (str): The name of the device to remove.

        Logs the action if logging is enabled.
        """
        if name in self.devices:
            del self.devices[name]
            self.log(f"Device '{name}' removed.")
        else:
            self.log(f"Device '{name}' not found for removal.")

    def get_device(self, name, device_type):
        """
        Retrieves a device from the greenhouse by name.

        Parameters:
            name (str): The name of the device to retrieve.

        Returns:
            Device: The device instance if found, None otherwise.
        """
        if device_type == 'co2dosing':
            return self.device_co2.get(name)
        elif device_type == 'heatingpipes':
            return self.device_heatingpipes.get(name)
        elif device_type == 'screens':
            return self.device_screens.get(name)
        elif device_type == 'illumination':
            return self.device_illumination.get(name)
        elif device_type == 'setpoints':
            return self.device_setpoints.get(name)
        else:
            raise ValueError("Unknown device type")

    def device_count(self):
        """
        Counts the number of devices in the greenhouse.

        Returns:
            int: The number of devices.
        """
        return len(self.devices)

    def list_device_names(self):
        """
        Lists the names of all devices in the greenhouse.

        Returns:
            list[str]: A list of device names.
        """
        device_names = []
        device_names.extend(self.device_co2.keys())
        device_names.extend(self.device_heatingpipes.keys())
        device_names.extend(self.device_screens.keys())
        device_names.extend(self.device_illumination.keys())
        device_names.extend(self.device_setpoints.keys())
        return device_names

    def display_device_settings(self, name):
        """
        Displays the settings of a device.

        Parameters:
            name (str): The name of the device whose settings to display.

        Returns:
            str: The settings of the device if found, or a not found message.
        """
        device = self.get_device(name)
        if device:
            return device.get_settings()
        else:
            return "Device not found."

    def display_all_device_settings(self):
        """
        Displays the settings of all devices in the greenhouse.
        """
        all_devices = [
            self.device_co2, self.device_heatingpipes, self.device_screens,
            self.device_illumination, self.device_setpoints
        ]
        print("Setting of devices in the greenhouse:")
        for device_dict in all_devices:
            for device_name, device in device_dict.items():
                print(f"Name: {device_name}, Settings: {device.get_settings()}")
        print(f"Additional Settings: EndDate: {self.endDate}, CO2 Capacity: {self.pureCO2cap}, Plant Density: {self.plantDensity}")
        print("Parameter explanation End")

    def export_all_devices(self, control_save_path:str = None, set_start_date = False):
        """Exports the configuration of all devices into a structured JSON string."""
        all_devices = {
            'heatingpipes': {name: dev.export() for name, dev in self.device_heatingpipes.items()},
            'screens': {name: dev.export() for name, dev in self.device_screens.items()},
            'illumination': {name: dev.export() for name, dev in self.device_illumination.items()},
        }
        # 'setpoints': {name: dev.export() for name, dev in self.device_setpoints.items()}

        all_devices.update({name: dev.export() for name, dev in self.device_setpoints.items()})
        if set_start_date:
            config = {
                "simset": {"@endDate": self.endDate, "@startDate" : self.startDate, "@meteodata" : self.meteodata},            
                "common": {"CO2dosing": {"@pureCO2cap": self.pureCO2cap}},
                "comp1": all_devices,
                "crp_dwarftomato": {"cropModel": {"@plantDensity": self.plantDensity}}
            }
        else:
            config = {
                "simset": {"@endDate": self.endDate, "@meteodata" : self.meteodata},            
                "common": {"CO2dosing": {"@pureCO2cap": self.pureCO2cap}},
                "comp1": all_devices,
                "crp_dwarftomato": {"cropModel": {"@plantDensity": self.plantDensity}}
            }
        json_result = json.dumps(config, indent=4)
        
        if control_save_path is not None:
            with open(control_save_path, 'w') as file:
                json.dump(config, file, indent=4)
        

        # data_dict = json.loads(json_result)
        # Flatten the JSON
        # from pandas import json_normalize
        # flat_data = json_normalize(data_dict, sep='\n')
        # flat_data.to_csv(csv_save_path, index=False)

        return json_result

    def explain_all_devices(self):
        # Assuming you have access to a list or other collection of device classes
        device_classes = [Device, CO2dosing, heatingpipes, screens, illumination, setpoints]

        print("Greenhouse Devices Overview:\n")
        for device_class in device_classes:
            # Directly calling the static describe method on the class
            print(device_class.describe() + "\n")

    def explain_greenhouse_functions(self):
        """
        Gathers and displays explanations for each function available in the Greenhouse class.

        Parameters:
            greenhouse (Greenhouse): An instance of the Greenhouse class.
        """
        function_names = [method for method in dir(self) if
                          callable(getattr(self, method)) and method.startswith('_describe_')]
        for name in function_names:
            description_method = getattr(self, name)
            info = description_method()
            print(f"Function: {name[len('_describe_'):]}")
            print(f"Description: {info['description']}")
            print(f"Parameters: {info['parameters']}")
            print(f"Returns: {info['returns']}\n")

    def _describe_log(self):
        return {
            'description': 'Logs a message to the console, if logging is enabled for the greenhouse.',
            'parameters': 'message (str): The message to log.',
            'returns': 'None'
        }

    def _describe_add_device(self):
        return {
            'description': 'Adds a device to the greenhouse system and logs the action.',
            'parameters': 'device (Device): The device instance to add to the greenhouse.',
            'returns': 'None'
        }
    
    def _describe_remove_device(self):
        return {
            'description': 'Removes a device from the greenhouse by its name and logs the action.',
            'parameters': 'name (str): The name of the device to remove.',
            'returns': 'None'
        }

    def _describe_get_device(self):
        return {
            'description': 'Retrieves a device instance from the greenhouse by its name.',
            'parameters': 'name (str): The name of the device to retrieve.',
            'returns': 'Device instance if found, None otherwise.'
        }

    def _describe_device_count(self):
        return {
            'description': 'Counts the total number of devices currently in the greenhouse.',
            'parameters': 'None',
            'returns': 'int: The total number of devices.'
        }

    def _describe_list_device_names(self):
        return {
            'description': 'Lists the names of all devices currently in the greenhouse.',
            'parameters': 'None',
            'returns': 'list[str]: A list containing the names of all devices.'
        }

    def _describe_display_device_settings(self):
        return {
            'description': 'Displays the settings of a specific device by its name.',
            'parameters': 'name (str): The name of the device whose settings are to be displayed.',
            'returns': 'str: The settings of the specified device, or a not found message.'
        }

    def _describe_display_all_device_settings(self):
        return {
            'description': 'Displays the settings of all devices within the greenhouse.',
            'parameters': 'None',
            'returns': 'None'
        }

    def _describe_update_device_parameter(self):
        return {
            'description': 'Updates a specific parameter of a device by its name and logs the action.',
            'parameters': 'name (str): The name of the device to update, parameter_name (str): The name of the parameter to update, value: The new value for the parameter.',
            'returns': 'None'
        }