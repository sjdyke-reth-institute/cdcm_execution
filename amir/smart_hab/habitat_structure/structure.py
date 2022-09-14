"""
Author: Amir Behjat

Date:
    7/08/2022


Defines the struct interface/type/system/concept.

A `structEnvironment` is `System` that exposes the following interface:


variable :: TypeOfVariable

(variable) = optional variable

                                               _________________
moon             :: Moon                   => |                 | -> strucure_health         :: State[array]
(int_env)        :: InteriorEnv            => |    StructEnv    |
agents           :: Agents                 => |                 |
design           :: DomeSpec               => |_________________| -> strucure_temp_innerside :: State

"""

from cdcm import *
from . import make_struct_health_env_0
from . import make_struct_temp_env_0

from dome_design import *


__all__ = ["make_structure"]


def make_structure(
    dome_specs,
    irradiance,
    surface_temperature,
    meteor_impacts_1,
    meteor_impacts_2,
    meteor_impacts_3,
    meteor_impacts_4,
    meteor_impacts_5,
    interior_environment_int_env_temp=None,
    agent_repair_struct=None,
    make_struct_health_env=make_struct_health_env_0,
    make_struct_temp_env=make_struct_temp_env_0,
):
    """
    Make a struct system.

    Arguments
    moon
    dome_specs,
    interior_environment_int_env_temp
    agent_dome_repair

    """
    with System(name="struct", description="The struct system") as struct:
        if interior_environment_int_env_temp is None:
            interior_environment_int_env_temp = Variable(
                name="place_holder_int_env_temp",
                units="K",
                value=280.0,
                description="Temparature of the interior environment",
            )
        if agent_repair_struct is None:
            agent_repair_struct = Variable(
                name="place_holder_agent_repair_struct",
                units="",
                value=[0.0, 0.0, 0.0, 0.0, 0.0],
                description="The array of how much repair is given to each dome section in unit of time step",
            )
        struct_health = make_struct_health_env(
            meteor_impacts_1,
            meteor_impacts_2,
            meteor_impacts_3,
            meteor_impacts_4,
            meteor_impacts_5,
            agent_repair_struct,
        )

        struct_temp = make_struct_temp_env(
            dome_specs,
            irradiance,
            surface_temperature,
            struct_health,
            interior_environment_int_env_temp,
        )

    return struct
