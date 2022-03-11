"""
Tests parameters using pytest.

Author:
	Dr. Ilias Bilionis
	Roman Ibrahimov

Date:
	3/11/2022
"""


import pytest
import numpy as np
from cdcm import *
import pint


class TestParameters():

    """
    Class for testing parameters
    """

    # input arguments for Paramter class
    _value = 5
    _units = "unit"
    _name = "name"
    _description = "description"
    _param = Parameter(_value, _units, _name, _description)
    _ureg = pint.UnitRegistry()

    def test_data_types(self):

        """
        Tests if the data types of input arguments have changed in Parameter class
        """

        param = self._param
        assert isinstance(param.value, int)
        self._ureg.check(self._units)
        assert isinstance(param.name, str)
        assert isinstance(param.description, str)


    def test_param_values(self):

        """
        Tests if the values of input arguments have changed in Parameter class
        """

        param = self._param
        assert param.value == self._value
        assert param.units == self._units
        assert param.name == self._name
        assert param.description == self._description

