"""
Author: Amir Behjat

Date:
    7/08/2022

A Energy performance model. This model's output specifies how much energy compared to nominal performance can be generated



variable :: TypeOfVariable

(variable) = optional variable
                                        ___________________________
(cleaning_panel)      :: Agents    => |                           | ->  performance_cleannese_solar        :: State
(cleaning_radiator)   :: Agents    => |                           |
(covering_panel)      :: HM        => |   Energy_performanceEnv   | ->  performance_cleannese_nuclear      :: State
clock                 :: Clock     => |                           |
dust                  :: Moon      => |                           | ->  performance_being_functional_solar :: State
                                       ___________________________

"""

from cdcm import *

__all__ = ["make_energy_performance_env_0"]


def make_energy_performance_env_0(
    clock, dust_rate, clean_panel, clean_plant, cover_panel
):
    with System(
        name="energy_performance", description="The structure_health environment"
    ) as energy_performance:
        accum_dust_solar = State(
            name="accum_dust_solar",
            value=1.0,
            units="",
            description="cleanness of the solar panel; 1 is the cleanest",
        )
        accum_dust_nuclear = State(
            name="accum_dust_nuclear",
            value=1.0,
            units="",
            description="cleanness of the nuclear radiators; 1 is the cleanest",
        )
        functional_covered = State(
            name="functional_covered",
            value=1.0,
            units="",
            description="functionality of the solar panel; 1 is functional, 0 is covered",
        )

        @make_function(accum_dust_solar, accum_dust_nuclear)
        def f_accum_dust(
            accum_dust_solar=accum_dust_solar,
            accum_dust_nuclear=accum_dust_nuclear,
            cleaning_panels=clean_panel,
            cleaning_rads=clean_plant,
            dt=clock.dt,
            dust_rate=dust_rate,
            functional_covered=functional_covered,
        ):
            """Transition function for accum_dust s"""
            accum_dust_solar_new = min(
                max(
                    accum_dust_solar
                    + dt * (-dust_rate * functional_covered + cleaning_panels),
                    0.0,
                ),
                1.0,
            )
            accum_dust_nuclear_new = min(
                max(accum_dust_nuclear + dt * (-dust_rate + cleaning_rads), 0.0), 1.0
            )
            return accum_dust_solar_new, accum_dust_nuclear_new

        @make_function(functional_covered)
        def f_functional_covered(covering_panels=cover_panel):
            """Transition function for covering_panels_solar"""
            functional_covered_new = covering_panels
            return functional_covered_new

    return energy_performance
