"""A transition function.

Author:
    Ilias Bilionis

Date:
    4/12/2022

"""


def get_default_args(func):
    """Return a dictionary containing the default arguments of a
    function.

    I took this from here:
    https://stackoverflow.com/questions/12627118/get-a-function-arguments-default-value
    """
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


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
        transition_func : Callable,
        **kwargs
    ):
        self._transition_func = transition_func

    def __call__(self):
        """Evaluates the next """
        pass
