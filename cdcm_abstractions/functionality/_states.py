"""Constructors for State type nodes for functionality models

Author:
    R Murali Krishnan
    
Date:
    10.02.2023
    
"""


from cdcm import State


class HealthState(State):
    """A class representing a health state variable"""
    pass


class BinaryHealthState(HealthState):
    """A class representing a Binary health state variable

    This is a `HealthState` variable which takes binary values {0, 1}.
    """
    pass


class ContinuousHealthState(HealthState):
    """A class representing a continuous health state variable

    This is a `HealthState` variable which takes real number values.

    See `State` in the CDCM execution language for the keyword arguments
    """
    def __init__(self, *args, value, **kwargs) -> None:
        self.nominal_value = value
        super().__init__(*args, value=self.nominal_value, **kwargs)