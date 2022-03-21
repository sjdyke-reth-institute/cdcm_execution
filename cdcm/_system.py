"""A class representing a system of systems.

Author:
    Ilias Bilionis

Date:
    3/14/2022

"""


__all__ = ["System", "_assert_and_make_dict", "_dict_to_yaml"]


import yaml
from collections.abc import Sequence
from copy import deepcopy
from . import (NamedType,
               Parameter,
               StateVariable,
               PhysicalStateVariable,
               HealthStateVariable)


def _assert_and_make_dict(obj, NamedType):
    """Check if the `obj` is a dict and turn it into a dict if it is not.

    Arguments
    obj       -- Either an object of type `NamedType` or a Sequence of type
                `NamedType` or a `dict` with keys that are strings and values
                 that are of type `NamedType`.
    NamedType -- A type instances of which have an attribute called "name".

    Returns a dictionary with keys that are strings made out of the name
    of the objects and values that are the objects.
    """
    if isinstance(obj, NamedType):
        obj = [obj]
    if isinstance(obj, Sequence):
        new_obj = {}
        for o in obj:
            assert isinstance(o, NamedType), \
                f"{o} is not of type {NamedType}"
            assert hasattr(o, "name"), \
                f"{o} does not have an attribute called 'name'"
            new_obj.update({o.name: o})
        return new_obj
    assert isinstance(obj, dict), \
        (f"{obj} is not must either be a NamedType, a Sequence[NamedType]"
         + " or a Dictionary[String, NamedType].")
    for o in obj.values():
        assert isinstance(o, NamedType), f"{o} is not of type {NamedType}"
    return obj


def _dict_to_yaml(data):
    """Turns a dictionary of object to a dictionary of dictionaries."""
    res = {}
    for k, v in data.items():
        res.update(v.to_yaml())
    return res


class System(NamedType):
    """A class representing a system of systems.

    Keyword Arguments
    name        -- A name for the system.
    state       -- The states of the system. A dictionary the keys of
                   which are strings and the values are 
                   `PhysicalStateVariable` or `HealthStateVariable`.
                   Alternatively, a list of `PhysicalStateVariables`
                   or `HealthStateVariables`.
    parameters  -- The parameters of the system. A dictionary the keys
                   of which are strings and the values are `Parameter`.
                   Alternatively, a list of `Parameter`.
    parents     -- A dictionary of keys which are strings and values
                   that are `System`. The keys correspond to inputs that
                   this system needs from the value `System` for
                   calculating the next state.
    sub_systems -- A dictionary of systems. The keys must be strings. 
                   The values must be `System`. Alternatively, a list of
                   systems.
    description -- A description for the system.
    """

    def __init__(
        self,
        name="system_of_systems",
        state={},
        parameters={},
        parents={},
        sub_systems={},
        description=""
    ):
        # Sanity check
        sub_systems = _assert_and_make_dict(sub_systems, System)
        self._sub_systems = sub_systems
        super().__init__(
            name=name,
            description=description
        )
        state = _assert_and_make_dict(state, StateVariable)
        parameters = _assert_and_make_dict(parameters, Parameter)
        assert isinstance(parameters, dict),\
            "The parameters must be a dictionary."
        for p in parameters.values():
            assert isinstance(p, Parameter),\
                f"The dictionary vaklue {p} is not a Parameter."
        assert isinstance(parents, dict),\
            "The parents must be a dictionary."
        for k, v in parents.items():
            assert isinstance(k, str),\
                "Each key in the parents dictionary must be a string."
            assert isinstance(v, System),\
                "Each value in the parents dictionary must be a System."
            assert v.has_state(k), \
                f'Parent {v.name} does not have a state named {k}'
        # Initialize variables
        self._name = name
        self._description = description
        self._current_state = state
        self._next_state = deepcopy(state)
        self._parameters = parameters
        self._parents = parents

    def has_state(self, state_name):
        """Return True if the system has a state called `state_name`."""
        return state_name in self.state.keys()

    def has_parameter(self, param_name):
        """Return True if the system has a parameter called `param_name`."""
        return param_name in self.parameters.keys()

    def _get_state_of_type(self, Type):
        """Return a dictionary with all state components of type `Type`."""
        res = {}
        for n, s in self.state.items():
            if isinstance(s, Type):
                res[n] = s
        return res

    @property
    def parameters(self):
        """Return the parameters of the object."""
        return self._parameters

    @property
    def state(self):
        """Return the current state."""
        return self._current_state

    @property
    def physical_state(self):
        """Return all physical states."""
        return self._get_state_of_type(PhysicalStateVariable)

    @property
    def health_state(self):
        """Return all health states."""
        return self._get_state_of_type(HealthStateVariable)

    @property
    def parents(self):
        """Return the parents of the object."""
        return self._parents

    def get_parent_state(self, name):
        """
        Get the current version of a parent state.
        """
        return self.parents[name].state[name]

    @property
    def sub_systems(self):
        """Return the subsystems."""
        return self._sub_systems

    def _calculate_my_next_state(self, dt):
        """Calculate the next sate of the system using the current one.

        **Note that this function should not update the subsystems.**

        Arguments:
        dt -- the time step to use when calculating the next state.

        The function assumes that `self._current_state` already contains
        the current state of the system and that access to all input
        variables is available through `self.parents`.

        This function should not return anything. It should just calculate
        the next state and store the result in `self._next_state`.

        By default, this function does not do anything.

        The user has to implement it if the states of the system have dynamics.
        """
        pass

    def _calculate_next_state(self, dt):
        """Transitions the state of the system and of all sub systems."""
        self._calculate_my_next_state(dt)
        for s in self.sub_systems.values():
            s._calculate_next_state(dt)

    def _transition(self):
        """This function transitions to the next state.

        The function simply swaps the `self._current_state` with
        `self._next_state`. It is essential for ensuring deterministic
        behavior.
        """
        self._current_state, self._next_state = (self._next_state,
                                                 self._current_state)

        for s in self.sub_systems.values():
            s._transition()

    def unsafe_step(self, dt):
        """Step without checking if the system can transition.

        Be careful. This may lead to bugs.
        """
        self._calculate_next_state(dt)
        self._transition()

    def __str__(self):
        """Return string representation of combined system."""
        return yaml.dump(self.to_yaml(), sort_keys=False)

    def to_yaml(self):
        """Turn the object to a dictionary of dictionaries."""
        res = super().to_yaml()
        dres = res[self.name]
        dres["physical_state"] = _dict_to_yaml(self.physical_state)
        dres["health_state"] = _dict_to_yaml(self.health_state)
        dres["parameters"] = _dict_to_yaml(self.parameters)
        parents_dict = {}
        for k, v in self.parents.items():
            parents_dict[k] = v.name
        dres["parents"] = parents_dict
        return res
        dres = res[self.name]
        dres["sub_systems"] = _dict_to_yaml(self.sub_systems)
        return res
