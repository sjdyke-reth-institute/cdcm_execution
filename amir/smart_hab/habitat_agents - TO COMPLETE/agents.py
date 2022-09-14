"""
Defines the agent interface/type/system/concept.

A `agentEnvironment` is `System` that exposes the following interface:


variable :: TypeOfVariable

(variable) = optional variable

                              ___________________________
(agents_command)   :: HM  => |                           |
                             |   agents_task_updateEnv   |  -> clean_panel   :: State
                             |                           |  -> clean_plant   :: State
                             |___________________________|  -> repair_struct :: State[array]

"""

from cdcm import *
from . import make_agents_task_update_env_0
from . import make_agents_task_delivary_env_0

from dome_design import *

import math

__all__ = ["make_agent"]


def make_agent(agents_command = None,
               make_agents_task_update_env=make_agents_task_update_env_0,
               make_agents_task_delivary_env=make_agents_task_delivary_env_0
              ):
    """
    Make an agent system.

    Arguments

    """
    with System(name="agent",
                description="The agent system") as agent:

        agent_task_update = make_agents_task_update_env()
        agent_task_delivary = make_agents_task_delivary_env()

    return agent

