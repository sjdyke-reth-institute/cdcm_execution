"""Tests quantities using pytest.

Author:
    Roman Ibrahimov

Date:
    3/11/2022
"""


import numpy as np
from cdcm import *


class TestQuantities():
    """
    Class for testing quantities
    """

    def test_success_parameter_1(self):
        """
        Tests the data types of value in Quantity class
        """
        # Testing floating point value
        p = Quantity(43.658123, "m", "random_name", True, "description")
        # Testing integer value
        p = Quantity(1, "m", "random_name", False, "description")
        # It tests Quantity class with arrays
        arr_float = np.array([1.12, 2.2332, 3.34, 4.5326, 5.67])
        p = Quantity(arr_float, "m", "random_name", False, "description")
        arr_int = np.array((1, 2, 3, 4, 5))
        p = Quantity(arr_int, "m", "random_name", False, "description")
        arr_mixed = np.array((1, 2.34, 3, 4.32532, 5))
        p = Quantity(arr_mixed, "m", "random_name", False, "description")

    def test_success_parameter_2(self):
        """
        Tests different units in Quantity class
        """
        # units of length
        p = Quantity(2, "parsec", "random_name", True, "description")
        p = Quantity(2, "light_year", "random_name", True, "description")
        p = Quantity(2, "mile", "random_name", True, "description")
        p = Quantity(2, "km", "random_name", True, "description")
        p = Quantity(2, "yard", "random_name", True, "description")
        p = Quantity(2, "foot", "random_name", True, "description")
        p = Quantity(2, "dm", "random_name", True, "description")
        p = Quantity(2, "cm", "random_name", True, "description")
        p = Quantity(2, "mm", "random_name", True, "description")
        p = Quantity(2, "micrometer", "random_name", True, "description")
        p = Quantity(2, "nanometer", "random_name", True, "description")
        # units of time
        p = Quantity(2, "year", "random_name", True, "description")
        p = Quantity(2, "month", "random_name", True, "description")
        p = Quantity(2, "week", "random_name", True, "description")
        p = Quantity(2, "day", "random_name", True, "description")
        p = Quantity(2, "hour", "random_name", True, "description")
        p = Quantity(2, "minute", "random_name", True, "description")
        p = Quantity(2, "second", "random_name", True, "description")
        p = Quantity(2, "millisecond", "random_name", True, "description")
        p = Quantity(2, "microsecond", "random_name", True, "description")
        p = Quantity(2, "micrometer", "random_name", True, "description")
        p = Quantity(2, "nanosecond", "random_name", True, "description")
        # units of temperature
        p = Quantity(2, "degF", "random_name", True, "description")
        p = Quantity(2, "K", "random_name", True, "description")
        p = Quantity(2, "degC", "random_name", True, "description")
        # units of mass
        p = Quantity(2, "metric_ton", "random_name", True, "description")
        p = Quantity(2, "ton", "random_name", True, "description")
        p = Quantity(2, "kilogram", "random_name", True, "description")
        p = Quantity(2, "pound", "random_name", True, "description")
        p = Quantity(2, "troy_ounce", "random_name", True, "description")
        p = Quantity(2, "ounce", "random_name", True, "description")
        p = Quantity(2, "carat", "random_name", True, "description")
        p = Quantity(2, "gram", "random_name", True, "description")
        p = Quantity(2, "milligram", "random_name", True, "description")
        p = Quantity(2, "microgram", "random_name", True, "description")
        # units of electrical measurement
        p = Quantity(2, "volt", "random_name", True, "description")
        p = Quantity(2, "ohm", "random_name", True, "description")
        p = Quantity(2, "ampere", "random_name", True, "description")
        # units of the amount of substance
        p = Quantity(2, "mole", "random_name", True, "description")
        p = Quantity(2, "troy_ounce", "random_name", True, "description")
        p = Quantity(2, "ounce", "random_name", True, "description")
        p = Quantity(2, "carat", "random_name", True, "description")
        p = Quantity(2, "gram", "random_name", True, "description")
        p = Quantity(2, "milligram", "random_name", True, "description")
        p = Quantity(2, "microgram", "random_name", True, "description")
        # unit of luminous intensity
        p = Quantity(2, "cd", "random_name", True, "description")

    def test_success_parameter_3(self):
        """
        Tests different names in Quantity class
        """
        p = Quantity(2, "degC", "random name", True, "description")
        p = Quantity(2, "degC", "random_name", True, "description")

    def test_success_parameter_4(self):
        """
        Tests the track in Quantity class
        """
        p = Quantity(2, "degC", "random name", True, "description")
        p = Quantity(2, "degC", "random_name", False, "description")

    def test_success_parameter_5(self):
        """
        Tests the description in Quantity class
        """
        p = Quantity(2, "degC", "random name", True)
        p = Quantity(2, "degC", "random_name", False, "description")

