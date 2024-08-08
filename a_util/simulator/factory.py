import sys
from a_util.simulator.devices import CO2dosing, heatingpipes, screens, illumination, setpoints

sys.path.append('./')

class DeviceFactory:
    """
    A factory class for creating and configuring device instances for the greenhouse system.
    This class abstracts the creation logic, making it easy to add new device types and manage
    their configuration in a centralized manner.
    """

    @staticmethod
    def create_device(device_type, name, **kwargs):
        """
        Creates a device instance based on the specified device type.

        Parameters:
            device_type (str): The type of device to create. It must match one of the predefined
                               device class names (e.g., 'CO2DosingSystem').
            name (str): The name of the device.
            **kwargs: Arbitrary keyword arguments that are passed directly to the device's constructor.

        Returns:
            Device: An instance of the requested device type.

        Raises:
            ValueError: If the specified device type does not match any known device classes.
        """
        if device_type == 'CO2dosing':
            return CO2dosing(name, **kwargs)
        elif device_type == 'heatingpipes':
            return heatingpipes(name, **kwargs)
        elif device_type == 'screens':
            return screens(name, **kwargs)
        elif device_type == 'illumination':
            return illumination(name, **kwargs)
        elif device_type == 'setpoints':
            return setpoints(name, **kwargs)
        else:
            raise ValueError(f"Unknown device type: {device_type}")

    @staticmethod
    def update_device_parameter(device, parameter_name, value):
        """
        Updates a specific parameter of a device.

        This method dynamically sets an attribute of a device if the attribute exists, enhancing
        the flexibility of device configuration management.

        Parameters:
            device (Device): The device instance to update.
            parameter_name (str): The name of the parameter to update.
            value: The new value to assign to the parameter.

        Raises:
            AttributeError: If the specified device does not have the given parameter.
        """
        if hasattr(device, parameter_name):
            setattr(device, parameter_name, value)
        else:
            raise AttributeError(f"Device does not have a '{parameter_name}' attribute.")

    @staticmethod
    def create_and_configure(device_type, name, **kwargs):
        """
        Creates a device and applies initial settings all in one step. This method is useful for
        initializing devices with specific configurations right upon their creation.

        Parameters:
            device_type (str): The type of device to create.
            name (str): The name of the device.
            **kwargs: Arbitrary keyword arguments for device creation. This can include a special
                      'initial_settings' dictionary for configurations that should be applied
                      immediately after creation.

        Returns:
            Device: An instance of the created and configured device.
        """
        device = DeviceFactory.create_device(device_type, name, **kwargs)
        initial_settings = kwargs.pop('initial_settings', {})
        for key, value in initial_settings.items():
            DeviceFactory.update_device_parameter(device, key, value)
        return device
