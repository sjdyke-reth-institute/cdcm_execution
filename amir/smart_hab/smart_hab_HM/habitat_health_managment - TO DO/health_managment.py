"""
Defines the HM interface/type/system/concept.

A `HMEnvironment` is `System` that exposes the following interface:


variable :: TypeOfVariable

(variable) = optional variable

                                          _________________
moon          :: Moon                 => |                 |
energy        :: Energy               => |                 | -> task_list             :: State[array]
eclss         :: Eclss                => |                 |
struct        :: Struct               => |                 |
interior_env  :: InteriorEnv          => |      HMEnv      |
agents        :: Agents               => |                 |
clock         :: Clock                => |                 | -> temprature_set_points :: State[array]
design        :: DomeSpec             => |_________________| -> pressurre_set_points  :: State[array]


"""


__all__ = ["make_eclss"]


from cdcm import *
from . import make_health_managment_detection_env_0
from . import make_health_managment_cyber_env_0
from . import make_health_managment_physical_env_0


def make_eclss(
    clock,
    dome_specs,
    moon,
    energy,
    eclss,
    struct,
    interior_env,
    agents,
    make_health_managment_detection_env=make_health_managment_physical_env_0,
    make_health_managment_cyber_env=make_health_managment_cyber_env_0,
    make_health_managment_physical_env=make_health_managment_physical_env_0,
):
    """
    Make an HM system.

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
    with System(name="HM", description="The HM system") as HM:
        if energy_available_energy is None:
            energy_available_energy = Variable(
                name="place_holder_available_en",
                value=0.0,
                units="J",
                description="Available battery",
            )

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

    return HM
