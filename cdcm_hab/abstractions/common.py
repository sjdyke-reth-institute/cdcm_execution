"""
Some functions that are commonly used.
"""


__all__ = ["maybe_make_system"]


from cdcm import System
from typing import Union


def maybe_make_system(name_or_system: Union[str, System], **kwargs):
    """Returns either a new system with a given name or the system that is provided."""
    if isinstance(name_or_system, str):
        # I am making a new system
        sys = System(name=name_or_system, **kwargs)
    elif isinstance(name_or_system, System):
        # I am just adding variables to an existing system
        sys = name_or_system
    else:
        raise ValueError(f"I do not know what to do with {type(name_or_system)}!")
    return sys
