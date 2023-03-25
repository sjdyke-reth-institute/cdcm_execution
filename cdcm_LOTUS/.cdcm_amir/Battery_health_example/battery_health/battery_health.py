"""
Author: Amir Behjat

Date:
    7/08/2022


Defines the battery_health interface/type/system/concept.

A `battery_healthEnvironment` is `System` that exposes the following interface:


variable :: TypeOfVariable

(variable) = optional variable

                                       ____________________
clock         :: Clock             => |                   |
disturbances  :: Disturbances      => | battery_healthEnv | -> battery_health  :: State
batteryspec   :: BatterySpec       => |___________________|


"""

from cdcm import *
from . import make_battery_health_degaradation_env_linear
from . import make_battery_health_degaradation_env_exponential_decay
from . import make_battery_health_degaradation_env_matrix_probability

from . import make_battery_health_shock_current_env_without_cooling
from . import make_battery_health_shock_current_env_with_cooling
from . import make_battery_health_shock_current_env_without_cooling_degraded_life
from . import make_battery_health_shock_current_env_with_cooling_degraded_life

from . import make_battery_health_overal_env_multipication
from . import make_battery_health_overal_env_min

# from . import make_battery_health_overal_env_harmonic_mean

from battery_design import *

__all__ = ["make_battery_health"]


def make_battery_health(
    clock,
    battery_specs,
    high_current,
    make_battery_health_degaradation_env=make_battery_health_degaradation_env_exponential_decay,
    make_battery_health_shock_env=make_battery_health_shock_current_env_with_cooling_degraded_life,
    make_battery_health_overal_env=make_battery_health_overal_env_min,
):
    """
    Make a struct system.

    Arguments
    disturbances
    battery_specs,

    """
    with System(
        name="battery_health", description="The battery_health system"
    ) as battery_health:

        make_battery_health_degaradation = make_battery_health_degaradation_env(
            clock, battery_specs
        )

        make_battery_health_shock = make_battery_health_shock_env(
            battery_specs,
            high_current,
            make_battery_health_degaradation.battery_degeradation_state,
        )

        make_battery_health_overal = make_battery_health_overal_env(
            make_battery_health_degaradation, make_battery_health_shock
        )

    return battery_health
