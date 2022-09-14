"""
Author: Amir Behjat

Date:
    7/08/2022


An int_env_pressure model.

variable :: TypeOfVariable

(variable) = optional variable

                                               ________________________
design                    :: DomeSpec     => |                        |
(eclss_used_energy_pres)    :: EClSS      => |                        | ->  energy needed for pressure control
(eclss_needed_energy_pres)  :: EClSS      => |                        |
Energy             :: available power     => |   int_envPressureEnv   |
(strucure_health)           :: Struct     => |                        | ->  energy used for pressure control
(pressure setpoints)        :: HM         => |                        |
                                              ________________________


"""

from cdcm import *

__all__ = ["make_int_env_pressure_env_0"]


def make_int_env_pressure_env_0(dome_specs,
                                en_used_pres,
                                en_needed_pres,
                                structure_sec_1,
                                structure_sec_2,
                                structure_sec_3,
                                structure_sec_4,
                                structure_sec_5,
                                HM_pressure_lower_setpoint,
                                HM_pressure_upper_setpoint):

    with System(name="int_env_pressure",
                description="The int_env_pressure environment") as int_env_pressure:
        int_env_pres = State(
            name="int_env_pres",
            value=1.0,
            units="atm",
            description="Air pressure inside the habitat")

        @make_function(int_env_pres)
        def f_interior_env_pres(
            lower_pressure_setpo=HM_pressure_lower_setpoint,
            upper_pressure_setpo=HM_pressure_upper_setpoint,
            air_leak_coeficent=dome_specs.air_leak_coeficent,
            out_of_str_pres=dome_specs.out_of_str_pres,
            en_used_pres=en_used_pres,
            en_needed_pres=en_needed_pres,
            structure_sec_1=structure_sec_1,
            structure_sec_2=structure_sec_2,
            structure_sec_3=structure_sec_3,
            structure_sec_4=structure_sec_4,
            structure_sec_5=structure_sec_5,
        ):

            latent_struct_int_env = (structure_sec_1 +
                                     structure_sec_2 +
                                     structure_sec_3 +
                                     structure_sec_4 +
                                     structure_sec_5) / 5

            if en_needed_pres == 0:
                int_env_pres_new = (
                    (lower_pressure_setpo + upper_pressure_setpo) / 2)
            else:
                int_env_pres_new = max(0.0, min(1.0,
                                                max(en_used_pres,
                                                    1 * 10 ** (-10)) /
                                                max(en_needed_pres,
                                                    1 * 10 ** (-4))) *
                                       ((lower_pressure_setpo +
                                           upper_pressure_setpo) / 2) +
                                       (1 - min(1.0, max(en_used_pres,
                                                         1 * 10 ** (-10)) /
                                                max(en_needed_pres,
                                                    1 * 10 ** (-4)))) *
                                       (((1.0 - latent_struct_int_env) *
                                           air_leak_coeficent + 0) *
                                        out_of_str_pres))
            return int_env_pres_new

    return int_env_pressure
