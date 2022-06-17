"""
Make the entire system.

"""


from cdcm import *
from disturbances import *
from dome_design import *

path_data_files = './data_files/'

with System(name="everything",
    description="Everything that goes in the simulation") as everything:
    pass
    # Make a clock
    clock = make_clock(3600.0)
    dome_specs = make_dome_specs()
    moon = make_moon(path_data_files, clock, dome_specs)


print(everything)
