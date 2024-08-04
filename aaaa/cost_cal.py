# import sys

# sys.path.append('./')
# from a_util.env.real_env import GreenHouseInput

class greenhouse_const:
    # const variables
    greenhouse_area  = 96  # 96 m2
    price_lettuce  = 0.5  # 0.4 or 0.5 euro multiplied by the average number of heads per m²
    lamp_watt  = 630 # W
    # = 7 # hour
    # fixed costs
    plant_fee = 0.12  # € 0.12 per piece
    occupation_fee = 17  # 11.50 euro per m² per year + 5.5 euro per m² per year
    co2_fee = 0.015  # € 0.015 per m² per year per kg/(ha hr) of capacity
    lamp_fee = 0.07  # € 0.07 per μmol/(m² s) per year
    lamp_umol = 270 # μmol/(m² s)
    screen_fee = 1.25  # € 1.25 per screen per yea
    screen_num = 2  # LUXOUS 1347 energy screen and OBSCURA 9950 light blocking screen and side scrren : no care in challenge
    spacing_fee = 1.5  # Each additional step brings € 1.50 additional costs per m² per year
    # variable costs
    lamp_var_peak = 0.125  # € 0.125 per kWh 07:00~23:00  led(max) 630W
    lamp_var_offpeak = 0.075  # € 0.075 per kWh 23:00~07:00  led(max) 630W
    pipe_var_fee = 0.0375  # € 0.0375 per kWh
    co2_var_fee = 0.132  # 0.132 per kg
    co2_var_fee_sim = 0.132  # 0.135 per kg
    co2_var_supply = 0.000125 * 60 # kg per hour
    dosing_capacity = 125
    # init_dummy
    dummy_day = 21
    dummy_density = [15, 15, 90, 90, 77, 60, 60, 51, 51, 35, 35, 35, 27, 27, 27, 27, 24, 24, 24, 24, 24]


class cost_calculate:
    def __init__(self,_in,current_density):
        self._in = _in
        self.density = greenhouse_const.dummy_density # 추후 더미 수정 필요
        self.density_len = 10
        self.averageheadm2 = self.head_cal()   
        self.gain = greenhouse_const.price_lettuce * self.averageheadm2
        self.plant_costs = greenhouse_const.plant_fee * self.averageheadm2
        self.fractionofyear = _in.nthday/365
        self.greenhouse_occupation = greenhouse_const.occupation_fee * self.fractionofyear
        self.screen_costs = greenhouse_const.screen_num * greenhouse_const.screen_fee * self.fractionofyear
        self.spacing_costs = greenhouse_const.spacing_fee * self.density_len * self.fractionofyear

    def head_cal(self):
        #density_array = convertDensityString2Array(density)
        if(self._in.nthday > self.density_len):#len(self.density)):  ### 추후 수정
            self.density = self.density + [self.density[-1]]*(self._in.nthday-self.density_len)
        return self._in.nthday/sum([1/self.density for self.density in self.density])
    
    def pipe_calculate(self):
        ptotal = (sum(self._in.indoor_env['t_rail'])-sum(self._in.indoor_env['tair']))*2 / 1000
        self.var_pipe_costs = greenhouse_const.pipe_var_fee * ptotal
        return self.var_pipe_costs

    def pipe_calculate_sim(self):
        ptotal = sum(self._in.indoor_env['t_rail']) / 1000
        self.var_pipe_costs = greenhouse_const.pipe_var_fee * ptotal
        return self.var_pipe_costs

    def lamp_calculate(self,intensity,hourslight,endtime):
        percentoflamp = intensity / greenhouse_const.lamp_umol
        self.fixed_lamp_costs = greenhouse_const.lamp_fee * greenhouse_const.lamp_umol * percentoflamp * self.fractionofyear
        self.var_lamp_costs = (greenhouse_const.lamp_watt * percentoflamp / 1000) * (greenhouse_const.lamp_var_peak * (endtime - greenhouse_const.lamp_peak_begintime) + greenhouse_const.lamp_var_offpeak * (hourslight - endtime - greenhouse_const.lamp_peak_begintime))
        return self.fixed_lamp_costs, self.var_lamp_costs

    def co2_calculate(self,co2_time_hour):
        self.fixed_co2_costs = greenhouse_const.co2_fee * greenhouse_const.dosing_capacity * self.fractionofyear
        self.var_co2_costs = greenhouse_const.co2_var_fee * greenhouse_const.co2_var_supply * co2_time_hour * greenhouse_const.dosing_capacity
        return self.fixed_co2_costs, self.var_co2_costs

    def co2_calculate_sim(self, dosing_capacity,comp1_McPureAir_Value):
        self.fixed_co2_costs = greenhouse_const.co2_fee * dosing_capacity * self.fractionofyear
        kgCO2 = sum(comp1_McPureAir_Value) * 3600
        self.var_co2_costs = greenhouse_const.co2_var_fee_sim * kgCO2
        return self.fixed_co2_costs, self.var_co2_costs
    """ 
    1~3일 합산
    - 1일 값 = 할계산
    """

    def result_calculate(self,intensity,hourslight,endtime):
        self.pipe_calculate()
        self.lamp_calculate(intensity, hourslight, endtime)
        self.co2_calculate()
        self.fixed_costs = self.greenhouse_occupation + self.fixed_co2_costs + self.fixed_lamp_costs + self.screen_costs + self.spacing_costs + self.plant_costs
        self.variable_costs = self.var_lamp_costs + self.var_pipe_costs + self.var_co2_costs
        self.net_profit = self.gain - self.fixed_costs - self.variable_costs
        return self.net_profit