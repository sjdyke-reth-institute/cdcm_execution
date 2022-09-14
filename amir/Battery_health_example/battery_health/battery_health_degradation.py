"""
Author: Amir Behjat

Date:
    7/12/2022


A battery_degeradation model.

variable :: TypeOfVariable

(variable) = optional variable

                                          _______________________________
battery_specs        :: BatterySpecs  => |                                |
                                         |                                |
                                         | battery_health_degaradationEnv | ->  battery_degeradation_health :: State
clock               :: Clock          => |                                |
                                          ________________________________

"""
import math

from cdcm import *
import numpy as np


__all__ = ["make_battery_health_degaradation_env_linear",
           "make_battery_health_degaradation_env_exponential_decay",
           "make_battery_health_degaradation_env_matrix_probability"]


def make_battery_health_degaradation_env_linear(clock,
                                                battery_specs):
    with System(name="battery_degerade",
                description="The battery_degerade environment") as battery_degerade:

        battery_degeradation_state = State(
            name="battery_degeradation_state",
            value=1.0,
            units="",
            description="State of Battery Degradatio; 1: Healthiest. 0: Dead Battery")
        battery_nominal_life = Parameter(
            name="battery_nominal_life",
            value=5.0 * 365 * 24 *3600,
            units="sec",
            description="Battery life for normal to low useage; 5 years")

        @make_function(battery_degeradation_state)
        def f_battery_degeradation_state(battery_degeradation_state=battery_degeradation_state,
                                         dt=clock.dt,
                                         battery_nominal_life=battery_nominal_life):
            """Transition function for battery_degeradation_state"""

            battery_degeradation_state_new = max(min(1.0, battery_degeradation_state - (dt / battery_nominal_life), 0.0))
            return battery_degeradation_state_new

    return battery_degerade

def make_battery_health_degaradation_env_exponential_decay(clock,
                                                           battery_specs):
    with System(name="battery_degerade",
                description="The battery_degerade environment") as battery_degerade:

        battery_half_life = Parameter(
            name="battery_nominal_life",
            value=2.5 * 365 * 24 * 3600,
            units="sec",
            description="Time it takes for the battry to reach 50% of its life; 2.5 year")

        battery_degeradation_state = State(
            name="battery_degeradation_state",
            value=1.0,
            units="",
            description="State of Battery Degradatio; 1: Healthiest. 0: Dead Battery")


        @make_function(battery_degeradation_state)
        def f_battery_degeradation_state(battery_degeradation_state=battery_degeradation_state,
                                         t=clock.t,
                                         battery_half_life =battery_half_life):
            """Transition function for battery_degeradation_state"""
            battery_degeradation_state_new = 1.0 * math.pow(2, -(t/battery_half_life))
            return battery_degeradation_state_new

    return battery_degerade

def make_battery_health_degaradation_env_matrix_probability(clock,
                                                            battery_specs):
    with System(name="battery_degerade",
                description="The battery_degerade environment") as battery_degerade:

        probability_matrix = Parameter(
            name="battery_nominal_life",
            value=np.array([[0.999726, 0.000243, 0.000031, 0.000000, 0.000000],
                            [0.000000, 0.999726, 0.000243, 0.000031, 0.000000],
                            [0.000000, 0.000000, 0.999726, 0.000243, 0.000031],
                            [0.000000, 0.000000, 0.000000, 0.999726, 0.000274],
                            [0.000000, 0.000000, 0.000000, 0.000000, 1.000000]]),
            units="",
            description="TProbability for degaration in each year based on "
                        "https://www.emerald.com/insight/content/doi/10.1108/IJQRM-06-2017-0116/full/pdf?title=degradation-modelling-and-life-expectancy-using-markov-chain-model-for-carriageway")

        battery_degeradation_state = State(
            name="battery_degeradation_state",
            value=1.00,
            units="",
            description="State of Battery Degradatio; 1.00: Healthiest; 0.75: Good; 0.50: functional; 0.25 low performance; 0.00: Dead Battery")


        @make_function(battery_degeradation_state)
        def f_battery_degeradation_state(battery_degeradation_state=battery_degeradation_state,
                                         probability_matrix=probability_matrix):
            """Transition function for battery_degeradation_state"""

            if battery_degeradation_state == 1.00:
                row = 0
            elif battery_degeradation_state == 0.75:
                row = 1
            elif battery_degeradation_state == 0.50:
                row = 2
            elif battery_degeradation_state == 0.25:
                row = 3
            elif battery_degeradation_state == 0.00:
                row = 4

            r = np.random.random()
            if r <= np.sum(probability_matrix[row, 0:0]):
                battery_degeradation_state = 1.00
            elif r <= np.sum(probability_matrix[row, 0:1]):
                battery_degeradation_state = 0.75
            elif r <= np.sum(probability_matrix[row, 0:2]):
                battery_degeradation_state = 0.50
            elif r <= np.sum(probability_matrix[row, 0:3]):
                battery_degeradation_state = 0.25
            elif r <= np.sum(probability_matrix[row, 0:4]):
                battery_degeradation_state = 0.00

            return battery_degeradation_state_new

    return battery_degerade