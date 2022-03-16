"""Defines a Quantify class.

Author:
    Ilias Bilionis
    Roman Ibrahimov

Date:
    3/10/2022

TODO:
    Figure out how to enforce SI units.
"""


__all__ = ['Quantity', 'Parameter', 
           'StateVariable', 'PhysicalStateVariable', 'HealthStateVariable']


import numpy as np
import pint
from . import trim_str


ureg = pint.UnitRegistry()


class Quantity(object):

    """
    Defines a CDCM quantity. The quantity knows its units.
    It has a decscription that explains what it is.
    It has a name. And it has a value.

    Arguments:

        value:      The value of the quantity. Must be an int, a double or a 
                    numpy array of ints or floating point numbers.
        units:      Must be a string or a pint object that describes an SI
                    physical unit.
        name:       A string. The name of the quantity. Please be expressive.
        track:      A boolean. If True the quantity will be tracked during
                    simulatiojns. If False it will not be tracked.
        desciption: A desciption of the quantity. Please be expressive.

    """

    def __init__(self, value, units=None, name=None, track=True, description=None):
        # Sanity checks
        if isinstance(value, int):
            dtype = int
            shape = ()
        elif isinstance(value, float):
            dtype = float
            shape = ()
        elif isinstance(value, np.ndarray):
            dtype = value.dtype
            shape = value.shape
        else:
            raise RuntimeError(
                    f"I cannot handle the type of the quantity {value}")
        ureg.check(units)
        assert name is None or isinstance(name, str)
        assert isinstance(track, bool)
        assert description is None or isinstance(description, str)
        # Assign values
        self._dtype = dtype
        self._shape = shape
        self._value = value
        self._units = units 
        self._name = name
        self._track = track
        self._description = description

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
    
    def __str__(self):
        """
        Return a string representation of the Quantity.
        """
        if isinstance(self._value, float):
            res = f"{self._value: {1}.{5}}"
        else:
            res = str(self._value)
        res += f" {self._units} ({self.type})"
        return res
        
    def __repr__(self):
        """
        Return an unambiguous text describing the object.
        """
        res = f'{self.type}(value={self.value}, units="{self.units}", ' + \
              f'name="{self.name}", description='
        if self.description is None:
            res += "None"
        else:
            res += f'"{trim_str(self.description)}"'
        res += ")"
        return res


class Parameter(Quantity):

    """
    A class representing a parameter of a system.
    """

    pass 


class StateVariable(Quantity):

    """
    A class representing a system state variable.
    """

    pass


class PhysicalStateVariable(StateVariable):

    """
    A class representing a physical system state variable.
    """

    pass 


class HealthStateVariable(StateVariable):

    """
    A class representing a health state variable.
    """

    pass

