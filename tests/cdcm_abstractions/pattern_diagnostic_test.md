## Patterns for defining a diagnostic test

```python
from cdcm import *
from cdcm_abstractions import *
from cdcm_utils import *


with System(name="system") as sys:

    clock = make_clock(dt=1.0, units="hr")

    hvar = make_health_variable(
        name="hvar",
        value=0.,
        description="Health variable of the system"
    )
    @make_test("test_hvar")
    def fn_test_hvar(h=hvar):
        """Test for the health variable"""
        if h > 0.75:
            return 1.
        else:
            return 0.
        

print("~ovn!")

print(sys)
sys.forward()

print("~~ovn!")

sys_graph = make_pyvis_graph(sys, "test_diagnostic_tests.html")
```
