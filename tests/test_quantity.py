"""
Tests quantities using pytest.

Author:
	Roman Ibrahimov

Date:
	3/11/2022
"""


import pytest
import numpy as np
from cdcm import *
import pint


class TestQuantities():

    """
    Class for testing quantities
    """

    ureg = pint.UnitRegistry()

    def test_success_parameter_1(self):
        """
        Tests the data types of value in Quantity class
        """
        # Testing floating point value
        p = Quantity(0.5, self.ureg.m, "random_name", True, "description")
        # Testing integer value
        p = Quantity(1, self.ureg.m, "random_name", False, "description")

    def test_success_parameter_2(self):
        """
        Tests different units in Quantity class
        """
        # units of length
        p = Quantity(2, self.ureg.parsec, "random_name", True, "description")
        p = Quantity(2, self.ureg.ly, "random_name", True, "description")
        p = Quantity(2, self.ureg.mile, "random_name", True, "description")
        p = Quantity(2, self.ureg.km, "random_name", True, "description")
        p = Quantity(2, self.ureg.yard, "random_name", True, "description")
        p = Quantity(2, self.ureg.foot, "random_name", True, "description")
        p = Quantity(2, self.ureg.dm, "random_name", True, "description")
        p = Quantity(2, self.ureg.cm, "random_name", True, "description")
        p = Quantity(2, self.ureg.mm, "random_name", True, "description")
        p = Quantity(2, self.ureg.micrometer, "random_name", True, "description")
        p = Quantity(2, self.ureg.nm, "random_name", True, "description")
        # units of time
        p = Quantity(2, self.ureg.year, "random_name", True, "description")
        p = Quantity(2, self.ureg.month, "random_name", True, "description")
        p = Quantity(2, self.ureg.week, "random_name", True, "description")
        p = Quantity(2, self.ureg.day, "random_name", True, "description")
        p = Quantity(2, self.ureg.hour, "random_name", True, "description")
        p = Quantity(2, self.ureg.minute, "random_name", True, "description")
        p = Quantity(2, self.ureg.second, "random_name", True, "description")
        p = Quantity(2, self.ureg.millisecond, "random_name", True, "description")
        p = Quantity(2, self.ureg.microsecond, "random_name", True, "description")
        p = Quantity(2, self.ureg.micrometer, "random_name", True, "description")
        p = Quantity(2, self.ureg.nanosecond, "random_name", True, "description")
        # units of temperature
        p = Quantity(2, self.ureg.degF, "random_name", True, "description")
        p = Quantity(2, self.ureg.kelvin, "random_name", True, "description")
        p = Quantity(2, self.ureg.degC, "random_name", True, "description")
        # units of mass
        p = Quantity(2, self.ureg.metric_ton, "random_name", True, "description")
        p = Quantity(2, self.ureg.ton, "random_name", True, "description")
        p = Quantity(2, self.ureg.kilogram, "random_name", True, "description")
        p = Quantity(2, self.ureg.pound, "random_name", True, "description")
        p = Quantity(2, self.ureg.troy_ounce, "random_name", True, "description")
        p = Quantity(2, self.ureg.ounce, "random_name", True, "description")
        p = Quantity(2, self.ureg.carat, "random_name", True, "description")
        p = Quantity(2, self.ureg.gram, "random_name", True, "description")
        p = Quantity(2, self.ureg.milligram, "random_name", True, "description")
        p = Quantity(2, self.ureg.microgram, "random_name", True, "description")
        # units of electrical measurement
        p = Quantity(2, self.ureg.volt, "random_name", True, "description")
        p = Quantity(2, self.ureg.ohm, "random_name", True, "description")
        p = Quantity(2, self.ureg.ampere, "random_name", True, "description")
        # units of the amount of substance
        p = Quantity(2, self.ureg.mole, "random_name", True, "description")
        p = Quantity(2, self.ureg.troy_ounce, "random_name", True, "description")
        p = Quantity(2, self.ureg.ounce, "random_name", True, "description")
        p = Quantity(2, self.ureg.carat, "random_name", True, "description")
        p = Quantity(2, self.ureg.gram, "random_name", True, "description")
        p = Quantity(2, self.ureg.milligram, "random_name", True, "description")
        p = Quantity(2, self.ureg.microgram, "random_name", True, "description")
        # unit of luminous intensity
        p = Quantity(2, self.ureg.cd, "random_name", True, "description")

    def test_success_parameter_3(self):
        """
        Tests different names in Quantity class
        """
        p = Quantity(2, self.ureg.degC, "random name", True, "description")
        p = Quantity(2, self.ureg.degC, "random_name", True, "description")

    def test_success_parameter_4(self):
        """
        Tests the track in Quantity class
        """
        p = Quantity(2, self.ureg.degC, "random name", True, "description")
        p = Quantity(2, self.ureg.degC, "random_name", False, "description")

    def test_success_parameter_5(self):
        """
        Tests the description in Quantity class
        """
        p = Quantity(2, self.ureg.degC, "random name", True, None)
        p = Quantity(2, self.ureg.degC, "random_name", False, "description")


if __name__ == '__main__':
    p = PhysicalStateVariable(10.0, "meters", "length",True,"description")
    print(str(p))
    print(p.__repr__())
    p = PhysicalStateVariable(10.0, "meters", "length",True,
        description="Some very very very very long description.")
    print(str(p))
    print(p.__repr__())
