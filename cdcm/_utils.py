"""Some utility functions that do not fit anywhere else.

Author:
    Ilias Bilionis
    Murali Krishnan R

Date:
    3/13/2022
    3/18/2022

"""


import numpy as np
import numpy.typing as npt
from typing import Union


__all__ = ["TEXT_TRIMMING_SIZE", "trim_str", "clip"]



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


def clip(value: Union[int, float, npt.NDArray], 
         min_value: Union[int, float]=None, 
         max_value: Union[int, float]=None):
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
    assert not (min_value is None and max_value is None), \
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

