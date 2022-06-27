"""A Energy_generation model.

variable :: TypeOfVariable

(variable) = optional variable

                                               ___________________________
energy_performance  :: Energy_Performance  => |                           | ->  generated solar energy   :: State
                                              |                           |
                                              | Energy_generate_energyEnv |
clock               :: Clock               => |                           |
iradiance           :: Moon                => |                           | ->  generated nuclear energy :: State
                                               ___________________________

"""

__all__ = ["make_energy_generate_energy_env_0"]



from cdcm import *
import numpy as np

def make_energy_generate_energy_env_0(clock, moon,
                              energy_performance):
    with System(name="energy_generate_energy", description="The energy_generate_energy environment") as energy_generate_energy:

        solar_cell_energy_max = (make_node("P:solar_cell_energy_max",
                                     value=0.08645881805490926,
                                     units="J",
                                     description="solar_cell_energy_max"))
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
        
        gen_energy_solar = (make_node("S:gen_energy_solar",
                                     value=0.0,
                                     units="J",
                                     description="gen_energy_solar"))
        gen_energy_nuclear = (make_node("S:gen_energy_nuclear",
                                       value=0.0,
                                       units="J",
                                       description="gen_energy_nuclear"))
        gen_energy_total = (make_node("S:gen_energy_total",
                                     value=0.0,
                                     units="J",
                                     description="gen_energy_total"))

        @make_function(gen_energy_solar)
        def f_gen_energy_solar(accum_dust_solar=energy_performance.accum_dust_solar,
                              functional_covered=energy_performance.functional_covered,
                              solar_cell_capacity=solar_cell_capacity,
                              solar_cell_energy_max=solar_cell_energy_max,
                              dt=clock.dt,
                              irradiance=moon.radiation.irradiance):
            """Transition function for gen_energy_solar"""

            gen_energy_solar_new = max(accum_dust_solar *
                                        irradiance * functional_covered *
                                        solar_cell_capacity *
                                        solar_cell_energy_max * dt, 0.0)
            return gen_energy_solar_new

        @make_function(gen_energy_nuclear)
        def f_gen_energy_nuclear(accum_dust_nuclear=energy_performance.accum_dust_nuclear,
                                nuclear_capacity=nuclear_capacity,
                                nuclear_fuel_rate=nuclear_fuel_rate,
                                dt=clock.dt):
            """Transition function for gen_energy_nuclear_new"""
            gen_energy_nuclear_new = max(accum_dust_nuclear *
                                          nuclear_capacity,
                                          0.0) * nuclear_fuel_rate * dt
            return gen_energy_nuclear_new

        @make_function(gen_energy_total)
        def f_gen_energy_total(gen_energy_solar=gen_energy_solar,
                              gen_energy_nuclear=gen_energy_nuclear):
            """Transition function for gen_energy_total"""
            gen_energy_total_new = gen_energy_solar + gen_energy_nuclear
            return gen_energy_total_new
    return energy_generate_energy
