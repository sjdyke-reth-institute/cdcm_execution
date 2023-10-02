"""Constructors for State type nodes for functionality models

Author:
    R Murali Krishnan
    
Date:
    10.02.2023
    
"""


from cdcm import Variable, State, Parameter, Transition
from numbers import Number


class HealthState(State):
    """A class representing a health state variable"""
    pass


class BinaryHealthState(HealthState):
    """A class representing a Binary health state variable

    This is a `HealthState` variable which takes binary values {0, 1}.
    """
    pass


class ContinuousHealthState(HealthState):
    """A class representing a continuous health state variable

    This is a `HealthState` variable which takes real number values.

    See `State` in the CDCM execution language for the keyword arguments
    """
    def __init__(self, *args, value, **kwargs) -> None:
        self.nominal_value = value
        super().__init__(*args, value=self.nominal_value, **kwargs)


def make_continuous_state_mechanism(clock, rate, func, nominal_value, name) -> HealthState:
    """Make a continuous state mechanism"""

    assert clock is not None and \
            callable(func) and \
            isinstance(rate, (Number, Variable))

    if isinstance(rate, Number):
        if isinstance(nominal_value, float):
            rate = Parameter(name=name + "_rate", value=rate)
            statecls = ContinuousHealthState
        elif isinstance(nominal_value, int):
            raise TypeError("I can't support creation of binary health `State` variables yet..")
    else:
        statecls = ContinuousHealthState

    state = statecls(name=name, value=float(nominal_value))
    func = Transition(
        name=name + "_state_transition_func",
        parents=(state, clock.dt, rate),
        children=state,
        func=func,
        description="Transition function of the continuous health state"
    )
    return state 