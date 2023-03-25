"""
Author: Amir Behjat

Date:
    7/08/2022


Makes the dome specs system with all its design and fixed parameters.

variable :: TypeOfVariable

(variable) = optional variable

 _________________
|                 |
|   DomeSpecsEnv  | -> dome_specs  :: DomeSpecs
|_________________|


"""

import math
import numpy as np

from cdcm import *

__all__ = ["make_dome_specs"]


def make_dome_specs():
    """
    Make a dome specs system. design[A long list of parameters] + All other physical constants that may affect multiple systems.

    Arguments
    - NULL

    """

    with System(name="dome_specs", description="The dome_specs system") as dome_specs:
        dome_radius = Parameter(
            name="dome_radius",
            value=2.9,
            units="m",
            description="radius of dome of the habitat",
        )

        dome_surface_area = Parameter(
            name="dome_surface_area",
            value=math.pi * dome_radius.value**2,
            units="m^2",
            description="surface area of dome of the habitat",
        )
        nominal_cond_coef = Parameter(
            name="nominal_cond_coef",
            value=2.25,
            units="W/(m*K)",
            description="conduction coeficent of an undamaged dome",
        )
        damaged_cond_coef = Parameter(
            name="damaged_cond_coef",
            value=2.25 * 20.0,
            units="W/(m*K)",
            description="conduction coeficent of a completley damaged dome",
        )
        dom_thickness = Parameter(
            name="dom_thickness",
            value=0.2,
            units="m",
            description="thickness of the wall of the dome",
        )
        surf_absorb_coef = Parameter(
            name="surf_absorb_coef",
            value=0.6,
            units="",
            description="Absorption coefficient for radiation by dome",
        )
        surf_emiss_coef = Parameter(
            name="surf_emiss_coef",
            value=0.9,
            units="",
            description="Emission coefficient for radiation from dome",
        )
        stefan_boltzmann_constant = Parameter(
            name="stefan_boltzmann_constant",
            value=5.67 * np.float_power(10, -8),
            units="W/K^4",
            description="Stefan–Boltzmann constant",
        )
        int_conv_coef = Parameter(
            name="int_conv_coef",
            value=1.0 * 25.0 * 2.0,
            units="W/(m^2*K)",
            description="Convection coefficient of the air inside the dome",
        )

        efficiency_of_PM = Parameter(
            name="efficiency_of_PM",
            value=31.25,
            units="J",
            description="Compressors efficiency for pressure adjustment",
        )
        pres_capac_per_vol = Parameter(
            name="pres_capac_per_vol",
            value=1.0035 * 1000,
            units="J/atm",
            description="Amount of energy needed to replace one atm of pressure (better model is based on the volume not pressure)",
        )
        air_leak_coeficent = Parameter(
            name="air_leak_coeficent",
            value=10.0 ** (-2),
            units="atm/sec",
            description="Air pressure loss per second for totally damaged dome",
        )

        air_heat_capac = Parameter(
            name="air_heat_capac",
            value=1.0035 * 1000,
            units="J/(kg*K)",
            description="Amount of energy required to change the temperature of 1 kg air's by 1 K",
        )

        efficiency_of_TM = Parameter(
            name="efficiency_of_TM",
            value=12.5,
            units="",
            description="AC efficiency for temperature adjustment",
        )

        out_of_str_pres = Parameter(
            name="out_of_str_pres",
            value=0.0,
            units="atm",
            description="Air Pressure on moon surface",
        )

    return dome_specs
