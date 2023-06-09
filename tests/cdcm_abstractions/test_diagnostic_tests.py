#~ovn!
"""Test diagnostic test variables

Author:
    R Murali krishnan
    
Date:
    04.15.2023

"""

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

# Arithmetic operations on `test` variables
import numpy as np


with System(name="math") as math:

    clock = make_clock(dt=1.0, units="hr")

    var = Variable(name="var", value=0)

    @make_function(var)
    def fn(t=clock.t):
        return np.sin(t)
    
    # Compose new tests
    test1 = BinaryTest(name="test1", value=1)
    test2 = BinaryTest(name="test2", value=1)

    test3 = test1 + test2
    # test3.name = "test3"

    test4 = test1 * var
    # test4.name = "test4"

print(math)

def trigger_test(test):
    print("*** Event (set_omega_to_minus_one ***)")
    def _trigger_test_inner():
        test.value = 0
    return _trigger_test_inner

model = Simulator(math)

model.add_event(10.0, trigger_test(test1))

for i in range(20):
    model.forward()
    print(f"**t={model.system.clock.t.value}, ",
          f"(+ test1 test2)   =   {getattr(model.system, '(+ test1 test2)').value}, ",
          f"(* test1 var)     =   {getattr(model.system, '(* test1 var)').value}")
    model.transition()