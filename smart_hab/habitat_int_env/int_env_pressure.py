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
                                struct_health,
                                HM_pressure_lower_setpoint,
                                HM_pressure_upper_setpoint):
    with System(name="int_env_pressure", description="The int_env_pressure environment") as int_env_pressure:
        int_env_pres = State(name="int_env_pres",
                                  value=1.0,
                                  units="atm",
                                  description="Air pressure inside the habitat")
        structure_sec_1 = Variable(name="structure_sec_1",
                                     value=struct_health.value[0],
                                     units="",
                                     description="health level of the dome section 1; 1 is the healthiest")
        structure_sec_2 = Variable(name="structure_sec_2",
                                     value=struct_health.value[1],
                                     units="",
                                     description="health level of the dome section 2; 1 is the healthiest")
        structure_sec_3 = Variable(name="structure_sec_3",
                                     value=struct_health.value[2],
                                     units="",
                                     description="health level of the dome section 3; 1 is the healthiest")
        structure_sec_4 = Variable(name="structure_sec_4",
                                     value=struct_health.value[3],
                                     units="",
                                     description="health level of the dome section 4; 1 is the healthiest")
        structure_sec_5 = Variable(name="structure_sec_5",
                                     value=struct_health.value[4],
                                     units="",
                                     description="health level of the dome section 5; 1 is the healthiest")

        @make_function(int_env_pres)
        def f_interior_env_pres(lower_pressure_setpo=HM_pressure_lower_setpoint,
                                upper_pressure_setpo=HM_pressure_upper_setpoint,
                                air_leak_coeficent=dome_specs.air_leak_coeficent,
                                out_of_str_pres=dome_specs.out_of_str_pres,
                                structure_sec_1=structure_sec_1,
                                structure_sec_2=structure_sec_2,
                                structure_sec_3=structure_sec_3,
                                structure_sec_4=structure_sec_4,
                                structure_sec_5=structure_sec_5,
                                en_used_pres=en_used_pres,
                                en_needed_pres=en_needed_pres):
            """Transition function for interior_env heat"""
            latent_struct_int_env = (structure_sec_1 +
                                     structure_sec_2 +
                                     structure_sec_3 +
                                     structure_sec_4 +
                                     structure_sec_5) / 5
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
                                     (((1 - latent_struct_int_env) *
                                       air_leak_coeficent + 0) *
                                      out_of_str_pres))
            return int_env_pres_new
        
    return int_env_pressure
