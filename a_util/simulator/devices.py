from typing import Dict, Type

class Device:
    """
    The base class for all devices in the greenhouse system. It defines common attributes
    and methods that all devices share.

    Attributes:
        name (str): The unique name of the device.
        enabled (bool): A flag indicating whether the device is enabled or disabled.
    """
    def __init__(self, name: str) -> None:
        """
        Initializes a new Device instance.

        Parameters:
            name (str): The name of the device.
            enabled (bool, optional): The initial enabled state of the device. Defaults to True.
        """
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"

    @staticmethod
    def describe():
        """
        Describes the base device features and attributes.
        """
        description = "Base device in the greenhouse system. Common attributes: name, enabled."
        return description

    def get_settings(self):
        """
        Retrieves the device's current settings as a formatted string. This base method
        provides a default implementation, which can be overridden by subclasses to include
        additional settings.

        Returns:
            str: A string representation of the device's settings.
        """
        return f"Name: {self.name}"

class CO2dosing(Device):
    """
    Represents a CO2 dosing system in the greenhouse. It inherits from the Device class and
    adds a specific attribute for CO2 capacity.

    Attributes:
        capacity (float): The capacity of the CO2 dosing system.
    """
    def __init__(self, name: str, capacity: float) -> None:
        """
        Initializes a new CO2DosingSystem instance.

        Parameters:
            name (str): The name of the CO2 dosing system.
            capacity (float): The capacity of the CO2 dosing system.
        """
        super().__init__(name)
        self.capacity = capacity

    def __repr__(self):
        return f"{super().__repr__()}, capacity={self.capacity}"

    def get_settings(self):
        """
        Retrieves the CO2 dosing system's current settings, including its capacity.

        Returns:
            str: A string representation of the CO2 dosing system's settings.
        """
        return f"{super().get_settings()}, Capacity: {self.capacity}"

    @staticmethod
    def describe():
        """
        Describes the CO2 Dosing System's features and attributes.
        """
        description = "CO2 Dosing System: Manages CO2 levels. Attributes: capacity."
        return description

class heatingpipes(Device):
    """
    Represents a heating pipe in the greenhouse. It controls the temperature within the greenhouse
    and its influence by radiation.

    Attributes:
        max_temp (float): The maximum temperature the heating pipe can reach.
        min_temp (float): The minimum temperature for the heating pipe.
        radiation_influence (list[int]): The influence of radiation on the heating process, represented as a range.
    """
    def __init__(self, name, max_temp, min_temp, radiation_influence, enabled=True):
        """
        Initializes a new HeatingPipe instance.

        Parameters:
            name (str): The name of the heating pipe.
            max_temp (float): The maximum temperature of the heating pipe.
            min_temp (float): The minimum temperature of the heating pipe.
            radiation_influence (str): A string representing the range of radiation influence.
                                       This will be converted into a list of integers.
        """
        super().__init__(name)
        self.max_temp = max_temp  # Nested dictionary for max temperature settings
        self.min_temp = min_temp  # Nested dictionary for min temperature settings
        self.radiation_influence = radiation_influence

    def __repr__(self):
        return f"{super().__repr__()}, max_temp={self.max_temp}, min_temp={self.min_temp}, radiation_influence = {self.radiation_influence}"

    def get_settings(self):
        """
        Retrieves the heating pipe's current settings, including temperature limits and radiation influence.

        Returns:
            str: A string representation of the heating pipe's settings.
        """
        return (f"{super().get_settings()}, Max Temp Periods: {self.max_temp}, "
                f"Min Temp Periods: {self.min_temp}, Radiation Influence: {self.radiation_influence}")
    def export(self):
        """
        Exports the heating pipe settings to a dictionary format for easy serialization or processing.

        Returns:
            dict: A dictionary representing the heating pipe's settings.
        """
        return {
                "@maxTemp": self.max_temp,
                "@minTemp": self.min_temp,
                "@radiationInfluence": self.radiation_influence
        }


    @staticmethod
    def describe():
        """
        Describes the Heating Pipe's features and attributes.
        """
        description = ("heatingpipes: Controls the greenhouse's temperature. "
                       "Attributes include max_temp (the maximum temperature it can reach), "
                       "min_temp (the minimum temperature), and radiation_influence "
                       "(how radiation affects heating efficiency).")
        return description

class screens(Device):
    """
    Represents a screen device in the greenhouse, which can be used to control the amount of light,
    temperature, and even help in preventing light pollution.

    Inherits from the Device class.

    Attributes:
        material (str): The material of the screen which affects its properties.
        close_below (float): The light intensity threshold below which the screen closes.
        close_above (float): The light intensity threshold above which the screen closes.
        tout_max (float): The maximum outside temperature for the screen to be active.
        light_pollution_prevention (bool): Indicates whether the screen is used to prevent light pollution.
    """

    def __init__(self, name, enabled,material, close_below, close_above, tout_max, light_pollution_prevention, gapOnTempExc=""):
        """
        Initializes a new Screen instance with specified properties.

        Parameters:
            name (str): The name of the screen device.
            material (str): The material type of the screen.
            close_below (float): Light intensity below which the screen should close.
            close_above (float): Light intensity above which the screen should close.
            tout_max (float): Maximum outside temperature for the screen's operation.
            light_pollution_prevention (bool): Flag indicating if the screen is for preventing light pollution.
        """
        super().__init__(name)
        self.enabled = enabled
        self.material = material
        self.close_below = close_below
        self.close_above = close_above
        self.tout_max = tout_max  # Dictionary for temperature max periods
        self.gapOnTempExc = gapOnTempExc  # String or structure representing gap on temperature exceptions
        self.light_pollution_prevention = light_pollution_prevention

    def __repr__(self):
        return f"{super().__repr__()}, material={self.material}, close_below={self.close_below}, close_above={self.close_above}, tout_max={self.tout_max}, gapOnTempExc={self.gapOnTempExc}  , light_pollution_prevention = {self.light_pollution_prevention}"

    def get_settings(self):
        """
        Retrieves the screen's current settings as a formatted string.

        Returns:
            str: A string representation of the screen's settings.
        """
        return (f"{super().get_settings()}, Material: {self.material}, Close Below: {self.close_below}, "
                f"Close Above: {self.close_above}, Tout Max Periods: {self.tout_max}, "
                f"Gap on Temp Exc: {self.gapOnTempExc}, Light Pollution Prevention: {self.light_pollution_prevention}")

    def export(self):
        """
        Exports the screen settings to a dictionary format for easy serialization or processing.
        Conditionally includes 'gapOnTempExc' only if it's not an empty string.

        Returns:
            dict: A dictionary representing the screen's settings.
        """
        data = {
            "@enabled": self.enabled,
            "@material": self.material,
            "@closeBelow": self.close_below,
            "@closeAbove": self.close_above,
            "@ToutMax": self.tout_max,
            "@lightPollutionPrevention": self.light_pollution_prevention
        }

        if self.gapOnTempExc != "":
            data["@gapOnTempExc"] = self.gapOnTempExc

        return data
        # return {self.name: data}

    @staticmethod
    def describe():
        """
        Describes the Screen's features and attributes.
        """
        description = ("Screen: Manages light and temperature entry. "
                       "Key attributes are material (type of screen material), close_below "
                       "(light intensity threshold to close), close_above (light intensity threshold to open), "
                       "tout_max (maximum outside temperature for operation), and "
                       "light_pollution_prevention (whether it prevents light pollution).")
        return description
class illumination(Device):
    """
    Represents an illumination device in the greenhouse, controlling light intensity and duration to
    optimize plant growth conditions.

    Inherits from the Device class.

    Attributes:
        intensity (float): The light intensity of the illumination device.
        hours_light (float): The number of hours the light is provided per day.
        end_time (float): The hour of the day when the illumination ends.
        max_iglob (float): The maximum global radiation allowed before the illumination is reduced.
        max_par_sum (float): The maximum photosynthetically active radiation sum allowed.
    """

    def __init__(self, name, type, intensity, hours_light, end_time, max_iglob, max_par_sum, enabled=True):
        """
        Initializes a new Illumination instance with specified properties.

        Parameters:
            name (str): The name of the illumination device.
            intensity (float): Light intensity level.
            hours_light (float): Duration of light provided in hours.
            end_time (float): The time of day when illumination ends.
            max_iglob (float): Maximum global radiation threshold.
            max_par_sum (float): Maximum PAR sum threshold.
        """
        super().__init__(name)
        self.enabled=enabled
        self.type = type
        self.intensity = intensity
        self.hours_light = hours_light  # Dictionary for hours of light over periods
        self.end_time = end_time
        self.max_iglob = max_iglob
        self.max_par_sum = max_par_sum

    def __repr__(self):
        return f"{super().__repr__()}, type={self.type}, intensity={self.intensity}, hours_of_light={self.hours_of_light}, end_time={self.end_time}, max_iglob={self.max_iglob}, max_par_sum={self.max_par_sum}"

    def get_settings(self):
        """
        Retrieves the illumination device's current settings as a formatted string.

        Returns:
            str: A string representation of the illumination device's settings.
        """
        return (f"{super().get_settings()}, Type: {self.type}, Intensity: {self.intensity}, "
                f"Hours Light Periods: {self.hours_light}, End Time: {self.end_time}, "
                f"Max Iglob: {self.max_iglob}, Max PAR Sum: {self.max_par_sum}")

    def export(self):
        """
        Exports the illumination settings to a dictionary format for easy serialization or processing.

        Returns:
            dict: A dictionary representing the illumination's settings.
        """
        return {
                "@enabled": self.enabled,
                "@type": self.type,
                "@intensity": self.intensity,
                "@hoursLight": self.hours_light,
                "@endTime": self.end_time,
                "@maxIglob": self.max_iglob,
                "@maxPARsum": self.max_par_sum
        }

    @staticmethod
    def describe():
        """
        Describes the Illumination device's features and attributes.
        """
        description = ("Illumination: Controls light intensity and duration for optimal plant growth. "
                       "Attributes include intensity (light intensity), hours_light (hours of light provided per day), "
                       "end_time (when illumination ends), max_iglob (maximum global radiation before reduction), "
                       "and max_par_sum (maximum photosynthetically active radiation sum allowed).")
        return description

class setpoints(Device):
    """
    Manages setpoints for temperature, CO2, and ventilation within the greenhouse.
    Extends the base Device class and organizes complex configurations for controlling environmental parameters.

    Attributes:
        name (str): The name of the setpoints group.
        temp_settings (dict): A dictionary containing all temperature-related settings.
        co2_settings (dict): Settings for CO2 control.
        ventilation_settings (dict): Settings for managing ventilation parameters.
        enabled (bool): Status indicating if the setpoints are active.
    """
    def __init__(self, name,temp=None,CO2=None,ventilation=None):
        super().__init__(name)
        self.temp = TempSettings(**(temp if temp is not None else {}))
        self.CO2 = CO2Settings(**(CO2 if CO2 is not None else {}))
        self.ventilation = VentilationSettings(**(ventilation if ventilation is not None else {}))


    def __repr__(self):
        return f"{super().__repr__()}, temp={self.temp}, CO2={self.CO2}, ventilation={self.ventilation}"

    def set_temp_settings(self, heating_temp, radiation_influence, vent_offset, pband_vent):
        """
        Sets all temperature-related settings at once.

        Parameters:
            heating_temp (dict): Heating temperature settings with conditions and values.
            radiation_influence (str): Radiation influence settings.
            vent_offset (dict): Ventilation offset settings with conditions and values.
            pband_vent (str): Proportional band ventilation settings.
        """
        self.temp.set_settings(heating_temp, radiation_influence, vent_offset, pband_vent)


    def set_co2_settings(self, setpoint, setp_if_lamps, dose_capacity):
        """
        Sets the configuration for managing CO2 within the greenhouse.

        Parameters:
            setpoint (dict): Specifies the CO2 concentration setpoints over time.
                             Keys are date ranges and values are sub-dictionaries with specific rules (e.g., 'r+0.5': 400).
            setp_if_lamps (dict): Specifies CO2 setpoints when lamps are active, formatted similarly to setpoint.
            dose_capacity (dict): Dictates the CO2 dosing capacities, with date ranges and specific values or ranges.

        This method updates the CO2 settings directly affecting the greenhouse's CO2 regulation capabilities.
        """
        self.CO2.set_settings(setpoint, setp_if_lamps, dose_capacity)


    def set_ventilation_settings(self, win_lee_min, win_lee_max, win_wnd_min, win_wnd_max, start_wnd):
        """
        Sets the configuration for managing the ventilation system within the greenhouse.

        Parameters:
            win_lee_min (dict): Minimum limits for window leeway settings based on time.
            win_lee_max (dict): Maximum limits for window leeway settings.
            win_wnd_min (dict): Minimum window wind settings, providing lower thresholds for ventilation based on time.
            win_wnd_max (dict): Maximum window wind settings, setting upper thresholds for ventilation.
            start_wnd (dict): Starting points for window operations, defined by specific times.

        This method updates the ventilation settings which are critical for maintaining proper air exchange and environment control.
        """
        self.ventilation.set_settings(win_lee_min, win_lee_max, win_wnd_min, win_wnd_max, start_wnd)


    def get_settings(self):
        """
        Retrieves all setpoint settings as a structured dictionary.

        Returns:
            dict: The comprehensive settings including temperature, CO2, and ventilation.
        """
        return {
            "temp": self.temp.export(),
            "CO2": self.CO2.export(),
            "ventilation": self.ventilation.export()
        }
        # return {
        #     "temp": self.temp,
        #     "CO2": self.CO2,
        #     "ventilation": self.ventilation
        # }

    def export(self):
        """
        Exports the setpoints settings to a dictionary format for easy serialization or processing.
        This method structures the configuration into a readable and manageable format.

        Returns:
            dict: A dictionary representing the setpoints' settings organized by category.
        """
        return {
            "temp": self.temp.export(),
            "CO2": self.CO2.export(),
            "ventilation": self.ventilation.export()
        }

    @staticmethod
    def describe():
        """
        Describes the purpose and function of the Setpoints class within the greenhouse system.

        Returns:
            str: A descriptive string outlining the role of Setpoints in managing environmental controls.
        """
        return ("Setpoints manage the critical control points for temperature, CO2, and ventilation "
                "within the greenhouse. These settings help ensure optimal growing conditions by "
                "adjusting various environmental parameters according to predefined schedules and conditions.")

class TempSettings:
    def __init__(self, **kwargs):
        self.heatingTemp = kwargs.get('heatingTemp', None)
        self.radiationInfluence = kwargs.get('radiationInfluence', None)
        self.ventOffset = kwargs.get('ventOffset', None)
        self.PbandVent = kwargs.get('PbandVent', None)

    def export(self):
        return {
            "@heatingTemp": self.heatingTemp,
            "@radiationInfluence": self.radiationInfluence,
            "@ventOffset": self.ventOffset,
            "@PbandVent": self.PbandVent
        }
    def set_settings(self, heating_temp, radiation_influence, vent_offset, pband_vent):
        self.heatingTemp = heating_temp
        self.radiationInfluence = radiation_influence
        self.ventOffset = vent_offset
        self.PbandVent = pband_vent

class CO2Settings:
    def __init__(self, **kwargs):
        self.setpoint = kwargs.get('setpoint', None)
        self.setpIfLamps = kwargs.get('setpIfLamps', None)
        self.doseCapacity = kwargs.get('doseCapacity', None)

    def export(self):
        return {
            "@setpoint": self.setpoint,
            "@setpIfLamps": self.setpIfLamps,
            "@doseCapacity": self.doseCapacity
        }
    def set_settings(self, setpoint, setp_if_lamps, dose_capacity):
        self.setpoint = setpoint
        self.setpIfLamps = setp_if_lamps
        self.doseCapacity = dose_capacity



class VentilationSettings:
    def __init__(self, **kwargs):
        self.winLeeMin = kwargs.get('winLeeMin', None)
        self.winLeeMax = kwargs.get('winLeeMax', None)
        self.winWndMin = kwargs.get('winWndMin', None)
        self.winWndMax = kwargs.get('winWndMax', None)
        self.startWnd = kwargs.get('startWnd', None)

    def __repr__(self):
        return f"@winLeeMin={self.winLeeMin}, @winLeeMax={self.winLeeMax}, @winWndMin={self.winWndMin}, @winWndMax={self.winWndMax}, @startWnd={self.startWnd})"

    def set_settings(self, win_lee_min, win_lee_max, win_wnd_min, win_wnd_max, start_wnd):
        self.winLeeMin = win_lee_min
        self.winLeeMax = win_lee_max
        self.winWndMin = win_wnd_min
        self.winWndMax = win_wnd_max
        self.startWnd = start_wnd

    def export(self):
        return {
            "@winLeeMin": self.winLeeMin,
            "@winLeeMax": self.winLeeMax,
            "@winWndMin": self.winWndMin,
            "@winWndMax": self.winWndMax,
            "@startWnd": self.startWnd
        }