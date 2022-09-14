"""A MoonThermalEnvironment

                    ___________________________
                   |                           |
clock :: Clock  => |  MoonRadiationEnvironment |-> surface_temperature :: Variable
moon  :: Moon   => |___________________________|

"""


__all__ = ["make_thermal_env_0"]


from cdcm import *
from . import is_loonar_day

import math

def make_thermal_env_0(clock, moon):
    with System(name="thermal") as thermal:
        surface_temperature = Variable(
            name="surface_temperature",
            value=0.0,
            units="K",
            description="Temperature of the lunar surface."
        )

        max_external_temp = Parameter(
            name="max_external_temp",
            value=400.0,
            units="K",
            description="The maximum temperature on the lunar surface."
        )

        min_external_temp = Parameter(
            name="min_external_temp",
            value=100.0,
            units="K",
            description="The minimum temperature on the lunar surface."
        )

        @make_function(surface_temperature)
        def f_surface_temp(
            half_day_light=moon.half_day_light,
            max_external_temp=max_external_temp,
            min_external_temp=min_external_temp,
            t=clock.t
        ):
            """Evaluate the loon surface temperature at a given time."""

            if not is_loonar_day(t, half_day_light):
                return min_external_temp
            else:
                return ((max_external_temp - min_external_temp) *
                        math.sin(math.pi * t / half_day_light) +
                        min_external_temp)
    return thermal
