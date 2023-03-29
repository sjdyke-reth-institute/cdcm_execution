"""An agents_task_delivary model.

variable :: TypeOfVariable

(variable) = optional variable

                              ___________________________
agents         :: Agents  => |                           |
                             |  agents_task_delivaryEnv  |  -> clean_panel   :: State
                             |                           |  -> clean_plant   :: State
                             |___________________________|  -> repair_struct :: State[array]


"""

from cdcm import *

__all__ = ["make_agents_task_delivary_env_0"]


def make_agents_task_delivary_env_0(agents):
    with System(
        name="agents_task_delivary", description="The agents_task_delivary environment"
    ) as agents_task_delivary:
        clean_panel = State(
            name="_agent_clean_panel",
            units="",
            value=0.0,
            description="Cleaning the panel value in one time step",
        )
        clean_plant = State(
            name="_agent_clean_panel",
            units="",
            value=0.0,
            description="Cleaning the plant value in one time step",
        )
        repair_struct = State(
            name="_agent_repair_struct",
            units="",
            value=[0.0, 0.0, 0.0, 0.0, 0.0],
            description="The array of how much repair is given to each dome section in unit of time step",
        )

        @make_function(clean_panel, clean_plant, repair_struct)
        def f_task_delivary(agents=agents):
            """Transition function for agents energy consumption"""
            clean_panel_new = 0.0
            clean_plant_new = 0.0
            repair_struct_new = [0.0, 0.0, 0.0, 0.0, 0.0]
            return clean_panel_new, clean_plant_new, repair_struct_new

    return agents_task_delivary
