"""A structure_health model.


                                               _________________________
Agents             :: cleaning             => |                        |
                                              |   StructureHealthEnv   | ->  sperformance level of energy from solar and nuclear
disturbance        :: dust                 => |                        |
                                              _________________________

"""


__all__ = ["make_energy_performance_env_0"]



from cdcm import *

def make_energy_performance_env_0(clock, moon, clean_panel, clean_plant, cover_panel):
    with System(name="energy_performance", description="The structure_health environment") as energy_performance:
        accum_dust_solar = (make_node("S:accum_dust_solar",
                                      value=1.0,
                                      units="",
                                      description="accum_dust_solar"))
        accum_dust_nuclear = (make_node("S:accum_dust_nuclear",
                                        value=1.0,
                                        units="",
                                        description="accum_dust_nuclear"))
        functional_covered = (make_node("S:functional_covered",
                                        value=1.0,
                                        units="",
                                        description="functional_covered"))

        @make_function(accum_dust_solar,
                       accum_dust_nuclear, 
                       functional_covered)
        def f_accum_dust(accum_dust_solar=accum_dust_solar,
                         accum_dust_nuclear=accum_dust_nuclear,
                         cleaning_panels=clean_panel,
                         cleaning_rads=clean_plant,
                         dt=clock.dt,
                         dust_rate=moon.dust.dust_rate,
                         functional_covered=cover_panel):
            """Transition function for accum_dust s"""
            accum_dust_solar_new = min(max(accum_dust_solar +
                                             dt * (-dust_rate *
                                                     functional_covered +
                                                     cleaning_panels), 0.0),
                                         1.0)
            accum_dust_nuclear_new = min(max(accum_dust_nuclear +
                                               dt * (-dust_rate +
                                                       cleaning_rads), 0.0),
                                           1.0)
            return accum_dust_solar_new, accum_dust_nuclear_new

        @make_function(functional_covered)
        def f_functional_covered(covering_panels=cover_panel):
            """Transition function for covering_panels_solar"""
            functional_covered_new = covering_panels
            return functional_covered_new
        
    return energy_performance
