"""A clean version of a state variable.

Author:
    Ilias Bilionis

Date:
    4/7/2022

"""


__all__ = ["State"]


from . import Variable
from copy import deepcopy


class State(Variable):
    """A class representing a system state variable.
    
    This is a `Variable` that is changing in discrete steps.
    It stores two versions of its value.
    The current value is in `State.value`.
    The next value is in `State.next_value`.
    A call to `State._transition()` swaps `next_value` and `value`.

    See `Quantity` for the keyword arguments.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._next_value = deepcopy(self._value)

    def transition(self):
        """Writes `value` on `next_value`.

        Precondition:
        The `_next_value` has already been set.
        """
        self._next_value, self.value = self._value, self._next_value
        #self.tell_my_children_I_have_changed()