"""Abstraction of a component level system element

Author:
    R Murali Krishnan
    
Date:
    10.02.2023
    
"""


from cdcm import System, Function
from numbers import Number
from typing import Callable, Union
from functools import partial

from .._types import (ToolSequence, 
                      ConsumableSequence, 
                      NumOrVar,
                      HealthVars)
from ..common import *



class Component(System):
    """A class that defines a component system
    
    Attributes:
    ----------
    name:   str
        Name of the component
    nominal_health  : Number
        Nominal health value of the component
    nominal_age     : Number
        Nominal age value of the component
    nominal_functionality   : Number
        Nominal functionality value of the component

    More details in the documentation of `cdcm.System` object
    """

    def __init__(self, 
                 name: str, 
                 nominal_health: Number, 
                 nominal_age: Number,
                 nominal_functionality: Number,
                 tools_to_repair: ToolSequence = (),
                 consumables_to_repair: ConsumableSequence = (),
                 tools_to_replace: ToolSequence = (),
                 consumables_to_replace: ConsumableSequence = (),
                 **kwargs):
        self.nominal_health = nominal_health
        self.nominal_age = nominal_age
        self.nominal_functionality = nominal_functionality
        self.tools_to_repair = tools_to_repair
        self.consumables_to_repair = consumables_to_repair
        self.tools_to_replace = tools_to_replace
        self.consumables_to_replace = consumables_to_replace
        super().__init__(name=name, **kwargs)


def make_component(name: str,
                   *,
                   clock: System=None,
                   nominal_health: Number=1.0,
                   health_damage_rate: NumOrVar = None,
                   health_state_func: Callable=linear_function(),
                   nominal_age: NumOrVar=1.0,
                   aging_rate: NumOrVar=None,
                   aging_func: Callable=linear_function(),
                   nominal_functionality: Number=1.0,
                   **kwargs) -> Component:
    """Constructor procedure for a component system

    A component system has a functionality that depends on its health.

    If the component is constructed with a `health_damage_rate`, and 
    a `health_state_func`, the procedure infers that the component
    has a `HealthState`, whose temporal evolution is described
    by the `health_state_func` which takes as its parents `clock.dt`,
    and `health_damage_rate`. Else, it is instantiated with a 
    `HealthVariable`.

    The componend can be additionally constructed with a aging mechanism,
    if it is passed a `aging_rate` and a `aging_func`.

    The functionality of the component is constructed by a `product` 
    function. 

    Arguments:
    ---------- 
    name                :   str
        Name of the component system
    clock               :   cdcm.clock
        A clock system required to define time-dependent health state
        transitions of a component
    nominal_health      : Number (default = 1.0)
        Nominal health value of the component
    health_damage_rate  : Union[Number, cdcm.Variable] (default=None)
        Damage rate of the health variable of the component
    health_state_func   : Callable (default = `linear_function`)
        A transition function that models the temporal evolution
        of the health state of the component. It takes in any function
        with the following signature
            `f(state, dt, rate, *args, **kwargs)`
        For the `linear_function`, it returns the following procedure
            ```
            def f(state, dt, rate):
                return state - dt * rate
            ```
    nominal_age     : Number (default = 1.0)
        Nominal age of the component
    aging_rate      : Union[Number, cdcm.Variable] (default=None)
        Aging rate of the age state of the component
    aging_func      : Callable (default = `linear_function`)
        A transition function that models the temporal evolution
        of the aging health state of the component.
        It takes in any function with the following signature
            `f(age, dt, aging_rate, *args, **kwargs)`
        For the `linear_function`, it returns the following procedure
            ```
            def f(age, dt, aging_rate):
                return age - dt * aging_rate
            ```
    nominal_functionality:  Number (default = 1.0)
        Nominal functionality variable of the component

    Return:
        A `Component` system with a functionality dependent on a health variable,
        possibly aging too.
    """

    component = Component(name=name,
                          nominal_health=nominal_health,
                          nominal_age=nominal_age,
                          nominal_functionality=nominal_functionality,
                          **kwargs
                        )
    with component:
        health = make_health_mechanism(clock, health_damage_rate, health_state_func, nominal_health)
        if aging_func and aging_rate:
            age = make_aging_mechanism(clock, aging_rate, aging_func, nominal_age)
        else:
            age = None
        # Construcing functionality for the component
        parents = (health,) if age is None else (health, age,)
        functionality = make_functionality(*parents, 
                                           nominal_functionality=nominal_functionality)

    return component


def make_maintainable_component(name: str,
                                *,
                                tools_to_repair: ToolSequence = (),
                                consumables_to_repair: ConsumableSequence = (),
                                tools_to_replace: ToolSequence = (),
                                consumables_to_replace: ConsumableSequence = (),
                                **kwargs) -> Component:
    """Construct a maintainable component"""

    # Checks for arguments required to define a `maintainable component`

    maintainable_component = make_component(name, 
                                            tools_to_repair=tools_to_repair,
                                            consumables_to_repair=consumables_to_repair,
                                            tools_to_replace=tools_to_replace,
                                            consumables_to_replace=consumables_to_replace,
                                            **kwargs)
    return maintainable_component


def make_health_mechanism(clock, health_damage_rate, transition_func, nominal, name: str="health") -> HealthVars:
    """Make a health transition mechanism""" 

    assert isinstance(nominal, Number)
    if health_damage_rate is None:
        # This is a pure Variable, depending on type(nominal)
        cls = ContinuousHealthVariable if isinstance(nominal, float) else BinaryHealthVariable
        return cls(name=name, value=nominal, descriptipn="Health variable")
    else:
        return make_continuous_state_mechanism(clock, health_damage_rate, transition_func, nominal, name)
    # need a constructor for `BinaryHealthState` with a transition_function


make_aging_mechanism = partial(make_continuous_state_mechanism, name="age")


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