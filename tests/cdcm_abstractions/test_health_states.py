#~ovn!
"""Test for health states

Author:
    R Murali krishnan
    
Date:
    04.15.2023
    
"""

from cdcm import *
from cdcm_abstractions import *
from cdcm_utils import *

print("~ovn!")

with System(name="system") as sys:

    clock = make_clock(dt=1.0, units="hr")

    ## !!
    # All `State` variables must be immediately
    # followed by their transition function definitions
    ## !!
    hstate1 = make_health_state(
        name="hstate1",
        value=0,
        description="A discrete health state variable"
    )
    @make_function(hstate1)
    def fn_discrete_health_state(hstate=hstate1):
        return hstate

    hstate2 = make_health_state(
        name="hstate2",
        value=10.,
        description="A continuous health state variable"
    )
    rate = Parameter(
        name="rate",
        value=0.1,
        description="A rate of consumption"
    )
    @make_function(hstate2)
    def fn_calc_consumption(hs=hstate2, r=rate, dt=clock.dt):
        """Calculate the rate of consumption"""
        return hs - r * dt

    with System(name="component") as component:
        rate_multiplier = Variable(
            name="rate_multiplier",
            value=0.,
            description="Variable that is a rate multiplier"
        )
        @make_function(rate_multiplier)
        def fn_rate_multiplier(hstate=hstate1):
            if hstate == 0:
                return 0.1
            else:
                return 1.

        hstate3 = make_health_state(
            name="hstate3",
            value=10.,
            description="A component health state"
        )

        @make_function(hstate3)
        def fn_calc_hstate3(hstate=hstate3, rate=rate_multiplier, dt=clock.dt):
            return hstate - rate * dt

print(sys) 

sys.forward()
print ("~ovn!")

from pprint import pprint

pprint(vars(sys))

sys_graph = make_pyvis_graph(sys, "test_health_state.html")