"""
Makes the dome specs system with all its design and fixed parameters.

variable :: TypeOfVariable

(variable) = optional variable

 _________________
|                 |
|   DomeSpecsEnv  | -> design[A long list of parameters]
|_________________|

"""


__all__ = ["make_dome_specs"]

import math

from cdcm import *



def make_dome_specs():
    """
    Make a dome specs system.

    Arguments

    """

    with System(name="dome_specs", description="The dome_specs system") as dome_specs:
        dome_radius = Parameter(
            name="dome_radius",
            value=2.9,
            units="m",
            description="radius of dome of the habitat"
        )

        dome_surface_area = Parameter(
            name="dome_surface_area",
            value=math.pi * dome_radius.value **2,
            units="m^2",
            description="surface area of dome of the habitat"
        )
        nominal_cond_coef = (make_node("P:nominal_cond_coef",
                                       value=2.25,
                                       units="W/(m*K)",
                                       description="nominal_cond_coef"))
        damaged_cond_coef = (make_node("P:damaged_cond_coef",
                                       value=2.25 * 20.0,
                                       units="W/(m*K)",
                                       description="damaged_cond_coef"))
        dom_thickness = (make_node("P:dom_thickness",
                                   value=0.2,
                                   units="m",
                                   description="dom_thickness"))
        surf_absorb_coef = (make_node("P:surf_absorb_coef",
                                      value=0.6,
                                      units="",
                                      description="surf_absorb_coef"))
        surf_emiss_coef = (make_node("P:surf_emiss_coef",
                                     value=0.9,
                                     units="",
                                     description="surf_emiss_coef"))
        stefan_boltzmann_constant = (make_node("P:stefan_boltzmann_constant",
                                          value=5.67 * math.pow(10, -8),
                                          units="W/K^4",
                                          description="Stefan–Boltzmann constant"))
        int_conv_coef = (make_node("P:int_conv_coef",
                                   value=1.0 * 25.0 * 2.0,
                                   units="W/(m^2*K)",
                                   description="int_conv_coef"))

        efficiency_of_PM = (make_node("P:efficiency_of_PM",
                                      value=31.25,
                                      units="",
                                      description="efficiency_of_PM"))
        pres_capac_per_vol = (make_node("P:pres_capac_per_vol",
                                        value=1.0035 * 1000,
                                        units="J/atm",
                                        description="pres_capac_per_vol"))
        air_leak_coeficent = (make_node("P:air_leak_coeficent",
                                        value=10.0 ** (-2),
                                        units="atm/sec",
                                        description="air_leak_coeficent"))

        air_heat_capac = (make_node("P:air_heat_capac",
                                    value=1.0035 * 1000,
                                    units="J/(kg*K)",
                                    description="air_heat_capac"))

        efficiency_of_TM = (make_node("P:efficiency_of_TM",
                                      value=12.5,
                                      units="",
                                      description="efficiency_of_TM"))

        out_of_str_pres = (make_node("P:out_of_str_pres",
                                     value=0.0,
                                     units="atm",
                                     description="out_of_str_pres"))

    return dome_specs