#~ovn!
"""Test the sensor component

Author:
    R Murali krishnan
    
Date:
    04.15.2023
    
"""


from cdcm import *
from cdcm_abstractions import *
from cdcm_utils import *


def make_sensor(
        sensor_name: Union[str, System], 
        **kwargs) -> System:

    with maybe_make_system(sensor_name, **kwargs) as sensor:

        hvar = make_health_variable(
            name="health_variable",
            value=0,
            support=(0, 1, 2),
            description="Health variable of the sensor" 
        )
        @make_functionality("sense_power")
        def fn_func_sense_power(h=hvar):
            if h < 2:
                return 1.
            else:
                return 0.
        
        @make_test("test_health_sensor")
        def fn_test_health_sensor(h=hvar):
            if h < 2:
                return 0.
            else:
                return 1.

        pass
    pass

with System(name="system") as sys:

    clock = make_clock(dt=1.0, units="hr")

    # Model of a sensor
    sensor = make_sensor("temperature_sensor")


print("~ovn!")
print(sys)

from pprint import pprint

pprint(vars(sys))

sys = make_pyvis_graph(sys, "test_sensors.html")

