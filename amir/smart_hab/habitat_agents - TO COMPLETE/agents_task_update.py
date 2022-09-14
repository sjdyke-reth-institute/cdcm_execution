"""An agents_task_update model.

variable :: TypeOfVariable

(variable) = optional variable

                              ___________________________
(agents_command)   :: HM  => |                           |
                             |   agents_task_updateEnv   |  -> agents_task_update :: State
                             |                           |
                             |___________________________|


"""

__all__ = ["make_agents_task_update_env_0"]



from cdcm import *

def make_agents_task_update_env_0(agent):
    with System(name="agents_task_update", description="The agents_task_update environment") as agents_task_update:

        agents = State(name="agents",
                       value=[],
                       units="",
                       description="Agents status")
        @make_function(agents)
        def f_task_update():
            """Transition function for agents energy consumption"""
            agents_new = agents
            return agents_new
    return agents_task_update
