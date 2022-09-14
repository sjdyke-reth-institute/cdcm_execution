"""An int_env_pressure model.

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


__all__ = ["make_int_env_pressure_env_0"]



from cdcm import *

def make_int_env_pressure_env_0(dome_specs,
                                en_used_pres,
                                en_needed_pres,
                                structure_secs,
                                HM_pressure_lower_setpoint,
                                HM_pressure_upper_setpoint):
    # print('cccc',dome_specs,en_used_pres,en_needed_pres,structure_secs,HM_pressure_lower_setpoint,HM_pressure_upper_setpoint)
    with System(name="int_env_pressure", description="The int_env_pressure environment") as int_env_pressure:
        int_env_pres = State(name="int_env_pres",
                                  value=1.0,
                                  units="atm",
                                  description="Air pressure inside the habitat")


        @make_function(int_env_pres)
        def f_interior_env_pres(en_used_pres=en_used_pres,
                                en_needed_pres=en_needed_pres,
                                structure_secs=structure_secs,
                                lower_pressure_setpo=HM_pressure_lower_setpoint,
                                upper_pressure_setpo=HM_pressure_upper_setpoint,
                                air_leak_coeficent=dome_specs.air_leak_coeficent,
                                out_of_str_pres=dome_specs.out_of_str_pres
                                ):
            """Transition function for interior_env heat"""
            # print('f_interior_env_pres', structure_secs)
            try:
                structure_sec_1 = structure_secs[0]
            except:
                structure_sec_1 = 1.0
            try:
                structure_sec_2 = structure_secs[1]
            except:
                structure_sec_2 = 1.0
            try:
                structure_sec_3 = structure_secs[2]
            except:
                structure_sec_3 = 1.0
            try:
                structure_sec_4 = structure_secs[3]
            except:
                structure_sec_4 = 1.0
            try:
                structure_sec_5 = structure_secs[4]
            except:
                structure_sec_5 = 1.0
            latent_struct_int_env = (structure_sec_1 +
                                     structure_sec_2 +
                                     structure_sec_3 +
                                     structure_sec_4 +
                                     structure_sec_5) / 5
            # print('int_env_pres_new', latent_struct_int_env, en_used_pres, en_needed_pres, lower_pressure_setpo, upper_pressure_setpo, air_leak_coeficent)
            # input('xxxxxxxx')
            try:
                int_env_pres_new = max(0.0, min(1.0,
                                                  max(en_used_pres,
                                                      1 * 10 ** (-4)) /
                                                  max(en_needed_pres,
                                                      1 * 10 ** (-4))) *
                                         ((lower_pressure_setpo +
                                           upper_pressure_setpo) / 2) +
                                         (1 - min(1.0, max(en_used_pres,
                                                           1 * 10 ** (-4)) /
                                                  max(en_needed_pres,
                                                      1 * 10 ** (-4)))) *
                                         (((1.0 - latent_struct_int_env) *
                                           air_leak_coeficent + 0) *
                                          out_of_str_pres))
            except:
                int_env_pres_new = 1.0
            return int_env_pres_new
        
    return int_env_pressure
