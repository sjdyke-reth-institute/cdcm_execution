"""
Make the entire system.

"""


from cdcm import *
from disturbances import *
from dome_design import *
from habitat_structure import *
from habitat_energy import *

from placeholder_handelers.place_holder_handeler import place_holders

path_data_files = './data_files/'

with System(name="everything",
    description="Everything that goes in the simulation") as everything:

    place_holder_0 = place_holders()
    place_holder_0.define_place_holder()

    # Make a clock
    clock = make_clock(3600.0)

    dome_specs = make_dome_specs()
    # TODO: comment on decomposition
    moon = make_moon(path_data_files, clock, dome_specs)
    struct = make_structure(moon,
                            dome_specs,
                            place_holder_0.place_holder_int_env_temp,
                            place_holder_0.place_holder_agent_repair_struct)
    energy = make_energy(clock,
                         moon,
                         place_holder_0.place_holder_power_cons,
                         place_holder_0.place_holder_agent_clean_panel,
                         place_holder_0.place_holder_agent_clean_plant,
                         place_holder_0.place_holder_agent_cover_panel)

    # place_holder_0.replace_place_holder()
print(everything)
