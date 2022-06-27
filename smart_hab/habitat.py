"""
Make the entire system.

"""


from cdcm import *
from disturbances import *
from dome_design import *
from habitat_energy import *
from habitat_eclss import *
from habitat_structure import *
from habitat_int_env import *

path_data_files = './data_files/'

with System(name="everything",
    description="Everything that goes in the simulation") as everything:

    # Make a clock
    clock = make_clock(3600.0)

    dome_specs = make_dome_specs()
    
    moon = make_moon(path_data_files, clock, dome_specs)

    energy = make_energy(clock, moon)

    eclss = make_eclss(clock, dome_specs)

    struct = make_structure(moon, dome_specs)

    int_env = make_int_env(dome_specs)
    
    # Code that ensures correct coupling if needed
    # in one line
    
print(everything)
