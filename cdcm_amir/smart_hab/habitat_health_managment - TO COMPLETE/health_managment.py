"""
Defines the health_managment interface/type/system/concept.

A `health_managmentEnvironment` is `System` that exposes the following interface:


variable :: TypeOfVariable

(variable) = optional variable

                                          _______________________________
moon          :: Moon                 => |                               |
energy        :: Energy               => |                               |
eclss         :: Eclss                => |                               |
struct        :: Struct               => |                               |
interior_env  :: InteriorEnv          => |      health_managmentEnv      | -> agents_command        :: State[array]
agents        :: Agents               => |                               |
clock         :: Clock                => |                               | -> temprature_set_points :: State[array]
design        :: DomeSpec             => |_______________________________| -> pressurre_set_points  :: State[array]


"""

from cdcm import *
from . import make_health_managment_detection_env_0
from . import make_health_managment_cyber_env_0
from . import make_health_managment_physical_env_0

__all__ = ["make_eclss"]


def make_eclss(
    clock,
    dome_specs,
    moon,
    energy,
    eclss,
    struct,
    interior_env,
    agents,
    make_health_managment_detection_env=make_health_managment_detection_env_0,
    make_health_managment_cyber_env=make_health_managment_cyber_env_0,
    make_health_managment_physical_env=make_health_managment_physical_env_0,
):
    """
    Make an health_managment system.

    Arguments
    clock
    moon
    dome_specs,
    energy,
    eclss,
    struct,
    interior_env,
    agents,
    """
    with System(
        name="health_managment", description="The health_managment system"
    ) as health_managment:

        health_managment_detection = make_health_managment_detection_env(
            clock, dome_specs, moon, energy, eclss, struct, interior_env
        )

        health_managment_cyber = make_health_managment_cyber_env(
            clock,
            dome_specs,
            moon,
            energy,
            eclss,
            struct,
            interior_env,
            health_managment_detection,
        )

        health_managment_physical = make_health_managment_physical_env(
            clock,
            dome_specs,
            moon,
            energy,
            eclss,
            struct,
            interior_env,
            health_managment_detection,
            agents,
        )

    return health_managment
