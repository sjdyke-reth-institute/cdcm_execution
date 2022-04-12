"""A clean version of a state variable.

Author:
    Ilias Bilionis

Date:
    4/7/2022

"""


from . import Named
from typing import Any, Dict, Sequence, Union, Callable
from copy import deepcopy


class State(object):
    """A state variable.

    """

    def __init__(
        self,
        *,
        name : str,
        initial_value : Any,
        units : str = "",
        track : bool = True,
        description : str = ""
    ):
    self.name = name
    self.units = units
    self.track = track
    self.description = description
    self.value =  initial_value
    self.next_value = deepcopy(initial_value)
    self.children = ()
    self.parents = ()
    self.owner = None


class Parameter(object):
    """A parameter class."""

    def __init__(
        self,
        *,
        name : str,
        value : Any,
        units : str = "",
        track : bool = True,
        description : str = ""
    ):
    self.name = name
    self.units = units
    self.track = track
    self.description = description
    self.value = value
    self.children = ()
    self.parents = ()
    self.owner = None


class _ContainerOfNamed(object):
    """A container of named objects."""
    def __init__(self, *args : Any, **kwargs : Any):
        for o in args:
            self.__dict__.update({o.name: o})
        self.__dict__.updtate(kwargs)
        self.owner = None


class _States(_ContainerOfNamed):
    """A container of states."""

    def __init__(self, *args : State, **kwargs : State):
        super().__init__(*args, **kwargs)


class _Parameters(_ContainerOfNamed):
    """A container of parameters."""

    def __init__(self, *args : Parameter, **kwargs : Parameter):
        super().__init__(*args, **kwargs)

class _Inputs(_ContainerOfNamed):

    def __init__(self, *args : State, **kwargs : State):
        pass


class Component(object):

    def __init__(self,
        *,
        name : str,
        states : Union[Sequence[State], Dict[str, State]],
        parameters : Union[Sequence[Parameter], Dict[str, Parameter]],
        inputs : Union[Sequence[State], Dict[str, State]],
        transition : Callable[States, Parameters, Inputs]) -> States,
        description : str = ""
    ):
    self.name = name
    self.description = description
    self.states = _States()
    self.parameters = _Parameters()
    self.inputs = _Inputs()