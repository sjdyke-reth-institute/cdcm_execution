#~ovn!
"""Tests for health variables

Author:
    R Murali Krishnan
    
Date:
    04.15.2023
    
"""

from cdcm import *
from cdcm_abstractions import *
from cdcm_utils import *


print("~ovn!")

with System(name="sys") as sys:

    # Make a clock
    clock = make_clock(dt=1.0, units="hr")

    hs1 = make_health_variable(
        name="status1",
        value=0.,
        support=(0., 1.),
        description="A continuous health variable"
    )

    hs2 = make_health_variable(
        name="status2",
        value=0,
        support=(0, 1),
        description="A binary health variable"
    )

    with System(name="component") as component:
        hs3 = make_health_variable(
            name="status3",
            value=0,
            support=(0, 1, 2),
            description="A discrete health variable"
        )

print("~~ovn!")
from pprint import pprint

pprint(vars(sys))

sys.forward()

sys_graph = make_pyvis_graph(sys, "test_health_variables.html")