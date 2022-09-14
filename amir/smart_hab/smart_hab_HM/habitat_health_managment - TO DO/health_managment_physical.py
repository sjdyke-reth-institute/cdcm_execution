"""An HM_physical model.

variable :: TypeOfVariable

(variable) = optional variable


                                                                      _________________
moon                               :: Moon                        => |                 |
energy                             :: Energy                      => |                 |
eclss                              :: Eclss                       => |                 | -> agents-clean_panel :: State
struct                             :: Struct                      => |                 |
interior_env                       :: InteriorEnv                 => |  HM_physicalEnv | -> agents-clean_nuclear :: State
agents                             :: Agents                      => |                 |
health_managment_detection         :: Health_managment_detection  => |                 |
clock                              :: Clock                       => |                 | -> agents-repair_dome :: State
design                             :: DomeSpec                    => |_________________|


"""

__all__ = ["make_HM_physical_env_0"]


from cdcm import *
import numpy as np


def make_HM_physical_env_0(
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
        name="HM_physical", description="The HM_physical environment"
    ) as HM_physical:
        # clean_panel = Variable(name="clean_panel",
        #                        value=False,
        #                        units="",
        #                        description="The command to clean the panel")
        # clean_plant = Variable(name="clean_plant",
        #                        value=False,
        #                        units="",
        #                        description="The command to clean the plant")
        # repair_struct = Variable(name="repair_struct",
        #                          value=False,
        #                          units="",
        #                          description="The command to repair the dome")
        agents_command = Variable(
            name="agents_command",
            value=False,
            units="",
            description="The model of agents in HM mind",
        )

        @make_function(agents_command)
        def f_physical(
            clock=clock,
            dome_specs=dome_specs,
            moon=moon,
            energy=energy,
            eclss=eclss,
            struct=struct,
            interior_env=interior_env,
            agents=agents,
            health_managment_detection=health_managment_detection,
        ):
            """Transition function for HM physical"""
            list_time_to_failures = []
            retask = True
            while retask:
                for fault in health_managment_detection:
                    list_time_to_failures.append(
                        health_managment_detection.time_to_failure
                    )
                idx_list = np.argsort(list_time_to_failures)
                retask = False
                for idx in idx_list:
                    if not (retask):
                        for agent in agents:
                            if (
                                agent.available
                                or health_managment_detection[idx].time_to_failure
                                < agent.task_at_hand.time_to_failure
                            ):
                                agent.available = False
                                health_managment_detection.append(agent.task_at_hand)
                                agent.task_at_hand = health_managment_detection[idx]
                                health_managment_detection.pop(idx)
                                retask = True
                                break

            agents_command = agents
            return agents_command
