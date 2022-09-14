"""Test the input order bug in execution code
Author:
    Amir Behjat



"""


from cdcm import *
import numpy as np


with System(name="combined_system") as sys:

    # ****************************
    #       SYSTEM 1
    # ****************************

    with System(name="sys1") as sys1:
        x1 = State(name="x1", value=0.1, units="meters", description="State of sys1.")
        r1 = Parameter(
            name="r1", value=0.1324324324, units="meters", description="State of sys1."
        )
        c1 = Parameter(
            name="c1", value=0.87867, units="meters", description="State of sys1."
        )

        # This is a placeholder node useed to establish the connection between
        # the two systems:
        placeholder = Variable(
            name="placeholder",
            value=21221.3323432423423434,
            units="meters",
            description="State of sys1.",
        )

        @make_function(x1)
        def f1(x1=x1, x2=placeholder, r1=r1, c1=c1):
            """Transition function for sys1."""
            print("current print is: ")
            print(
                "f1",
                "x1",
                x1,
                "x2",
                x2,
                "r1",
                r1,
                "c1",
                c1,
            )
            print("correct print is: ")
            print("f1", "x1", 0.1, "x2", 0.3, "r1", 0.1324324324, "c1", 0.87867)
            return x1

    # ****************************
    #       SYSTEM 2
    # ****************************

    with System(name="sys2") as sys2:
        x2 = State(name="x2", value=0.3, units="meters", description="State of sys1.")

        @make_function(x2)
        def f2(x2=x2):
            """Another simple system."""
            return x2

    # ****************************
    #   CONNECT SYSTEMS
    # ****************************
    replace(placeholder, x2)

print(sys)

sys.forward()
sys.transition()
