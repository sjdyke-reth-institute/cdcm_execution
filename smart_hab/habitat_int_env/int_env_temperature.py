"""An int_env_temperature model.


variable :: TypeOfVariable

(variable) = optional variable
                                              ________________________
design                    :: DomeSpec     => |                        |
(eclss_used_energy_heat)    :: EClSS      => |                        | ->  energy needed for pressure control
(eclss_needed_energy_heat)  :: EClSS      => |                        |
(strucure_temp_innerside)   :: Struct     => | int_envTemperatureEnv  |
(strucure_health)           :: Struct     => |                        | ->  energy used for pressure control
(temperature setpoints)     :: HM         => |                        |
                                              ________________________


"""

__all__ = ["make_int_env_temperature_env_0"]



from cdcm import *

def make_int_env_temperature_env_0(en_used_heat,
                                   en_needed_heat,
                                   structure_int_struct_temp,
                                   HM_temperature_lower_setpoint,
                                   HM_temperature_upper_setpoint
                                   ):
    with System(name="int_env_temperature", description="The int_env_temperature environment") as int_env_temperature:
        int_env_temp = (make_node("S:int_env_temp",
                                  value=298.0,
                                  units="K",
                                  description="Air temperature inside the habitat"))

        @make_function(int_env_temp)
        def f_interior_env_heat(en_used_heat=en_used_heat,
                                en_needed_heat=en_needed_heat,
                                int_str_temp=structure_int_struct_temp,
                                lower_temp_setpo=HM_temperature_lower_setpoint,
                                upper_temp_setpo=HM_temperature_upper_setpoint
                                ):
            """Transition function for interior_env heat"""
            int_env_temp_new = max(100.0,
                                     min(400.0,
                                         1.0 * (min(1.0,
                                                    max(en_used_heat,
                                                        1 * 10 ** (-4)) /
                                                    max(en_needed_heat,
                                                        1 * 10 ** (-4)))) *
                                         ((lower_temp_setpo +
                                           upper_temp_setpo) / 2) + 1.0 *
                                         (1 - min(1.0,
                                                  (max(en_used_heat,
                                                       1 * 10 ** (-4)) /
                                                   max(en_needed_heat,
                                                       1 * 10 ** (-4))))) *
                                         int_str_temp))
            return int_env_temp_new
    return int_env_temperature
