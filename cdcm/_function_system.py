"""A system put together from a simple function.

Author:
    Ilias Bilionis

Date:
    3/14/2022

TODO: Write me.

"""


__all__ = ['SystemFromFunction']


from . import System


class SystemFromFunction(System):
    """A system class made out of a function.

    Keyword argumets:
    name            -- A name for the system.
    state           -- The state of the system.
    parents         -- The parents of the system.
    transition_func -- A function that tells us how to calculate the new state
                       from the current state. The transition function must be
                       as follows:
                       ```
                       def transition_func(dt, *, state1, ...
                                           parent_var1, ..., 
                                           parameter_1, ...):
                           # Do the calculations
                           # Make a return a new_state dictionary for the form:
                           new_state = {'state_var1': value1,
                                        'state_var2': value2,
                                        ...}
                           return new_state
                       ```
                       Notice the "*" in the function definition. It is essential.
                       Do not skip it!
    description     -- A description for the object.
    """

    def __init__(self, name="SystemFromFunction", state={}, parameters={}, parents={}, transition_func=None,
                 description=None, test_func=False, default_dt=1e-3):
        super().__init__(name=name, state=state, parameters=parameters, parents=parents, 
                         description=description)
        assert callable(transition_func)
        self._transition_func = transition_func

    def _calculate_next_state(self, dt):
        inputs = {}
        for k, var in self.state.items():
            inputs[k] = var.value
        for k, var in self.parameters.items():
            inputs[k] = var.value 
        for k, var in self.parents.items():
            inputs[k] = var.state[k].value
        new_state = self._transition_func(dt, **inputs)
        for s, v in new_state.items():
            self._next_state[s].value = v
