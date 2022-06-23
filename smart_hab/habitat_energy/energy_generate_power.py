"""A structure_temp model.

                                                       _________________________________
disturbance               :: iradiance             => |                                | ->  generated solar energy
                                                      |   energy_generate_powerEnv     |
Energy_performance        :: surface temperature   => |                                | ->  generated nuclear energy
                                                       _________________________________

"""

__all__ = ["make_energy_generate_power_env_0"]



from cdcm import *
import numpy as np

def make_energy_generate_power_env_0(clock, moon,
                              energy_performance):
    with System(name="energy_generate_power", description="The energy_generate_power environment") as energy_generate_power:

        solar_cell_power_max = (make_node("P:solar_cell_power_max",
                                     value=0.08645881805490926,
                                     units="J",
                                     description="solar_cell_power_max"))
        solar_cell_capacity = (make_node("P:solar_cell_capacity",
                                         value=0.3,
                                         units="",
                                         description="solar_cell_capacity"))

        nuclear_fuel_rate = (make_node("P:nuclear_fuel_rate",
                                       value=1.0,
                                       units="kg/sec",
                                       description="nuclear_fuel_rate"))
        nuclear_capacity = (make_node("P:nuclear_capacity",
                                      value=2399.9999999432475,
                                      units="J/kg",
                                      description="nuclear_capacity"))
        
        gen_power_solar = (make_node("S:gen_power_solar",
                                     value=0.0,
                                     units="J",
                                     description="gen_power_solar"))
        gen_power_nuclear = (make_node("S:gen_power_nuclear",
                                       value=0.0,
                                       units="J",
                                       description="gen_power_nuclear"))
        gen_power_total = (make_node("S:gen_power_total",
                                     value=0.0,
                                     units="J",
                                     description="gen_power_total"))

        @make_function(gen_power_solar)
        def f_gen_power_solar(accum_dust_solar=energy_performance.accum_dust_solar,
                              functional_covered=energy_performance.functional_covered,
                              solar_cell_capacity=solar_cell_capacity,
                              solar_cell_power_max=solar_cell_power_max,
                              dt=clock.dt,
                              irradiance=moon.radiation.irradiance):
            """Transition function for gen_power_solar"""

            gen_power_solar_new = max(accum_dust_solar *
                                        irradiance * functional_covered *
                                        solar_cell_capacity *
                                        solar_cell_power_max * dt, 0.0)
            return gen_power_solar_new

        @make_function(gen_power_nuclear)
        def f_gen_power_nuclear(accum_dust_nuclear=energy_performance.accum_dust_nuclear,
                                nuclear_capacity=nuclear_capacity,
                                nuclear_fuel_rate=nuclear_fuel_rate,
                                dt=clock.dt):
            """Transition function for gen_power_nuclear_new"""
            gen_power_nuclear_new = max(accum_dust_nuclear *
                                          nuclear_capacity,
                                          0.0) * nuclear_fuel_rate * dt
            return gen_power_nuclear_new

        @make_function(gen_power_total)
        def f_gen_power_total(gen_power_solar=gen_power_solar,
                              gen_power_nuclear=gen_power_nuclear):
            """Transition function for gen_power_total"""
            gen_power_total_new = gen_power_solar + gen_power_nuclear
            return gen_power_total_new
    return energy_generate_power
