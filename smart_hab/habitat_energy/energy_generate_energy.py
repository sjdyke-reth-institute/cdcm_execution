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

        solar_cell_energy_max = Parameter(name="solar_cell_energy_max",
                                     value=0.08645881805490926,
                                     units="J",
                                     description="Maximum energy solar power could generate in 1 second in maximum solar radiation with 100% efficiency")
        solar_cell_capacity = Parameter(name="solar_cell_capacity",
                                         value=0.3,
                                         units="",
                                         description="Efficiency of the solar panels")

        nuclear_fuel_rate = Parameter(name="nuclear_fuel_rate",
                                       value=10**(-5),
                                       units="kg/sec",
                                       description="Rate of nuclear fuel fed to the reactor")
        nuclear_capacity = Parameter(name="nuclear_capacity",
                                      value=2.4 * 10**(8),
                                      units="J/kg",
                                      description="Amount of energy 1 kg nuclear fuel will free")

        gen_energy_solar = State(name="gen_energy_solar",
                                     value=0.0,
                                     units="J",
                                     description="Generated solar energy in this time step")
        gen_energy_nuclear = State(name="gen_energy_nuclear",
                                       value=0.0,
                                       units="J",
                                       description="Generated nuclear energy in this time step")
        gen_energy_total = State(name="gen_energy_total",
                                     value=0.0,
                                     units="J",
                                     description="Total generated energy in this time step")

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
