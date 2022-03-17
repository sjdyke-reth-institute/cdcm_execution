"""Defines a power dependent system

Author:
    Murali Krishnan R

Date:
    3/16/2022
"""

__all__ = ["BatterySystem"]

from . import SystemFromFunction
from . import Parameter, StateVariable, PhysicalStateVariable, \
              HealthStateVariable


class BatterySystem(SystemFromFunction):
    """A battery system made out of a function

    """

    def __init__(self, name="BatterySystem", state={}, parameters={}, parents={}, transition_func=None,
                 description=None, test_func=False, default_dt=1e-3):
        super().__init__(name=name, state=state, parameters=parameters, parents=parents, 
                         transition_func=transition_func, description=description)
        pass