"""Defines an abstract system class.


Author:
    Ilias Bilionis

Date:
    3/11/2022

"""


__all__ = ['System']


from abc import ABC, abstractmethod
from collections.abc import Sequence
from copy import deepcopy
from . import Parameter, StateVariable, PhysicalStateVariable, \
              HealthStateVariable


def _assert_and_make_dict(obj, NamedType):
    """Check if the `obj` is a dict and turn it into a dict if it is not.

    Arguments
    obj       -- Either an object of type `NamedType` or a Sequence of type 
                `NamedType` or a `dict` with keys that are strings and values 
                 that are of type `NamedType`.
    NamedType -- A type instances of which have an attribute called "name".

    Returns the a dictionary with keys that are strings made out of the name
    of the objects and values that are the objects.
    """
    if isinstance(obj, NamedType):
        obj = [obj]
    if isinstance(obj, Sequence):
        new_obj = {}
        for o in obj:
            assert (isinstance(o, NamedType), 
                f"{o} is not of type {NamedType}")
            assert (hasattr(o, "name"),
                f"{o} does not have an attribute called 'name'")
            new_obj.update({o.name: o})
        return new_obj
    assert (isinstance(obj, dict),
        f"{obj} is not must either be a NamedType, a Sequence[NamedType]" +
        " or a Dictionary[String, NamedType].")
    for o in obj.values():
        assert (isinstance(o, NamedType), 
            f"{o} is not of type {NamedType}")
    return obj


class System(ABC):
    """Describes an abstract System.

    A system has the following characteristics:
        - It has a name.
        - It has a description of what it does.
        - It knows its current_state.
        - It knows which variables from other systems may affect its transition.
        - It knows how to transition its state to the next timestep.

    All specific CDCM systems must inherit from this class.

    Keyword Arguments:
    name         -- A name for the system.
    state        -- A dictionary with keys that are strings corresponding to
                    the state variable names and values that are 
                    `StateVariable`. Alternatively, use a list. The class will
                    turn it into a dictionary using the name of the states.
    parameters   -- A dictionary with keys that are strings corresponding to
                    parameter names and values that are Parameter objects.
                    parameters of a system. A list is also possible.
    parents      -- A dictionary with keys that are strings corresponding
                    to the state variable names and values that are the
                    `System` from which this variable must be taken. A list is
                    also possible.
    description  -- A long description of the system.
    """

    def __init__(self, name="System", state={}, parameters={}, parents={}, description=None):
        # Sanity checks
        assert isinstance(name, str)
        assert description is None or isinstance(description, str)
        # Sanity check for state variables
        state = _assert_and_make_dict(state, StateVariable)
        parameters = _assert_and_make_dict(parameters, Parameter)
        # Sanity check for parameters
        assert isinstance(parameters, dict)
        for p in parameters.values():
            assert isinstance(p, Parameter)
        # Sanity check for parents
        assert isinstance(parents, dict)
        for k, v in parents.items():
            assert isinstance(k, str)
            assert isinstance(v, System)
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
        """Return True if the system has a state called `state_name`.
        """
        return state_name in self.state.keys()

    def has_paremeter(self, param_name):
        """Return True if the system has a parameter called `param_name`.
        """
        return param_name in self.parameters.keys()

    def get_state(self, state_name):
        """Get the state called `state_name`.
        """
        assert self.has_state(state_name)
        return self.state[state_name]

    def get_parameter(self, param_name):
        """Get the parameter called `param_name`.
        """
        assert self.has_parameter(param_name)
        return self.parameters[param_name]

    def _get_state_of_type(self, Type):
        """Return a dictionary with all state components of type `Type`.
        """
        res = {}
        for n, s in self.state.items():
            if isinstance(s, Type):
                res[n] = s
        return res

    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def parameters(self):
        return self._parameters

    @property
    def state(self):
        return self._current_state
    
    @property
    def physical_state(self):
        return self._get_state_of_type(PhysicalStateVariable)
    
    @property
    def health_state(self):
        return self._get_state_of_type(HealthStateVariable)

    @property
    def parents(self):
        return self._parents

    @property
    def time(self):
        return self._time
    
    def get_parent_state(self, name):
        """
        Get the current version of a parent state.
        """
        return self.parents[name].state[name]
    
    @abstractmethod
    def _calculate_next_state(self, dt):
        """Calculate the next sate of the system using the current one.

        Arguments:
        dt -- the time step to use when calculating the next state.

        The function assumes that `self._current_state` already contains
        the current state of the system and that access to all input
        variables is available through `self.parents`.

        This function should not return anything. It should just calculate
        the next state and store the result in `self._next_state`.
        """
        pass

    def _transition(self):
        """This function transitions to the next state.

        The function simply swaps the `self._current_state` with 
        `self._next_state`. It is essential for ensuring deterministic
        behavior.
        """
        self._current_state, self._next_state = self._next_state, self._current_state

    @property
    def can_transition(self):
        """
        Return True if the system can transition independently.
        """
        return not bool(self.parents)

    def step(self, dt):
        """Make the system step forward in time.

        Note that this only works if `self.can_transition` is True.
        If not, then it will raise an error.

        To avoid bugs, `self.can_transition` is calculated every time
        it is needed. This is in case the parents change.
        So, doing step may take a while.
        Use `unsafe_step()` if you are sure the system can transition.
        """
        if self.can_transition:
            self.unsafe_step(dt)
        else:
            raise RuntimeError("The system has parents and it cannot transition.")

    def unsafe_step(self, dt):
        """Step without checking if the system can transition.

        Be careful. This may lead to bugs.
        """
        self._calculate_next_state(dt)
        self._transition()

    def __str__(self):
        """Return a readable string representation of the class.

        TODO: Make this pretty.
        TODO: Add verbosity control.
        """
        res = f"""System name:    {self.name}
Physical state: {list(self.physical_state.keys())}
Health state:   {list(self.health_state.keys())}
Parameters:     {list(self.parameters.keys())}
Parents:        {list([p.name + "." + v for v, p in self.parents.items()])}"""
        return res

    def __repr__(self):
        """Return a complete string representation of the class.
        """
        # TODO: Write me
        return self.__str__()
