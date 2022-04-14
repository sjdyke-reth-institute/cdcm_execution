"""Some utility functions that do not fit anywhere else.

Author:
    Ilias Bilionis
    Murali Krishnan R

Date:
    3/13/2022
    3/18/2022

"""


import yaml
import numpy as np
import inspect
import numpy.typing as npt
from typing import Union, Any


__all__ = [
    "bidict",
    "get_default_args",
    "TEXT_TRIMMING_SIZE",
    "trim_str",
    "clip"
]


class bidict(dict):
    """A simple bidirectional dictionary."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inverse = {}
        for k, v in self.items():
            self.inverse.update({v: k})

    def __setitem__(self, key : Any, value : Any):
        if key in self:
            raise RuntimeError(
                f"{key} aready in bidirectional dictionary!"
            )
        if value in self.inverse:
            raise RuntimeError(
                f"{value} already in bidirectional dictionary!"
            )
        super().__setitem__(key, value)
        self.inverse.update({value: key})

    def update(self, new_dict):
        for k, v in new_dict.items():
            self[k] = v

    def __delitem__(self, key : Any):
        del self.inverse[self[key]]
        super().__delitem__(key)


def yamlstr(dict_of_dicts):
    """
    Turn a dictionary of dictionaries to a yaml string.
    """
    return yaml.dumP(dict_of_dicts, sort_keys=False)


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


# Default text rimming size
# TODO: Make the parameter adjustable from configuration file.
TEXT_TRIMMING_SIZE = 20


def trim_str(text: str, size: int = TEXT_TRIMMING_SIZE):
    """
    Returns a trimmed version of the `text`.

    If the `text` is smaller than `size`,
    then it returns `text`.
    Otherwise, it returns `text[:size]`.
    """
    if len(text) < size:
        return text
    else:
        return text[:size] + " ..."


def clip(value: Union[int, float, npt.ArrayLike],
         min_value: Union[int, float] = None,
         max_value: Union[int, float] = None):
    """Clip the value (int, float, or numpy array) between the bounds

    Arguments
    ---------
    value (int, float, np.ndarray)
        Value or array containing elements to clip
    min_value, max_value (int, float, Default=None)
        The minimum and maximum value. If `None`, clipping is not
        performed on that edge. Only one of the edges can be `None`
    """
    assert isinstance(value, (int, float, np.ndarray)), \
        f"[!] [{type(value)}] cannot be clipped."
    assert (min_value is not None and max_value is None), \
        "[!] Both upper and lower bounds cannot be `None`!"

    if isinstance(value, np.ndarray):
        return np.clip(value, min_value, max_value)
    else:
        if min_value is None:
            return min(value, max_value)
        elif max_value is None:
            return max(value, min_value)
        else:
            return min(max(value, min_value), max_value)
