"""Common constructors used in the module

Author:
    Ilias Bilionis
    R Murali Krishnan
    
Date:
    09.18.2022
    10.04.2023

"""


__all__ = ["make_continuous_state_mechanism",
           "make_aging_mechanism",
           "make_health_mechanism",
           "make_functionality",
           "polynomial",
           "linear_function"]


from cdcm import *
from numbers import Number
from typing import Union, Callable
from functools import partial

from ._variables import *
from ._variable_patterns import product


def maybe_make_system(name_or_system: Union[str, System], clstype=System, **kwargs) -> System:
    """Returns either a new system with a given name or the system that is provided."""

    if isinstance(name_or_system, str):
        # I am making a new system
        sys = clstype(name=name_or_system, **kwargs)
    elif isinstance(name_or_system, System):
        # I am just adding variables to an existing system
        sys = name_or_system
    else:
        raise ValueError(f"I do not know what to do with {type(name_or_system)}!")
    return sys


def polynomial(order: int, _clip: bool=True, lval: Number=0.0, uval: Number=1.0):
    """A polynominal function"""
    def f(state, dt, rate, *args, **kwargs):
        rate_term = [rate ** i for i in range(1, order + 1)]
        new_state = state - dt * sum(rate_term)
        return clip(new_state, lval, uval) if _clip else new_state
    return f


# State transition function which is linear to rate
linear_function = partial(polynomial, order=1)


def make_continuous_state_mechanism(clock, rate, func, nominal_value, name, **kwargs) -> HealthState:
    """Make a continuous state mechanism"""

    assert clock is not None
    assert callable(func)
    assert isinstance(rate, (Number, Variable)), f"{type(rate)}"

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


make_aging_mechanism = partial(make_continuous_state_mechanism, name="age")


def make_health_mechanism(clock, health_damage_rate, transition_func, nominal, name: str="health", **kwargs) -> Union[HealthState, HealthVariable]:
    """Make a health transition mechanism""" 

    assert isinstance(nominal, Number)
    if health_damage_rate is None:
        # This is a pure Variable, depending on type(nominal)
        cls = ContinuousHealthVariable if isinstance(nominal, float) else BinaryHealthVariable
        return cls(name=name, value=nominal, descriptipn="Health variable")
    else:
        return make_continuous_state_mechanism(clock, health_damage_rate, transition_func, nominal, name, **kwargs)
    # need a constructor for `BinaryHealthState` with a transition_function


def make_functionality(
        *args,
        name: str="functionality",
        functionality_func: Callable=product,
        nominal_functionality: Number=1.0,
        **kwargs) -> Functionality:
    """A constructor for a `Functionality` variable"""

    functionality = Functionality(
        name=name,
        nominal_value=nominal_functionality,
        description="Functionality of the component"
    )

    if args:
        # Need to construct a functionality model
        assert callable(functionality_func)
        variables = []

        for arg in args:
            if isinstance(arg, System):
                assert hasattr(arg, "functionality"), \
                "[!] `System` instance does not have a functionality"
                variables.append(arg.functionality)
            elif isinstance(arg, Variable):
                variables.append(arg)
            else:
                raise TypeError("I need Variables to create a functionality")


        functionality_func = Function(
            name=name + "_function",
            parents=tuple(variables),
            children=functionality,
            func=functionality_func,
            description="A function that describes the functionality of the system"
    )
    return functionality