"""Defines a Quantify class.

Author:
    Ilias Bilionis
    Roman Ibrahimov

Date:
    3/10/2022
"""


__all__ = ['Quantity', 'Parameter',
           'StateVariable', 'PhysicalStateVariable', 'HealthStateVariable']


import numpy as np
import pint
from . import NamedType


ureg = pint.UnitRegistry()


class Quantity(NamedType):
    """Defines a CDCM quantity.

    The quantity knows its units. It has a decscription that explains
    what it is. It has a name. And it has a value.

    Arguments:

        value      -- The value of the quantity. Must be an int, a
                      double or a numpy array of ints or floating point
                      numbers. We also allow it to be a string.
        units      -- Must be a string or a pint object that describes
                      an SI physical unit.
        name       -- A string. The name of the quantity. Please be
                      expressive.
        track      -- A boolean. If True the quantity will be tracked
                      during simulations. If False it will not be
                      tracked.
        desciption -- A desciption of the quantity. Please be
                      expressive.
    """

    def __init__(self, value, units="", name="quantity", track=True,
                 description=""):
        self._initilize(value, units, track)
        super().__init__(name=name, description=description)

    def _initilize(self, value, units, track):
        """Do some sanity checks and set the value."""
        if isinstance(value, int):
            dtype = int
            shape = ()
        elif isinstance(value, float):
            dtype = float
            shape = ()
        elif isinstance(value, str):
            dtype = str
            # TODO: Check if this is the correct thing to do for HDF5.
            shape = ()
        elif isinstance(value, (list, tuple, np.ndarray)):
            value = np.array(value)
            dtype = value.dtype
            shape = value.shape
        else:
            raise RuntimeError(f"I cannot handle the type of the"
                               + " quantity {value}")
        ureg.check(units)
        assert isinstance(track, bool)
        self._dtype = dtype
        self._shape = shape
        self._value = value
        self._units = units
        self._track = track

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        assert isinstance(self.value, type(new_value))
        self._value = new_value

    @property
    def dtype(self):
        return self._dtype

    @property
    def shape(self):
        return self._shape

    @property
    def units(self):
        return self._units

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def type(self):
        return type(self).__name__

    @property
    def track(self):
        return self._track

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

    def to_yaml(self):
        """Turn the object to a dictionary of dictionaries."""
        res = super().to_yaml()
        dres = res[self.name]
        if isinstance(self.value, np.ndarray):
            dres["value"] = str(self.value)
        else:
            dres["value"] = self.value
        dres["units"] = self.units
        dres["track"] = self.track
        return res

    def from_yaml(self, data):
        """TODO Write me."""
        super().from_yaml(data)
        self._initilize(data["value"],
                        data["units"],
                        data["track"])


class Parameter(Quantity):
    """A class representing a parameter of a system."""

    pass


class StateVariable(Quantity):
    """A class representing a system state variable."""

    pass


class PhysicalStateVariable(StateVariable):
    """A class representing a physical system state variable."""

    pass


class HealthStateVariable(StateVariable):
    """A class representing a health state variable."""

    pass
