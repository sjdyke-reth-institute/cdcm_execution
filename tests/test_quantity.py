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

    def test_success_parameter(self):
        """
        Tests if the data types of input arguments have changed in Quantity class
        """
        # Testing floating point value
        p = Quantity(0.5, "meters", "random_name", "Blah blah")
        # Testing integer value

    def test_success_parameter_2(self):
        p = Quantity(2, "meters", "random_name", "Blah blah")
        # Testing different units
        p = Quantity(2, "seconds", "random_name", "Blah blah")
        p = Quantity(2, "s", "random_name", "Blah blah")
        p = Quantity(2, "kg", "random_name", "Blah blah")
        p = Quantity(2, "grams", "random_name", "Blah blah")
        p = Quantity(2, "miles", "random_name", "Blah blah")
        # No description
        p = Quantity(2, "miles", "random_name")


if __name__ == '__main__':
    p = PhysicalStateVariable(10.0, "meters", "length")
    print(str(p))
    print(p.__repr__())
    p = PhysicalStateVariable(10.0, "meters", "length", 
        description="Some very very very very long description.")
    print(str(p))
    print(p.__repr__())
