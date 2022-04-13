"""A transition function.

Author:
    Ilias Bilionis

Date:
    4/12/2022

"""


__all__ = ["TransitionFunction"]


from . import Node
from typing import Any, Dict, Callable, Sequence


class TransitionFunction(Node):
    """A class representing a transition function.

    Keyword Arguments
    transition_func -- A function that tells us how to calculate the new
                       state from the current state. The transition
                       function must be as follows:
                       ```
                       def transition_func(*, parent1, parent2, ...):
                           # Do the calculations
                           # Make a return a new_state dictionary for the form:
                           children_vals = {
                                child1: value1,
                                child2: value2,
                            }
                           return children_vals
                       ```
                       Notice the "*" in the function definition. It is
                       essential. Do not skip it!

    For the rest of the keyword arguments see `Node`.
    """

    def __init__(
        self,
        *,
        transition_func : Callable,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._transition_func = transition_func

    @property
    def transition_func(self):
        """Get the transition function."""
        return self._transition_func


    def to_yaml(self) -> Dict[str, Any]:
        """Turn the object to a dictionary of dictionaries."""
        res = super().to_yaml()
        dres = res[self.name]
        dres["transition_func"] = self.transition_func
        return res

    def __call__(self):
        """Evaluates the next values of the children."""
        result = self.transition_func(
            **{
                name: obj.value
                for name, obj in self.parents.items()
            }
        )
        if not isinstance(result, Sequence):
            result = (result, )
        for new_value, child in zip(result, self.children.values()):
            child._next_value = new_value
