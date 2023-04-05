#~ovn!
"""Abstract definitions for a sensor

Author:
    R Murali Krishnan
    
Date:
    04.05.2023

"""

from cdcm import *

class Sensor(System):
    """A sensor component with one test and health-status variable"""
    pass


def make_sensor_test(
        test_name: str
        ):
    """Make a test variable dependent on sensor systems"""
    pass
