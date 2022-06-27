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
    # energy = make_energy(clock,
    #                      moon,
    #                      place_holder_0.place_holder_energy_cons,
    #                      place_holder_0.place_holder_agent_clean_panel,
    #                      place_holder_0.place_holder_agent_clean_plant,
    #                      place_holder_0.place_holder_HM_cover_panel)
    energy = make_energy(clock, moon)
    # eclss = make_eclss(clock,
    #                    dome_specs,
    #                    energy_available_energy=place_holder_0.place_holder_available_en,
    #                    struct_health=place_holder_0.place_holder_struct_health,
    #                    struct_inside_temperature=place_holder_0.place_holder_int_str_temp,
    #                    interior_env_temperature=place_holder_0.place_holder_int_env_temp,
    #                    interior_env_pressure=place_holder_0.place_holder_int_env_pres,
    #                    HM_temperature_lower_setpoint=place_holder_0.place_holder_HM_pressure_lower_setpoint,
    #                    HM_temperature_upper_setpoint=place_holder_0.place_holder_HM_pressure_upper_setpoint,
    #                    HM_pressure_lower_setpoint=place_holder_0.place_holder_HM_pressure_lower_setpoint,
    #                    HM_pressure_upper_setpoint=place_holder_0.place_holder_HM_pressure_upper_setpoint)
    eclss = make_eclss(clock, dome_specs)
    # struct = make_structure(moon,
    #                         dome_specs,
    #                         place_holder_0.place_holder_int_env_temp,
    #                         place_holder_0.place_holder_agent_repair_struct)
    struct = make_structure(moon, dome_specs)
    # int_env = make_int_env(dome_specs,
    #                        eclss_en_used_heat=place_holder_0.place_holder_en_used_heat,
    #                        eclss_en_needed_heat=place_holder_0.place_holder_en_needed_heat,
    #                        eclss_en_used_pres=place_holder_0.place_holder_en_used_pres,
    #                        eclss_en_needed_pres=place_holder_0.place_holder_en_needed_pres,
    #                        struct_health=place_holder_0.place_holder_struct_health,
    #                        struct_inside_temperature=place_holder_0.place_holder_int_str_temp,
    #                        HM_temperature_lower_setpoint=place_holder_0.place_holder_HM_pressure_lower_setpoint,
    #                        HM_temperature_upper_setpoint=place_holder_0.place_holder_HM_pressure_upper_setpoint,
    #                        HM_pressure_lower_setpoint=place_holder_0.place_holder_HM_pressure_lower_setpoint,
    #                        HM_pressure_upper_setpoint=place_holder_0.place_holder_HM_pressure_upper_setpoint)
    int_env = make_int_env(dome_specs)

everything = place_holder_0.replace_place_holder(everything)
print(everything)
