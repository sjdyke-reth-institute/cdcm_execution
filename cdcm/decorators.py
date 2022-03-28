"""Some decorators to simplify making systems.

Author:
    Ilias Bilionis

Date:
    3/27/2022

"""


__all__ = ["make_system"]


from collections.abc import Sequence
import inspect
from . import System, StateVariable, Parameter


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


def make_system(trans_func):
    """Make a system directly from a function.

    See below for an example.
    """
    kwargs = get_default_args(trans_func)
    # Find all states and parameters
    state = {}
    parameters = {}
    parents = {}
    for k, v in kwargs.items():
        if isinstance(v, StateVariable):
            state.update({k: v})
        elif isinstance(v, Parameter):
            parameters.update({k: v})
        elif isinstance(v, tuple):
            parents.update({k: v})
        elif v is None:
            # assuming this is a parent that hasn't been defined yet
            pass
        else:
            raise TypeError(f"I cannot understand keyword type {type(v)}")

    def new_trans_func(*args, **kwargs):
        new_x = trans_func(*args, **kwargs)
        if not isinstance(new_x, Sequence):
            new_x = (new_x, )
        return {
            s: v
            for s, v in zip(state, new_x)
        }

    return System(
        name=trans_func.__name__,
        state=state,
        parameters=parameters,
        parents=parents,
        description=trans_func.__doc__,
        transition_func=new_trans_func
    )
