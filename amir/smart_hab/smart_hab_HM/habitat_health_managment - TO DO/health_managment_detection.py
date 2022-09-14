"""An HM_detection model.


variable :: TypeOfVariable

(variable) = optional variable

                                          _________________
moon          :: Moon                 => |                 |
energy        :: Energy               => |                 |
eclss         :: Eclss                => |                 |
struct        :: Struct               => |                 |
interior_env  :: InteriorEnv          => | HM_detectionEnv | -> fault_list             :: State[array]
agents        :: Agents               => |                 |
clock         :: Clock                => |                 |
design        :: DomeSpec             => |_________________|


"""


__all__ = ["make_HM_detection_env_0"]

import math

from cdcm import *


def make_HM_detection_env_0(
    clock, dome_specs, moon, energy, eclss, struct, interior_env, agents
):
    with System(
        name="HM_detection", description="The HM_detection environment"
    ) as HM_detection:
        fault_limit = Parameter(
            name="fault_limit",
            value={
                "error_1": {
                    "name_state": "structure_secs",
                    "name_system": struct,
                    "min_acceptable_value": 0.95,
                    "max_acceptable_value": math.inf,
                    "current_value": 1.00,
                    "time_to_failure": 100,
                    "cyber_physical": "Physical",
                },
                "error_2": {
                    "name_state": "accum_dust_solar",
                    "name_system": energy,
                    "min_acceptable_value": 0.90,
                    "max_acceptable_value": math.inf,
                    "current_value": 1.00,
                    "time_to_failure": 100,
                    "cyber_physical": "Physical",
                },
                "error_3": {
                    "name_state": "accum_dust_nuclear",
                    "name_system": energy,
                    "min_acceptable_value": 0.90,
                    "max_acceptable_value": math.inf,
                    "current_value": 1.00,
                    "time_to_failure": 100,
                    "cyber_physical": "Physical",
                },
                "error_4": {
                    "name_state": "int_env_temp",
                    "name_system": interior_env,
                    "min_acceptable_value": 270.0,
                    "max_acceptable_value": 310.0,
                    "current_value": 300.00,
                    "time_to_failure": 100,
                    "cyber_physical": "Cyber",
                },
                "error_4": {
                    "name_state": "int_env_pres",
                    "name_system": interior_env,
                    "min_acceptable_value": 0.80,
                    "max_acceptable_value": 1.03,
                    "current_value": 0.00,
                    "time_to_failure": 100,
                    "cyber_physical": "Cyber",
                },
            },
            units="",
            description="list of parameters and their limits for a fault to occur",
        )

        fault_list = State(
            name="energy_cons",
            value=[],
            units="J",
            description="list of faults needed to be addressed by the ",
        )

        @make_function(fault_list)
        def f_detection(
            clock=clock,
            dome_specs=dome_specs,
            moon=moon,
            energy=energy,
            eclss=eclss,
            struct=struct,
            interior_env=interior_env,
            agents=agents,
            fault_limit=fault_limit,
        ):
            """Transition function for HM fault detection"""
            fault_list_new = []
            for key in fault_limit.keys():
                state_name = fault_limit[key]["name_state"]
                fault_limit[key]["name_system"].current_value = fault_limit[key][
                    "name_system"
                ].state_name.value
                if (
                    fault_limit[key]["min_acceptable_value"]
                    > fault_limit[key]["name_system"].current_value
                ):
                    fault_list_new.append(fault_limit[key]["name_system"].state_name)
                elif (
                    fault_limit[key]["max_acceptable_value"]
                    < fault_limit[key]["name_system"].current_value
                ):
                    fault_list_new.append(fault_limit[key])
            return fault_list_new

    return HM_detection
