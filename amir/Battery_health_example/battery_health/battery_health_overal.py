"""
Author: Amir Behjat

Date:
    7/12/2022


A battery_overal model.

variable :: TypeOfVariable

(variable) = optional variable

                                          _______________________________
battery_specs        :: BatterySpecs  => |                                |
                                         |                                |
                                         | battery_health_overalEnv | ->  battery_overal_health :: State
clock                :: Cloc          => |                                |
                                          ________________________________

"""
import math

from cdcm import *
import numpy as np


__all__ = ["make_battery_health_overal_env_multipication",
           "make_battery_health_overal_env_min",
           "make_battery_health_overal_env_harmonic_mean"]

def make_battery_health_overal_env_multipication(battery_health_degaradation,
                                                 battery_health_shock):
    with System(name="battery_overal",
                description="The battery_overal environment") as battery_overal:

        battery_overal_state = State(
            name="battery_overal_state",
            value=1.0,
            units="",
            description="State of Battery overal; 1: Healthiest. 0: Dead Battery")

        @make_function(battery_overal_state)
        def f_battery_overal_state(battery_health_degaradation_state=battery_health_degaradation.battery_degeradation_state,
                                   battery_shock_current_state=battery_health_shock.battery_shock_current_state):
            """Transition function for battery_overal_state"""

            battery_overal_state_new = max(min(1.0, battery_health_degaradation_state * battery_shock_current_state, 0.0))
            return battery_overal_state_new

    return battery_overal

def make_battery_health_overal_env_min(battery_health_degaradation,
                                       battery_health_shock):
    with System(name="battery_overal",
                description="The battery_overal environment") as battery_overal:

        battery_overal_state = State(
            name="battery_overal_state",
            value=1.0,
            units="",
            description="State of Battery overal; 1: Healthiest. 0: Dead Battery")

        @make_function(battery_overal_state)
        def f_battery_overal_state(battery_health_degaradation_state=battery_health_degaradation.battery_degeradation_state,
                                   battery_shock_current_state=battery_health_shock.battery_shock_current_state):
            """Transition function for battery_overal_state"""
            battery_overal_state_new = max(min(1.0, min(battery_health_degaradation_state, battery_shock_current_state)), 0.0)
            return battery_overal_state_new

    return battery_overal

def make_battery_health_overal_env_harmonic_mean(battery_health_degaradation,
                                                 battery_health_shock):
    with System(name="battery_overal",
                description="The battery_overal environment") as battery_overal:

        battery_overal_state = State(
            name="battery_overal_state",
            value=1.0,
            units="",
            description="State of Battery overal; 1: Healthiest. 0: Dead Battery")

        @make_function(battery_overal_state)
        def f_battery_overal_state(battery_health_degaradation_state=battery_health_degaradation.battery_degeradation_state,
                                   battery_shock_current_state=battery_health_shock.battery_shock_current_state):
            """Transition function for battery_overal_state"""
            if battery_health_degaradation_state * battery_shock_current_state > 0:
                battery_overal_state_new = max(min(1.0, 2 / (1 / battery_health_degaradation_state + 1 / battery_shock_current_state)), 0.0)
            else:
                battery_overal_state_new = 0.0
            return battery_overal_state_new

    return battery_overal