"""A class representing a system of systems.

Author:
    Ilias Bilionis

Date:
    3/14/2022

"""


__all__ = ["System", "_dict_to_yaml"]


import yaml
from collections.abc import Sequence
from copy import deepcopy
from . import (NamedType,
               Parameter,
               StateVariable,
               PhysicalStateVariable,
               HealthStateVariable)


def _dict_to_yaml(data):
    """Turns a dictionary of objects to a dictionary of dictionaries."""
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
                   that are tuples of type `System` or of type
                   `(str, System)`. In any case, the keys correspond the
                   name of the input variable used locally by this
                   object. For the values the story is as follows. If
                   the value is just a `System` object, then we assume
                   that this object has a state with the same name as
                   the corresponding key. If the value is
                   `(str, System)`, then we assume that the first item
                   of the tupe is the name of the input variable in the
                   `System` object.

                   Here is an example:
                   ```
                   parents = {
                        "input_var_1": system_object_1,
                        "input_var_2": ("foo", system_object_2)
                   }
                   ```
                   This is a dictionary with two items. The first item
                   tells us that there is an input named `input_var_1`
                   which can be found in the object `system_object_1`.
                   That is, the variable can be accessed through
                   `system_object_1.state["input_var_1"]`.
                   The second item, tells us that there is another
                   input, which we name "input_var_2", that actually
                   corresponds to a state called "foo" in
                   `system_object_2`. It can be accessed through
                   `system_object_2.state["foo"]`.

                   Despite accepting both kinds of parents, the class
                   using the second type of specification to store
                   things locally because it is more general. So,
                   the first item becomes
                   `"input_var_1": ("input_var_1", system_object_1)`
                   in the internal representation.

                   Now when you inherit from this class, you can
                   access these input variables from the `get_parent()`
                   method by just providing the local name.
    sub_systems -- A dictionary of systems. The keys must be strings.
                   The values must be `System`. Alternatively, a list of
                   systems.
    description -- A description for the system.

    TODO: The names of the subsystems should be unique. Fix this.
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
        super().__init__(
            name=name,
            description=description
        )
        self.state = state
        self.parameters = parameters
        self.parents = parents
        self.sub_systems = sub_systems

    def has_state(self, state_name):
        """Return True if the system has a state called `state_name`."""
        return state_name in self.state.keys()

    def has_parameter(self, param_name):
        """Return True if the system has a parameter called
        `param_name`."""
        return param_name in self.parameters.keys()

    def _get_state_of_type(self, Type):
        """Return a dictionary with all state components of type
        `Type`."""
        res = {}
        for n, s in self.state.items():
            if isinstance(s, Type):
                res[n] = s
        return res

    def _add_type(self, local_name, obj, Type, out_dict):
        """Add a new `system` which is referred by `name`."""
        assert isinstance(local_name, str),\
            "The name must be a string."
        assert isinstance(obj, Type),\
            f"You must supply a {Type} object."
        new_item = {local_name: obj}
        out_dict.update(new_item)
        return new_item

    def _add_types(self, new_objs, Type, out_dict):
        """Add many subsystems from a dictionary or a list.

        Arguments:
        objs --     The objects to be added. Either a dictionary with
                    keys that are strings and values that are `Type` or
                    a `Sequence` of `Type`. In the latter case, we
                    assume that `Type` the objects are also `NamedType`,
                    i.e., they have a name attribute. If the do, the
                    name attribute is used as a key.
        Type     -- The type of the objects being added.
        out_dict -- The dictionary on which to add the objects.
        """
        if isinstance(new_objs, Type):
            new_objs = [new_objs]
        if isinstance(new_objs, Sequence):
            tmp = {}
            for obj in new_objs:
                assert isinstance(obj, NamedType),\
                    "The objects must be of `NamedType`."
                tmp.update({obj.name: obj})
            new_objs = tmp
        else:
            assert isinstance(new_objs, dict),\
                "You must supply a dictionary (or a list) of subsystems."
        for local_name, obj in new_objs.items():
            self._add_type(local_name, obj, Type, out_dict)
        return new_objs

    @property
    def parameters(self):
        """Return the parameters of the object."""
        return self._parameters

    @parameters.setter
    def parameters(self, new_parameters):
        """Set the parameters from a dictionary or a list."""
        self._parameters = {}
        self.add_parameters(new_parameters)

    def add_parameter(self, new_parameter):
        """Add a new parameter."""
        self._add_type(new_parameter, Parameter, self._parameters)

    def add_parameters(self, new_parameters):
        """Add new parameters from a dictionary or a list."""
        self._add_types(new_parameters, Parameter, self._parameters)

    @property
    def state(self):
        """Return the current state."""
        return self._current_state

    @state.setter
    def state(self, new_state):
        """Set the states.

        Be careful, it removes the old states.
        """
        self._current_state = {}
        self._next_state = {}
        self.add_states(new_state)

    def add_state(self, new_state):
        """Add a single new state variable."""
        new_item = self._add_type(
            new_state,
            StateVariable,
            self._current_state
        )
        self._next_state.update(deepcopy(new_item))
        return new_item

    def add_states(self, new_states):
        """Add many new states from a dictionary or a list."""
        new_items = self._add_types(
            new_states,
            StateVariable,
            self._current_state
        )
        self._next_state.update(deepcopy(new_items))
        return new_items

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

    @parents.setter
    def parents(self, new_parents):
        """Sets the parents from a dictionary.

        See the class docstring for the format of the `new_parents`
        dictionary.

        Be careful! This class replaces the current parents dictionary.
        Use the `add_parents_from_dict()` method if you want to add
        parents to the existing list from a dictionary.
        Use the `add_parent()` method if you want to add a single
        new parent.
        """
        self._parents = {}
        self.add_parents_from_dict(new_parents)

    def add_parents_from_dict(self, new_parents):
        """Adds more parents from a dictionary.

        See the class docstring for the format of the `new_parents`
        dictionary.
        """
        for local_name, value in new_parents.items():
            if not isinstance(value, tuple):
                value = (value,)
            assert len(value) <= 2,\
                "See the class docstring for details on the parents dict."
            self.add_parent(local_name, *value)

    def add_parent(self, local_name, system, remote_name=None):
        """Adds a new parent variable to the class.

        Arguments:
        local_name -- The name that is used locally for the input
                      variable. If `remote_name` is not specified,
                      then we assume that `remote_name == local_name`.
        system     -- The system from which to take the variable.

        Keyword Arguments:
        remote_name -- The name of the variable that is used in `styem`.
        """
        assert isinstance(local_name, str)
        assert isinstance(system, System)
        if remote_name is None:
            remote_name = local_name
        else:
            assert isinstance(remote_name, str)
        assert local_name not in self.parents.keys(),\
            f"The parents dictionary already includes a key `{local_name}`."
        self._parents.update({local_name: (remote_name, system)})

    def get_parent_state(self, local_name):
        """
        Get the current version of a parent state.
        """
        remote_name, system = self.parents[local_name]
        return system.state[remote_name]

    @property
    def sub_systems(self):
        """Return the subsystems."""
        return self._sub_systems

    @sub_systems.setter
    def sub_systems(self, new_sub_systems):
        """Set the subsystems of the system from a dictionary.

        Arguments:
        new_sub_systems -- A dictionary of systems. The keys must be
                           strings. The values must be `System`.
                           Alternatively, a list of systems.
        """
        self._sub_systems = {}
        self.add_subystems(new_sub_systems)

    def add_subystem(self, local_name, system):
        """Add a new `system` which is referred by `name`."""
        self._add_type(local_name, System, self._sub_systems)

    def add_subystems(self, sub_systems):
        """Add many subsystems from a dictionary."""
        self._add_types(sub_systems, System, self._sub_systems)

    def _calculate_my_next_state(self, dt):
        """Calculate the next sate of the system using the current one.

        **Note that this function should not update the subsystems.**

        Arguments:
        dt -- the time step to use when calculating the next state.

        The function assumes that `self._current_state` already contains
        the current state of the system and that access to all input
        variables is available through `self.parents`.

        This function should not return anything. It should just 
        calculate the next state and store the result in
        `self._next_state`.

        By default, this function does not do anything.

        The user has to implement it if the states of the system have
        dynamics.
        """
        pass

    def _calculate_next_state(self, dt):
        """Transitions the state of the system and of all sub
        systems."""
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
        for local_name, (remote_name, system) in self.parents.items():
            parents_dict[local_name] = {"remote_name": remote_name,
                                        "system_name": system.name}
        dres["parents"] = parents_dict
        dres["sub_systems"] = _dict_to_yaml(self.sub_systems)
        return res
