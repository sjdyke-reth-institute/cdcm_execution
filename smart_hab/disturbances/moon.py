"""
Author: Amir Behjat

Date:
    7/08/2022

Defines the MoonEnvironment interface/type/system/concept.

A `MoonEnvironment` is `System` that exposes the following interface:

variable :: TypeOfVariable

(variable) = optional variable

                                        _________________ -> half_day_light :: Parameter
clock            :: Clock          => |                 | -> dust           :: Variable
                                      | MoonEnvironment | -> thermal        :: Variable
(path_data_file) :: String         => |                 | -> radiation      :: Variable
design           :: DomeSpec       => |_________________| -> meteorite      :: Variable[array]



"""


from cdcm import *
from . import make_dust_env_0
from . import make_radiation_env_0
from . import make_thermal_env_0
from . import make_meteor_env_0
from dome_design import *
import pandas as pd

__all__ = ["make_moon"]


def make_moon(
    clock,
    dome_specs,
    data_files_address=None,
    make_dust_env=make_dust_env_0,
    make_radiation_env=make_radiation_env_0,
    make_thermal_env=make_thermal_env_0,
    make_meteor_env=make_meteor_env_0
):
    """
    Make a moon system.

    Arguments
    clock -- A clock object measuring time in seconds.
             TODO: Clock should be in Julian time.
    domeSpecs -- For all parameters affecting the system
    data_files_address

    """
    with System(name="moon", description="The moon system") as moon:
        if data_files_address is None:
            data_files_address = './data_files/'

        half_day_light = Parameter(
            name="half_day_light",
            value=29.5306 * 3600 * 12,
            units="sec",
            description="The period of time during which the sun is shining"
        )
        meteorite_df = Parameter(
            name="meteorite_df",
            value=pd.read_csv(data_files_address + "meteorite_impacts.csv"),
            units="sec",
            description="The data frame of meteor strikes samples"
        )
        meteor_samp_location = Parameter(
            name="meteor_samp_location",
            value=meteorite_df.value['location'].to_numpy(),
            units="",
            description="Location of meteor strike in dome; samples list"
        )
        meteor_samp_impact = Parameter(
            name="meteor_samp_impact",
            value=meteorite_df.value['energy'].to_numpy(),
            units="",
            description="Damage of meteor strike in dome; samples list"
        )
        # I would love to have things depend on these:
        # longitude =
        # latitude =
        # height =

        dust = make_dust_env(clock)

        radiation = make_radiation_env(clock, moon)

        thermal = make_thermal_env(clock, moon)

        meteor = make_meteor_env(clock, moon, dome_specs)

    return moon
