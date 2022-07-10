"""
Author: Amir Behjat

Date:
    7/08/2022

An MoonRadiationEnvironment.

                    ___________________________
                   |                           |
clock :: Clock  => |  MoonRadiationEnvironment |-> irradiance :: Variable
moon  :: Moon   => |___________________________|

Specification of irradiance:
        irradiance = Variable(
            name="irradiance",
            value=0.0,
            units="W/m^2",
            description="The horizontal total irradiance on moon surface."
        )

A constructor must requires as inputs instances of `Clock` and `MoonEnvironment`.

"""

from cdcm import *
from . import is_loonar_day
import math


__all__ = ["make_radiation_env_0"]


def make_radiation_env_0(clock, moon):
    with System(name="radiation",
                description="The irradiance environment") as radiation:
        irradiance = Variable(
            name="irradiance",
            value=0.0,
            units="W/m^2",
            description="The horizontal total irradiance on moon surface."
        )   # was Variable; Change it to State for consistency if you want

        irradiance_max = Parameter(
            name="irradiation_max",
            value=1450.0,
            units="W/m^2",
            description="The maximum solar irradiance. Power."
            + "Note: This ignores the rotation of the Earth arround the sun."
            + "The real value is actualy +- 7% this over the course of a year."
        )

        @make_function(irradiance)
        def f_irradiance(
            half_day_light=moon.half_day_light,
            irradiance_max=irradiance_max,
            t=clock.t
        ):
            """Calculate the solar irradiance"""
            # Is it day or night?
            if not is_loonar_day(t, half_day_light):
                # It's night
                return 0.0
            else:
                # It's day
                return irradiance_max * math.sin(math.pi * t / half_day_light)
    return radiation
