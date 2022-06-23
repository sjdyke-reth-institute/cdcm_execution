"""
Defines the struct interface/type/system/concept.

A `structEnvironment` is `System` that exposes the following interface:

                                               _________________
disturbance        :: iradiance            => |                 | -> strucure_health           :: structure_health_env
disturbance        :: surface temperature  => |                 |
disturbance        :: meteor model         => |    StructEnv    |
Interior-Env       :: Interior-Env_temp    => |                 |
Agents             :: Dome Repair          => |                 |
Design             :: Dome design & specs  => |_________________| -> strucure_temp             :: structure_temp_env


"""



__all__ = ["make_structure"]


from cdcm import *
from . import make_structure_health_env_0
from . import make_structure_temp_env_0

from dome_design import *


def make_structure(moon,
                   dome_specs,
                   interior_environment_int_env_temp,
                   agent_repair_struct_temp,
                   make_struct_health_env=make_structure_health_env_0,
                   make_struct_temp_env=make_structure_temp_env_0,
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

        struct_health = make_struct_health_env(moon, agent_repair_struct_temp)

        struct_temp = make_struct_temp_env(struct_health,
                                           dome_specs, moon,
                                           interior_environment_int_env_temp
                                           )

    return struct

