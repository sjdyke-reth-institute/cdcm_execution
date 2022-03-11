"""
Tests parameters using pytest.

Author:
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

    def test_success_parameter(self):
        """
        Tests if the data types of input arguments have changed in Parameter class
        """
        # Testing floating point value
        p = Parameter(0.5, "meters", "random_name", "Blah blah")
        # Testing integer value

    def test_success_parameter_2(self):
        p = Parameter(2, "meters", "random_name", "Blah blah")
        # Testing different units
        p = Parameter(2, "seconds", "random_name", "Blah blah")
        p = Parameter(2, "s", "random_name", "Blah blah")
        p = Parameter(2, "kg", "random_name", "Blah blah")
        p = Parameter(2, "grams", "random_name", "Blah blah")
        p = Parameter(2, "miles", "random_name", "Blah blah")
        # No description
        p = Parameter(2, "miles", "random_name")

