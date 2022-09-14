"""
Author: Amir Behjat

Date:
    7/12/2022


A battery_shock_current model.

variable :: TypeOfVariable

(variable) = optional variable

                                          ________________________________
battery_specs        :: BatterySpecs  => |                                |
                                         |                                |
                                         |battery_health_shock_currentEnv | ->  battery_shock_current_health :: State
clock               :: Clock          => |                                |
                                          ________________________________

"""
import math

from cdcm import *
import numpy as np


__all__ = [
    "make_battery_health_shock_current_env_without_cooling",
    "make_battery_health_shock_current_env_with_cooling",
    "make_battery_health_shock_current_env_without_cooling_degraded_life",
    "make_battery_health_shock_current_env_with_cooling_degraded_life",
]


def make_battery_health_shock_current_env_without_cooling(
    battery_specs, high_current, battery_health_degaradation_state
):
    with System(
        name="battery_shocked", description="The battery_shocked environment"
    ) as battery_shocked:

        battery_shock_current_state = State(
            name="battery_shock_current_state",
            value=1.0,
            units="",
            description="State of Battery shocked; 1: Healthiest. 0: Dead Battery",
        )

        battery_nominal_max_current_damage = Parameter(
            name="battery_nominal_max_current_damage",
            value=0.2,
            units="",
            description="How much damage battery_nominal_max_current will cause in 1 time step",
        )
        battery_short_time_max_current_damage = Parameter(
            name="battery_short_time_max_current_damage",
            value=0.7,
            units="",
            description="How much damage battery_short_time_max_current_damage will cause in 1 time step",
        )

        @make_function(battery_shock_current_state)
        def f_battery_shock_current_state(
            battery_shock_current_state=battery_shock_current_state,
            high_current=high_current,
            battery_nominal_max_current=battery_specs.battery_nominal_max_current,
            battery_short_time_max_current=battery_specs.battery_short_time_max_current,
            battery_ultimate_max_current=battery_specs.battery_ultimate_max_current,
            battery_short_time_max_current_damage=battery_short_time_max_current_damage,
            battery_nominal_max_current_damage=battery_nominal_max_current_damage,
        ):
            """Transition function for battery_shock_current_state"""
            if high_current >= battery_ultimate_max_current:
                battery_shock_current_state_new = 0.0
            elif high_current >= battery_short_time_max_current:
                battery_shock_current_state_new = max(
                    0.0,
                    battery_shock_current_state - battery_short_time_max_current_damage,
                )
            elif high_current >= battery_nominal_max_current:
                battery_shock_current_state_new = max(
                    0.0,
                    battery_shock_current_state - battery_nominal_max_current_damage,
                )
            else:
                battery_shock_current_state_new = battery_shock_current_state
            return battery_shock_current_state_new

    return battery_shocked


def make_battery_health_shock_current_env_with_cooling(
    battery_specs, high_current, battery_health_degaradation_state
):
    with System(
        name="battery_shocked", description="The battery_shocked environment"
    ) as battery_shocked:

        battery_shock_current_state = State(
            name="battery_shock_current_state",
            value=1.0,
            units="",
            description="State of Battery shocked; 1: Healthiest. 0: Dead Battery",
        )

        battery_nominal_max_current_damage = Parameter(
            name="battery_nominal_max_current_damage",
            value=0.2,
            units="",
            description="How much damage battery_nominal_max_current will cause in 1 time step",
        )
        battery_short_time_max_current_damage = Parameter(
            name="battery_short_time_max_current_damage",
            value=0.7,
            units="",
            description="How much damage battery_short_time_max_current_damage will cause in 1 time step",
        )
        battery_refrigerant_cooling_allowance = Parameter(
            name="battery_refrigerant_cooling_allowance",
            value=2.5,
            units="",
            description="How much more current we can have if the water cooling is provided",
        )
        battery_water_cooling_allowance = Parameter(
            name="battery_water_cooling_allowance",
            value=1.523,
            units="",
            description="How much more current we can have if the water cooling is provided",
        )
        battery_air_cooling_allowance = Parameter(
            name="battery_air_cooling_allowance",
            value=1.00,
            units="",
            description="How much more current we can have if the water cooling is provided",
        )
        battery_cooling_method = Parameter(
            name="battery_cooling_method",
            value="r",
            units="",
            description="a string about what type of cooling method is used; r:refrigerant; w:water; a:air",
        )

        @make_function(battery_shock_current_state)
        def f_battery_shock_current_state(
            battery_shock_current_state=battery_shock_current_state,
            high_current=high_current,
            battery_nominal_max_current=battery_specs.battery_nominal_max_current,
            battery_short_time_max_current=battery_specs.battery_short_time_max_current,
            battery_ultimate_max_current=battery_specs.battery_ultimate_max_current,
            battery_short_time_max_current_damage=battery_short_time_max_current_damage,
            battery_nominal_max_current_damage=battery_nominal_max_current_damage,
            battery_refrigerant_cooling_allowance=battery_refrigerant_cooling_allowance,
            battery_water_cooling_allowance=battery_water_cooling_allowance,
            battery_air_cooling_allowance=battery_air_cooling_allowance,
            battery_cooling_method=battery_cooling_method,
        ):
            """Transition function for battery_shock_current_state"""
            if battery_cooling_method == "r":
                current_allowance_gain = battery_refrigerant_cooling_allowance
            elif battery_cooling_method == "w":
                current_allowance_gain = battery_water_cooling_allowance
            elif battery_cooling_method == "a":
                current_allowance_gain = battery_air_cooling_allowance

            if high_current >= battery_ultimate_max_current * current_allowance_gain:
                battery_shock_current_state_new = 0.0
            elif (
                high_current >= battery_short_time_max_current * current_allowance_gain
            ):
                battery_shock_current_state_new = max(
                    0.0,
                    battery_shock_current_state - battery_short_time_max_current_damage,
                )
            elif high_current >= battery_nominal_max_current * current_allowance_gain:
                battery_shock_current_state_new = max(
                    0.0,
                    battery_shock_current_state - battery_nominal_max_current_damage,
                )
            else:
                battery_shock_current_state_new = battery_shock_current_state
            return battery_shock_current_state_new

    return battery_shocked


def make_battery_health_shock_current_env_without_cooling_degraded_life(
    battery_specs, high_current, battery_health_degaradation_state
):
    with System(
        name="battery_shocked", description="The battery_shocked environment"
    ) as battery_shocked:

        battery_shock_current_state = State(
            name="battery_shock_current_state",
            value=1.0,
            units="",
            description="State of Battery shocked; 1: Healthiest. 0: Dead Battery",
        )

        battery_nominal_max_current_damage = Parameter(
            name="battery_nominal_max_current_damage",
            value=0.2,
            units="",
            description="How much damage battery_nominal_max_current will cause in 1 time step",
        )
        battery_short_time_max_current_damage = Parameter(
            name="battery_short_time_max_current_damage",
            value=0.7,
            units="",
            description="How much damage battery_short_time_max_current_damage will cause in 1 time step",
        )
        battery_degeradation_decay = Parameter(
            name="battery_degeradation_decay",
            value=1.2,
            units="",
            description="How much damage battery is vulnerable to damage due to degeradation",
        )

        @make_function(battery_shock_current_state)
        def f_battery_shock_current_state(
            battery_shock_current_state=battery_shock_current_state,
            high_current=high_current,
            battery_nominal_max_current=battery_specs.battery_nominal_max_current,
            battery_short_time_max_current=battery_specs.battery_short_time_max_current,
            battery_ultimate_max_current=battery_specs.battery_ultimate_max_current,
            battery_short_time_max_current_damage=battery_short_time_max_current_damage,
            battery_nominal_max_current_damage=battery_nominal_max_current_damage,
            battery_degeradation_decay=battery_degeradation_decay,
            battery_health_degaradation_state=battery_health_degaradation_state,
        ):
            """Transition function for battery_shock_current_state"""
            if high_current >= battery_ultimate_max_current:
                battery_shock_current_state_new = 0.0
            elif high_current >= battery_short_time_max_current:
                battery_shock_current_state_new = max(
                    0.0,
                    battery_shock_current_state
                    - battery_short_time_max_current_damage
                    * battery_degeradation_decay
                    / (0.001 + battery_health_degaradation_state),
                )
            elif high_current >= battery_nominal_max_current:
                battery_shock_current_state_new = max(
                    0.0,
                    battery_shock_current_state
                    - battery_nominal_max_current_damage
                    * battery_degeradation_decay
                    / (0.001 + battery_health_degaradation_state),
                )
            else:
                battery_shock_current_state_new = battery_shock_current_state
            return battery_shock_current_state_new

    return battery_shocked


def make_battery_health_shock_current_env_with_cooling_degraded_life(
    battery_specs, high_current, battery_health_degaradation_state
):
    with System(
        name="battery_shocked", description="The battery_shocked environment"
    ) as battery_shocked:

        battery_shock_current_state = State(
            name="battery_shock_current_state",
            value=1.0,
            units="",
            description="State of Battery shocked; 1: Healthiest. 0: Dead Battery",
        )

        battery_nominal_max_current_damage = Parameter(
            name="battery_nominal_max_current_damage",
            value=0.2 * 10 ** (-3),
            units="",
            description="How much damage battery_nominal_max_current will cause in 1 time step",
        )
        battery_short_time_max_current_damage = Parameter(
            name="battery_short_time_max_current_damage",
            value=0.7 * 10 ** (-3),
            units="",
            description="How much damage battery_short_time_max_current_damage will cause in 1 time step",
        )
        battery_refrigerant_cooling_allowance = Parameter(
            name="battery_refrigerant_cooling_allowance",
            value=2.5,
            units="",
            description="How much more current we can have if the water cooling is provided",
        )
        battery_water_cooling_allowance = Parameter(
            name="battery_water_cooling_allowance",
            value=1.523,
            units="",
            description="How much more current we can have if the water cooling is provided",
        )
        battery_air_cooling_allowance = Parameter(
            name="battery_air_cooling_allowance",
            value=1.00,
            units="",
            description="How much more current we can have if the water cooling is provided",
        )
        battery_cooling_method = Parameter(
            name="battery_cooling_method",
            value="r",
            units="",
            description="a string about what type of cooling method is used; r:refrigerant; w:water; a:air",
        )
        battery_degeradation_decay = Parameter(
            name="battery_degeradation_decay",
            value=1.2,
            units="",
            description="How much damage battery is vulnerable to damage due to degeradation",
        )

        @make_function(battery_shock_current_state)
        def f_battery_shock_current_state(
            battery_shock_current_state=battery_shock_current_state,
            high_current=high_current,
            battery_nominal_max_current=battery_specs.battery_nominal_max_current,
            battery_short_time_max_current=battery_specs.battery_short_time_max_current,
            battery_ultimate_max_current=battery_specs.battery_ultimate_max_current,
            battery_short_time_max_current_damage=battery_short_time_max_current_damage,
            battery_nominal_max_current_damage=battery_nominal_max_current_damage,
            battery_refrigerant_cooling_allowance=battery_refrigerant_cooling_allowance,
            battery_water_cooling_allowance=battery_water_cooling_allowance,
            battery_air_cooling_allowance=battery_air_cooling_allowance,
            battery_cooling_method=battery_cooling_method,
            battery_degeradation_decay=battery_degeradation_decay,
            battery_health_degaradation_state=battery_health_degaradation_state,
        ):
            """Transition function for battery_shock_current_state"""
            if battery_cooling_method == "r":
                current_allowance_gain = battery_refrigerant_cooling_allowance
            elif battery_cooling_method == "w":
                current_allowance_gain = battery_water_cooling_allowance
            elif battery_cooling_method == "a":
                current_allowance_gain = battery_air_cooling_allowance

            if high_current >= battery_ultimate_max_current * current_allowance_gain:
                battery_shock_current_state_new = 0.0
            elif (
                high_current >= battery_short_time_max_current * current_allowance_gain
            ):
                battery_shock_current_state_new = max(
                    0.0,
                    battery_shock_current_state
                    - battery_short_time_max_current_damage
                    * battery_degeradation_decay
                    / (0.001 + battery_health_degaradation_state),
                )
            elif high_current >= battery_nominal_max_current * current_allowance_gain:
                battery_shock_current_state_new = max(
                    0.0,
                    battery_shock_current_state
                    - battery_nominal_max_current_damage
                    * battery_degeradation_decay
                    / (0.001 + battery_health_degaradation_state),
                )
            else:
                battery_shock_current_state_new = battery_shock_current_state
            return battery_shock_current_state_new

    return battery_shocked
