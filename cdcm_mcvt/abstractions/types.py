#~ovn!
"""Types of abstractions used in CDCM for higher-order functions

Author:
    R Murali Krishnan
    
Date:
    04.05.2023
    
"""


from cdcm import *
from cdcm_abstractions import *


class Component(System):
    """A component system"""
    pass

class DamageableComponent(Component):
    """A component with at-least one health-status variable"""
    pass

class TestableComponent(Component):
    """A component with at-least one test variable"""
    pass

class Sensor(Component):
    """A sensor component with one test and health-status variable"""
    pass
