"""Description of sensor and fault detection and diagnosis (FDD) systems

Author:
    R Murali Krishnan

Date:
    03.16.2023

"""


from cdcm import *

from .health_status import make_health_status

class Sensor(System):
    """Description of a sensor system"""
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name=name, **kwargs)

    def define_internal_nodes(self, **kwargs):

        raise NotImplementedError("Implement me..")

class FDD(System):
    """Description of an FDD System"""
    
    def __init__(self):
        raise NotImplementedError("Implement me..")