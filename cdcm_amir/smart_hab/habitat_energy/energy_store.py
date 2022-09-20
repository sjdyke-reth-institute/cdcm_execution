"""
Author: Amir Behjat

Date:
    7/08/2022

A Energy_ storing model.


variable :: TypeOfVariable

(variable) = optional variable

                                             ___________________________
energy_generation  :: Energy_generation  => |                           |
                                            |  Energy_stored_energyEnv  | ->  stored energy   :: State
(ecless_energy_cons)  :: ECLSS           => |                           |
                                             ___________________________


"""

from cdcm import *


__all__ = ["make_energy_store_env_0"]


def make_energy_store_env_0(energy_generate, ecless_energy_cons):
    with System(
        name="energy_store", description="The energy_store environment"
    ) as energy_store:
        battery_capacity_0 = 7200000.0

        battery_capacity = Parameter(
            name="battery_capacity",
            value=battery_capacity_0,
            units="J",
            description="battery capacity for saving energy",
        )
        available_en = State(
            name="available_en",
            value=battery_capacity_0,
            units="J",
            description="Current energy stored in batteries",
        )

        @make_function(available_en)
        def f_available_en(
            available_en=available_en,
            gen_energy_total=energy_generate.gen_energy_total,
            battery_capacity=battery_capacity,
            energy_cons=ecless_energy_cons,
        ):
            """Transition function for available_en"""
            available_en_new = min(
                max(0.0, available_en + gen_energy_total - energy_cons),
                battery_capacity,
            )
            return available_en_new

    return energy_store
