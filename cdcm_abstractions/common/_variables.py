"""Constructors for Variable type nodes for functionality models

Author:
    R Murali Krishnan
    
Date:
    10.02.2023
    
"""


from cdcm import Variable



class HealthVariable(Variable):
    """A class representing a health variable"""
    pass


class BinaryHealthVariable(HealthVariable):
    """A class representing a binary health state variable

    This is a `HealthState` variable which takes discrete binary values {0, 1}

    See `State` in the CDCM execution language for the keyword arguments.
    """

    pass


class ContinuousHealthVariable(HealthVariable):
    """A class representing a continuous health state variable"""
    pass






class Functionality(Variable):
    """A class representing a functionality variable

    This is a `Variable` that represents the concept of a component functionality

    See `Variable` in the CDCM execution language for the keyword arguments.
    """

    def __init__(self, *args, nominal_value, **kwargs) -> None:
        self.nominal_value = nominal_value
        super().__init__(value=nominal_value, *args, **kwargs)