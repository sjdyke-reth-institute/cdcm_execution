#~ovn!
"""Test a basic model of a component

Author:
    R Murali Krishnan
    
Date:
    03.31.2023
    
"""

from cdcm import *
from cdcm_abstractions import *
from cdcm_utils import *

import numpy as np



with System(name="sys") as sys:
    # Make a clock
    clock = make_clock(dt=1.0, units="hr")

    hs1 = make_health_status(
        name="status1",
        value=0.,
        support=(0., 1.),
        description="A continuous status variable"
    )

    hs2 = make_health_status(
        name="status2",
        value=0,
        support=(0, 1),
        description="A discrete (binary) health status variable"
    )

    with System(name="component") as component:
        status = make_health_status(
            name="status",
            value=0,
            support=(0, 1)
        )
        usability = Functionality(
            name="usability",
            value=0.,
            description="Variable describing the functionality of component"
        )
        @make_function(status)
        def calc_usability_of_component(s=usability):
            if s == 0:
                return 1.
            else:
                return 0.

    with System(name="component_w_sensor") as component_w_sensor:
        status_1 = make_health_status(
            name="health_status_1",
            value=0,
            support=(0, 1)
        )
        status_2 = make_health_status(
            name="health_status_2",
            value=0.,
            support=(0., 1.),
            description="Continuous status variable"
        )
        usability_comp = Functionality(
            name="usability_comp",
            value=0.,
            description="Component is usable."
        )
        @make_function(usability_comp)
        def calc_can_function(hs_1=status_1, hs_2=status_2):
            """Can the system be `used`?"""
            if hs_1 == 0 and hs_2 == 0:
                return 1.
            else:
                return 0.5
            
        with System(name="sensor") as sensor:
            status_sensor = make_health_status(
                name="status_sensor",
                value=0,
                support=(0, 1)
            )
            usability_sensor = Functionality(
                name="usability_sensor",
                value=0.,
                description="Functionality variable of the sensor"
            )
            def func_usability_sensor(status):
                """Function for usable sensor"""
                if status == 0:
                    return 1.
                else:
                    return 0.

            func_usable_sensor = Function(
                name="func_usable_sensor",
                parents=(status_sensor,),
                children=usability_sensor,
                func=func_usability_sensor,
                description="Function that calculates if the sensor is usable"
            )

            test = Test(
                name="test",
                value=0,
                description="Variable fo capturing the results of the test"
            )
            # TestFunction :: Type of function
            # requires =>
            #   Set<SensorFunctionality> Nodes
            #   Set<HealthStatus> Nodes on which test function is defined
            #   \lambda <Set<HealthStatus>]>
            @make_function(test)
            def calc_test_result(f_sensor=usability_sensor, hs1=status_1, hs2=status_2):
                """Calculate the test result"""
                if f_sensor == 0:
                    return -1.
                else:
                    if hs1 == 0 and hs2 == 0:
                        return 0.
                    else:
                        return 1.
    
    f1 = Functionality(
        name="f1",
        value=0,
        description="Discrete Functionality of `sys`"
    )
    @make_function(f1)
    def calculate_functionality1(f_1=component.status, f_2=component_w_sensor.usability_comp):
        return f_1 * f_2

    f2 = Functionality(
        name="f2",
        value=0.,
        description="Continuous functionality of `sys`"
    )
    @make_function(f2)
    def calculate_functionality2(t=clock.t, f_2=component_w_sensor.usability_comp):
        return np.sin(t) + f_2

    value = Variable(
        name="value",
        value=0.,
        description="Value"
    )
    @make_function(value)
    def calculate_value(f_1=f1, f_2=f2):
        return f_1 * f_2

            

print(sys)
sys.forward()
sys_interactive = make_pyvis_graph(sys, "test_variable_types.html")

