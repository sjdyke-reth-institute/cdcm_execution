"""Test models of components

Author:
    R Murali Krishnan
    
Date:
    10.02.2023

"""


from cdcm import *
from cdcm_abstractions import *


with System(name="system_of_components") as system_of_components:

    clock = make_clock(dt=1.0, units="hr")

    # Simple component that have - [HealthVariable, Functionality] nodes
    simple_component = make_component("simple_component", nominal_health=1.0)


print(system_of_components)