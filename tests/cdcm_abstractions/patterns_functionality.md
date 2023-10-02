```python
from cdcm import *
from cdcm_abstractions import *
from cdcm_utils import *

with System(name="system") as sys:

    clock = make_clock(dt=1.0, units="hr")

    hvar1 = make_health_variable(
        name="health_variable",
        value=0.,
        description="A health variable of the system"
    )
    rate = Parameter(
        name="rate",
        value=0.1,
        description="Rate of a flow"
    )

    @make_functionality("func_flow")
    def fn_func_hvar1(hvar=hvar1, rate=rate, dt=clock.dt):
        """Calculate functionality from variables"""
        if hvar == 0:
            return 2. * rate * dt
        else:
            return rate * dt

print("~ovn!")        
print(sys)

sys.forward()

print("~~ovn!")

sys_graph = make_pyvis_graph(sys, "test_functionality.html")

```

