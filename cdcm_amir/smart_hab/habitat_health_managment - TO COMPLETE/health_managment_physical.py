"""An health_managment_physical model.

variable :: TypeOfVariable

(variable) = optional variable


                                                                      _______________________________
moon                               :: Moon                        => |                               |
energy                             :: Energy                      => |                               |
eclss                              :: Eclss                       => |                               |
struct                             :: Struct                      => |                               |
interior_env                       :: InteriorEnv                 => |  health_managment_physicalEnv | -> agents_command  :: ُState
agents                             :: Agents                      => |                               |
health_managment_detection         :: Health_managment_detection  => |                               |
clock                              :: Clock                       => |                               |
design                             :: DomeSpec                    => |_______________________________|


"""

from cdcm import *
import numpy as np

__all__ = ["make_health_managment_physical_env_0"]


def make_health_managment_physical_env_0(
    clock,
    dome_specs,
    moon,
    energy,
    eclss,
    struct,
    interior_env,
    agents,
    health_managment_detection,
):
    with System(
        name="health_managment_physical",
        description="The health_managment_physical environment",
    ) as health_managment_physical:

        agents_command = Variable(
            name="agents_command",
            value=[],
            units="",
            description="The model of agents in health_managment mind",
        )

        @make_function(agents_command)
        def f_physical():
            """Transition function for health_managment physical"""
            agents_command = []
            return health_managment_physical
