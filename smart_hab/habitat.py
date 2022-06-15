"""
Make the entire system.

"""


from cdcm import *
from disturbances import *


with System(name="everything",
    description="Everything that goes in the simulation") as everything:
    pass
    # Make a clock
    clock = make_clock(3600.0)

    moon = make_moon(clock)


print(everything)
