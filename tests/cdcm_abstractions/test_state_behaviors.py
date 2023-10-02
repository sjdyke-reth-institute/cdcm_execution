"""Testing common patterns for describing state behaviors

Author:
    R Murali Krishnan
    
Date:
    09.22.2023
    
"""


from cdcm import State, Parameter, System, make_clock, make_function
from cdcm_utils import make_pyvis_graph


with System(name="sys") as sys:

    clock = make_clock(dt=1.0)

    x = State(name="x", value=1.0)
    r = Parameter(name="r", value=0.01)

    @make_function(x)
    def linear_function(x=x, r=r, dt=clock.dt):
        return x - r * dt


print(sys)
sys.forward()

g = make_pyvis_graph(sys)
g.show("test_state_behaviors.html")