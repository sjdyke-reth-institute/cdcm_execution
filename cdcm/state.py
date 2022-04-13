"""A clean version of a state variable.

Author:
    Ilias Bilionis

Date:
    4/7/2022

"""


__all__ = ["State"]


from . import Quantity
from copy import deepcopy


class State(Quantity):
    """A class representing a system state variable.
    
    This is a `Quantity` that is varying with time.
    It stores two versions of its value.
    The current value is in `Quantity.value`.
    The next value is in `Quantity.next_value`.
    A call to `Quantity.transition()` writes `next_value` on `value`.

    See `Quantity` for the keyword arguments.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._next_value = deepcopy(self.value)

    def _transition():
        """Writes `value` on `next_value`.

        Precondition:
        The `_next_value` has already been set.
        """
        self._next_value, self._value = self._value, self._next_value
