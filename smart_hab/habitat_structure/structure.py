"""
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



__all__ = ["make_structure"]


from cdcm import *
from . import make_structure_health_env_0
from . import make_structure_temp_env_0

from dome_design import *


def make_structure(moon,
                   dome_specs,
                   interior_environment_int_env_temp=None,
                   agent_repair_struct=None,
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
        if interior_environment_int_env_temp is None:
            interior_environment_int_env_temp = Variable(name="int_env_temp", value=280.0, units="K", description="Interior Environment Temperature")
        if agent_repair_struct is None:
            agent_repair_struct = Variable(name="agent_repair_struct", value=[0.0, 0.0, 0.0, 0.0, 0.0], units="", description="Agent's given health improvment for each dome section")
        struct_health = make_struct_health_env(moon, agent_repair_struct)

        struct_temp = make_struct_temp_env(struct_health,
                                           dome_specs, moon,
                                           interior_environment_int_env_temp
                                           )

    return struct

