"""
Write me 
"""


__all__ = ["make_resource_generator"]


from cdcm import *
from typing import Union

from common import maybe_make_system


def make_resource_generator(name_or_system : Union[str,System],
                            resource_input : Variable,
                            resource_name : str,
                            resource_units : str,
                            resource_default_value : float = 0.0,
                            resource_input_local_name : Union[None, str] = None,
                            **kwargs):

    sys = maybe_make_system(name_or_system, **kwargs)
    with sys:
        if resource_input_local_name is None:
            local_input_name = resource_input.name
        else:
            local_input_name = resource_input_local_name
        resource_input_local_copy = Variable(name=local_input_name,
                                             units=resource_input.units,
                                             value=resource_input.value,
                                             description=resource_input.description + " (local copy)")
        @make_function(resource_input_local_copy)
        def copy_resource_input(x=resource_input):
            return x
        resource_output = Variable(name=resource_name + "_output",
                                     value=resource_default_value,
                                     units=resource_units)

    return sys


if __name__ == "__main__":
    from physical_object import *

    with System(name="moon") as moon:
        irradiance = Variable(name="irradiance", units="W/m^2", value=1000.0,
                              description="Dummy irradiance")

    solar = make_resource_generator(make_physical_system("solar"),
                                    moon.irradiance, "power", "W")
    with solar:
        area = Parameter(name="area", value=10.0, units="m^2")
        efficiency = Variable(name="efficiency", value=1.0, units="")
        @make_function(solar.power_output)
        def calculate_power(I=solar.irradiance, A=area, eta=efficiency):
            return A * eta * I

    print(solar)
