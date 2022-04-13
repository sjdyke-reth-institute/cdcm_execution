"""Defines a Quantify class.

Author:
    Ilias Bilionis
    Roman Ibrahimov

Date:
    3/10/2022
	4/7/2022
"""


__all__ = ["Quantity"]


import numpy as np
import pint
from typing import Any, Dict
from numbers import Number
from . import Node


ureg = pint.UnitRegistry()


class Quantity(Node):
    """Defines a CDCM quantity.

    The quantity knows its units. It has a decscription that explains
    what it is. It has a name. And it has a value.

    Arguments:

        value      -- The value of the quantity. Must be an int, a
                      double or a numpy array of ints or floating point
                      numbers. We also allow it to be a string.
                      Initially, no value is specified. We are not
                      going to check for the value of quantities.
                      But keep in mind that for saving them in files,
                      the type has to be constant through out the life
                      of the object.
        units      -- Must be a string or a pint object that describes
                      an SI physical unit. This is optional as some
                      quantities may not have units.
        track      -- A boolean. If True the quantity will be tracked
                      during simulations. If False it will not be
                      tracked.

    See `Node` for the rest of the parameters.
    """

    def __init__(
        self,
        value : Any = None,
        units : str = "",
        track : bool = True,
        **kwargs
    ):
        self.value = value
        self.units = units
        self.track = track
        super().__init__(**kwargs)

    @property
    def value(self) -> Any:
        """Get the value of the object."""
        return self._value

    @value.setter
    def value(self, new_value : Any):
        """Set the value of the object."""
        self._value = new_value

    @property
    def units(self) -> str:
        """Get the units of the object."""
        return self._units

    @units.setter
    def units(self, new_units : str):
        """Set the units."""
        ureg.check(new_units)
        self._units = new_units

    @property
    def track(self) -> bool:
        """Check if variable is being tracked during simulations or not."""
        return self._track

    @track.setter
    def track(self, new_track : bool):
        """Change the tracking flag."""
        self._track = new_track

    def __str__(self):
        """Return a string representation of the Quantity.

        TODO: Make the formating variable and debug approach on numpy
        arrays. Make units optional.
        """
        if isinstance(self._value, float):
            res = f"{self.value:9.5f}"
        else:
            res = str(self.value)
        res += f" {self.units}"
        return res

    def to_yaml(self) -> Dict[str, Any]:
        """Turn the object to a dictionary of dictionaries."""
        res = super().to_yaml()
        dres = res[self.name]
        if isinstance(self.value, Number):
            dres["value"] = self.value
        else:
            dres["value"] = str(self.value)
        dres["units"] = self.units
        dres["track"] = self.track
        return res

    def from_yaml(self, data):
        """TODO Write me."""
        raise NotImplementedError("This is not implemented yet.")
