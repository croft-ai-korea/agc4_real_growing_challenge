import math

def sun_cal(date, forecast, wur_cal=True):
    if (wur_cal == False):
        par_sum = 0
        par_trig = True
        for key, value in enumerate(forecast['fc_iglob']):
            # glass transmission
            par_sum = par_sum + wsm_to_umolm2(value)
            if (par_sum > 50 and par_trig):
                # par_sum이 50 이상이면 해가 떴다고 간주
                date_Rise = date.replace(hour=int(key / 12))
                par_trig = False
            elif (wsm_to_umolm2(value) == 0 and par_trig == False):
                # 해가 뜬 이후 예보 결과가 0이면 해가 졌다고 간주
                date_Set = date.replace(hour=int(key / 12))
                break
    else:
        # dayOfYear = 31 , 2 * math.pi / 365 = 0.01721420632103996
        dayOfYear = (date - date.replace(month=1, day=1)).days
        latitude = 52
        Year_angle = (dayOfYear - 80) * 2 * math.pi / 365
        ellipseCorrection = -7.127 * math.cos(Year_angle) - 1.84 * math.sin(Year_angle) - 0.688 * math.cos(
            2 * Year_angle) + 9.92 * math.sin(2 * Year_angle)
        declination = 0.38 - 0.77 * math.cos(Year_angle) + 23.27 * math.sin(Year_angle) + 0.37 * math.cos(
            2 * Year_angle) - 0.109 * math.sin(2 * Year_angle) - 0.1665 * math.sin(3 * Year_angle)
        Day_length = math.acos(
            -math.tan(declination * 2 * math.pi / 360) * math.tan(latitude * 2 * math.pi / 360)) * 24 / math.pi

        Rise = 12.6 - ellipseCorrection / 60 - 0.5 * Day_length
        Set = 12.6 - ellipseCorrection / 60 + 0.5 * Day_length
        print("Rise",Rise)
        print("Set",Set)
        date_Rise = date.replace(hour=math.floor(Rise), minute=math.floor(Rise % math.floor(Rise) * 60))
        date_Set = date.replace(hour=math.floor(Set), minute=math.floor(Set % math.floor(Set) * 60))
        print("sun_rise = {} and sun_set = {}".format(date_Rise, date_Set))
    return date_Rise, date_Set


def wsm_to_jcm2_day(rad_array):
    return rad_array.sum() * 0.0001 * 60 * 60

def jcm2_to_molm2_day(jcm_var):
    return jcm_var * 0.0215

# 4.6 μmole.m2/s = 1 W/m2
# 2.1μmole.m2/s = 1 W/m2 (305 - 2800nm)
# glass transmission
def wsm_to_umolm2(rad_array):
    return rad_array * 2.4

def wsm_to_molm2_day(rad_array):
    return sum(rad_array) * 2.4 * 60 * 60 * 1e-6

def wsm_to_molm2_day_per5min(rad_array):
    return sum(rad_array) * 2.4 * 60 * 12 * 1e-6

def VPD_cal(green_temp,green_humidity,plant_Temp):
    VPsat = (610.7*10**((7.5*plant_Temp)/(237.3+plant_Temp)))/1000
    VPair = (610.7*10**((7.5*green_temp)/(237.3+green_temp)))/1000 * green_humidity/100
    VPD = VPsat-VPair
